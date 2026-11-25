"""ClipCraft window in WR colours with an English/Polish switch. Author: WR"""

import threading
from pathlib import Path
from tkinter import PhotoImage

import customtkinter as ctk
from PIL import Image

from . import i18n, pipeline
from .chapters import split_into_chapters
from .config import IMAGE_SIZES, Settings
from .theme import ERROR, INK, INK_2, LINE, MONO, MUTED, PAPER, SANS, SIGNAL, SIGNAL_HOVER, SLATE
from .tiktokvoice import VOICES

ASSETS = Path(__file__).parent / "assets"
BOX = dict(fg_color=INK, border_color=LINE, border_width=1, corner_radius=8, text_color=PAPER)


class App(ctk.CTk):
    def __init__(self, lang: str):
        super().__init__(fg_color=INK)
        ctk.set_appearance_mode("dark")
        self.geometry("900x700")
        self.minsize(760, 640)
        self._icon = PhotoImage(file=ASSETS / "wr-icon.png")
        self.iconphoto(True, self._icon)
        logo = Image.open(ASSETS / "wr-logo.png")
        self._logo = ctk.CTkImage(logo, size=(logo.width // 2, logo.height // 2))
        self.form = {
            "script": "",
            "out": "output",
            "size": IMAGE_SIZES[0],
            "length": "300",
            "voice": "en_us_006",
            "images": True,
            "video": True,
            "subtitles": True,
        }
        self._set_lang(lang.upper())

    # layout
    def _build(self):
        for child in self.winfo_children():
            child.destroy()
        t = self.text
        self.title(f"WR · {t['title']}")

        head = ctk.CTkFrame(self, fg_color=INK, corner_radius=0)
        head.pack(fill="x", padx=24, pady=(20, 12))
        ctk.CTkLabel(head, image=self._logo, text="").pack(side="left")
        ctk.CTkFrame(head, width=2, height=28, fg_color=LINE, corner_radius=0).pack(side="left", padx=16)
        ctk.CTkLabel(head, text=t["title"], text_color=PAPER, font=(SANS, 18, "bold")).pack(side="left")
        ctk.CTkLabel(head, text=f"  {t['subtitle']}", text_color=MUTED, font=(SANS, 13)).pack(side="left")
        switch = ctk.CTkSegmentedButton(
            head,
            values=["EN", "PL"],
            command=self._set_lang,
            font=(SANS, 12, "bold"),
            fg_color=INK_2,
            selected_color=SIGNAL,
            selected_hover_color=SIGNAL_HOVER,
            unselected_color=INK_2,
            unselected_hover_color=LINE,
            text_color=PAPER,
        )
        switch.set(self.lang.upper())
        switch.pack(side="right")

        body = ctk.CTkFrame(self, fg_color=INK_2, corner_radius=12, border_width=1, border_color=LINE)
        body.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(1, weight=1)

        self._label(body, t["script"]).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 4))
        self.script = ctk.CTkTextbox(body, font=(MONO, 13), wrap="word", **BOX)
        self.script.grid(row=1, column=0, sticky="nsew", padx=(20, 10))
        self.script.insert("1.0", self.form["script"])
        hint = ctk.CTkLabel(body, text=t["script_hint"], text_color=SLATE, font=(SANS, 11), wraplength=440, justify="left")
        hint.grid(row=2, column=0, sticky="w", padx=20, pady=(4, 0))

        side = ctk.CTkFrame(body, fg_color="transparent")
        side.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=(10, 20), pady=(16, 0))
        self.out = self._field(side, t["output_dir"], ctk.CTkEntry(side, font=(SANS, 13), **BOX), self.form["out"])
        self.length = self._field(side, t["chapter_length"], ctk.CTkEntry(side, font=(SANS, 13), **BOX), self.form["length"])
        menu = dict(
            fg_color=INK,
            button_color=LINE,
            button_hover_color=SLATE,
            text_color=PAPER,
            font=(SANS, 13),
            dropdown_fg_color=INK_2,
            dropdown_text_color=PAPER,
            dropdown_hover_color=LINE,
        )
        self.size = self._field(side, t["image_size"], ctk.CTkOptionMenu(side, values=list(IMAGE_SIZES), **menu))
        self.size.set(self.form["size"])
        self.voice = self._field(side, t["voice"], ctk.CTkOptionMenu(side, values=VOICES, **menu))
        self.voice.set(self.form["voice"])

        self._label(side, t["steps"]).pack(anchor="w", pady=(12, 4))
        self.checks = {}
        for key in ("images", "video", "subtitles"):
            box = ctk.CTkCheckBox(
                side,
                text=t[f"step_{key}"],
                font=(SANS, 13),
                text_color=PAPER,
                fg_color=SIGNAL,
                hover_color=SIGNAL_HOVER,
                border_color=SLATE,
                checkmark_color=INK,
            )
            if self.form[key]:
                box.select()
            box.pack(anchor="w", pady=3)
            self.checks[key] = box
        keys = ctk.CTkLabel(side, text=t["keys"], text_color=SLATE, font=(SANS, 11), wraplength=300, justify="left")
        keys.pack(anchor="w", pady=(10, 0))

        foot = ctk.CTkFrame(body, fg_color="transparent")
        foot.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=16)
        foot.grid_columnconfigure(1, weight=1)
        self.start = ctk.CTkButton(
            foot,
            text=t["start"],
            command=self._start,
            fg_color=SIGNAL,
            hover_color=SIGNAL_HOVER,
            text_color=INK,
            font=(SANS, 14, "bold"),
            corner_radius=8,
            width=170,
            height=38,
        )
        self.start.grid(row=0, column=0, rowspan=2, padx=(0, 16))
        self.progress = ctk.CTkProgressBar(foot, progress_color=SIGNAL, fg_color=INK, height=8)
        self.progress.set(0)
        self.progress.grid(row=0, column=1, sticky="ew", pady=(4, 6))
        self.status = ctk.CTkLabel(foot, text=t["ready"], text_color=MUTED, font=(SANS, 12), anchor="w")
        self.status.grid(row=1, column=1, sticky="ew")

    def _label(self, master, text):
        return ctk.CTkLabel(master, text=text, text_color=MUTED, font=(SANS, 12))

    def _field(self, master, label, widget, value=None):
        self._label(master, label).pack(anchor="w", pady=(0, 2))
        widget.pack(fill="x", pady=(0, 10))
        if value is not None:
            widget.insert(0, value)
        return widget

    def _remember(self):
        if not hasattr(self, "script"):
            return
        self.form.update(
            script=self.script.get("1.0", "end-1c"),
            out=self.out.get(),
            size=self.size.get(),
            length=self.length.get(),
            voice=self.voice.get(),
            **{k: bool(box.get()) for k, box in self.checks.items()},
        )

    def _set_lang(self, value: str):
        self._remember()
        self.lang = value.lower()
        self.text = i18n.load(self.lang)
        self._build()

    # actions
    def _say(self, text, error=False):
        self.status.configure(text=text, text_color=ERROR if error else MUTED)

    def _start(self):
        t = self.text
        self._remember()
        s = self.form
        if not s["script"].strip():
            return self._say(t["error_empty"], True)
        if not s["length"].isdigit() or int(s["length"]) < 1:
            return self._say(t["error_length"], True)
        settings = Settings.from_env()
        missing = settings.missing(s["images"], s["subtitles"])
        if missing:
            return self._say(t["error_missing"].format(names=", ".join(missing)), True)
        plan = pipeline.steps(s["images"], s["video"], s["subtitles"])
        if not plan:
            return
        chapters = split_into_chapters(s["script"], int(s["length"]))
        self.start.configure(state="disabled")
        threading.Thread(target=self._run, args=(plan, chapters, dict(s), settings), daemon=True).start()

    def _run(self, plan, chapters, s, settings):
        out = Path(s["out"])
        images, voices, video = out / "images", out / "voices", out / "complete_clip.mp4"
        actions = {
            "images": lambda: pipeline.generate_images(chapters, images, s["size"], settings),
            "voices": lambda: pipeline.generate_voices(chapters, voices, s["voice"]),
            "video": lambda: pipeline.generate_video(images, voices, out, len(chapters)),
            "subtitles": lambda: pipeline.add_subtitles(video, settings),
        }
        result = video
        for done, step in enumerate(plan):
            name = self.text[f"step_name_{step}"]
            self.after(0, self._say, self.text["running"].format(step=name, done=done, total=len(plan)))
            try:
                result = actions[step]() or result
            except Exception as error:  # report any failure in the UI instead of a silent console print
                self.after(0, self._finish, self.text["error_step"].format(step=name, error=error), True)
                return
            self.after(0, self.progress.set, (done + 1) / len(plan))
        self.after(0, self._finish, self.text["done"].format(path=result), False)

    def _finish(self, text, error):
        self.start.configure(state="normal")
        self._say(text, error)


def main():
    App(i18n.default_language()).mainloop()
