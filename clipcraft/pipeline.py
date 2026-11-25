"""Generation steps. Heavy libraries are imported inside each step so the GUI and tests start without them. Author: WR"""

import logging
import time
from pathlib import Path

from .config import Settings
from .theme import INK, PAPER

log = logging.getLogger("clipcraft")


def generate_images(chapters: list[str], out: Path, size: str, settings: Settings) -> None:
    import requests
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    out.mkdir(parents=True, exist_ok=True)
    for number, chapter in enumerate(chapters, start=1):
        response = client.images.generate(prompt=chapter, n=1, size=size, model="dall-e-3")
        image = requests.get(response.data[0].url, timeout=60)
        image.raise_for_status()
        (out / f"image_{number}.png").write_bytes(image.content)
        log.info("image %d/%d saved", number, len(chapters))


def generate_voices(chapters: list[str], out: Path, voice: str) -> None:
    from .tiktokvoice import tts

    out.mkdir(parents=True, exist_ok=True)
    for number, chapter in enumerate(chapters, start=1):
        tts(chapter, voice, str(out / f"chapter{number}.mp3"))
        log.info("voice %d/%d saved", number, len(chapters))


def generate_video(images: Path, voices: Path, out: Path, count: int) -> Path:
    from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips

    clips = []
    for number in range(1, count + 1):
        audio = AudioFileClip(str(voices / f"chapter{number}.mp3"))
        clips.append(ImageClip(str(images / f"image_{number}.png")).set_duration(audio.duration).set_audio(audio))
    out.mkdir(parents=True, exist_ok=True)
    target = out / "complete_clip.mp4"
    concatenate_videoclips(clips).write_videofile(
        str(target),
        fps=30,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=str(out / "temp-audio.m4a"),
        remove_temp=True,
    )
    return target


def add_subtitles(video: Path, settings: Settings) -> Path:
    import assemblyai as aai
    from moviepy.config import change_settings
    from moviepy.editor import CompositeVideoClip, TextClip, VideoFileClip
    from moviepy.video.tools.subtitles import SubtitlesClip

    change_settings({"IMAGEMAGICK_BINARY": settings.imagemagick})
    aai.settings.api_key = settings.assemblyai_api_key
    srt = video.with_suffix(".srt")
    srt.write_text(aai.Transcriber().transcribe(str(video)).export_subtitles_srt(), encoding="utf-8")

    main = VideoFileClip(str(video))
    width, height = main.size

    def caption(text):
        return TextClip(
            text,
            font=settings.subtitle_font,
            fontsize=40,
            color=PAPER,
            method="caption",
            size=(int(width * 0.75), None),
            bg_color=f"{INK}b3",
        )

    subs = SubtitlesClip(str(srt), caption).set_position(("center", int(height * 0.62)))
    target = video.with_name(f"{video.stem}_subtitles_{time.strftime('%Y%m%d-%H%M%S')}.mp4")
    CompositeVideoClip([main, subs], size=main.size).write_videofile(
        str(target),
        fps=main.fps,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=str(video.parent / "temp-audio.m4a"),
        remove_temp=True,
    )
    return target


def steps(images: bool, video: bool, subtitles: bool) -> list[str]:
    """Ordered step names for the progress bar."""
    plan = []
    if images:
        plan.append("images")
    if video:
        plan += ["voices", "video"]
    if subtitles:
        plan.append("subtitles")
    return plan
