<p>
  <img src=".github/readme/banner.svg" width="100%" alt="WR · clipCraft: Text-to-video generator with AI">
</p>

<p><img alt="English" src="https://img.shields.io/badge/English-20C9B0?style=flat-square">&nbsp;<a href="README.pl.md"><img alt="Polski" src="https://img.shields.io/badge/Polski-526077?style=flat-square"></a></p>

<p>
  <img alt="status: active" src="https://img.shields.io/badge/status-active-20C9B0?style=flat-square&labelColor=121B2B">
  <img alt="stack: Python · OpenAI · AssemblyAI" src="https://img.shields.io/badge/stack-Python%20%C2%B7%20OpenAI%20%C2%B7%20AssemblyAI-3267E9?style=flat-square&labelColor=121B2B">
  <a href="../../actions/workflows/ci.yml"><img alt="CI" src="../../actions/workflows/ci.yml/badge.svg"></a>
  <img alt="license: public" src="https://img.shields.io/badge/license-public-526077?style=flat-square&labelColor=121B2B">
</p>

**Desktop app that turns text into a narrated video with AI-generated images.**
Images come from OpenAI (`dall-e-3`), narration from TikTok Voice TTS, subtitles from AssemblyAI. Example videos: [YouTube playlist](https://www.youtube.com/playlist?list=PLlVNFvFbjZ3G73D6XfwyN_exaYW9FQOk6).

<p align="center"><img alt="Preview: ClipCraft window with a script ready to convert" src="docs/screenshots/form.en.png" width="85%"></p>

## Features

- **Chapters**: the script is split on whole sentences up to a set length; one image and one voice clip per chapter.
- **Pick the steps**: images, voice and video, subtitles; each can be switched off.
- **Image sizes** for `dall-e-3`: `1024x1792`, `1024x1024` or `1792x1024`.
- **Safe keys**: API keys come from environment variables, are never typed into the window and never printed.
- **English and Polish** interface, WR look (logo, ink and signal colours, Poppins), errors shown in the window.

## Quick start

Requirements: Python 3.10+ with Tkinter, ImageMagick (for subtitles), OpenAI and AssemblyAI keys.

```bash
git clone https://github.com/vviktooor/clipCraft.git
cd clipCraft
pip3 install -r requirements.txt
export OPENAI_API_KEY=... ASSEMBLYAI_API_KEY=...
python3 -m clipcraft
```

## Configuration

Variables (see `.env.example`): `OPENAI_API_KEY`, `ASSEMBLYAI_API_KEY`, `IMAGEMAGICK_BINARY` (path to `magick`; found on `PATH` when empty), `SUBTITLE_FONT`, `APP_LANG` (`en` or `pl`).

## Example output

A frame from a generated clip with burned-in subtitles:

<p align="center"><img alt="Frame of a generated clip" src="docs/screenshots/example-clip-frame.png" width="280"></p>

## Usage

Paste the script, choose output folder, chapter length, image size and narrator voice, tick the steps and press **Create clip**. Results land in the output folder: `images/`, `voices/`, `complete_clip.mp4` and the subtitled copy.

## Languages

This README is available in English (default) and [Polish](README.pl.md). Interface: English by default, Polish via the EN/PL switch or `APP_LANG=pl` (strings in `clipcraft/locales/`).

## Repository layout

| Where | What |
|---|---|
| `clipcraft/gui.py` | CustomTkinter window |
| `clipcraft/pipeline.py` | Images, voices, video and subtitles steps |
| `clipcraft/chapters.py` | Script splitting |
| `clipcraft/config.py` | Settings from environment variables |
| `clipcraft/tiktokvoice.py` | TikTok TTS client (third-party, adapted) |
| `clipcraft/locales/` | `en.json` and `pl.json` |
| `tests/` | Unit tests |
| `docs/screenshots/` | Screenshots from the running app |

## Tests and quality

```bash
ruff check .
ruff format --check .
python3 -m unittest discover -s tests
```

| Check | Result | Date |
|---|---|---|
| ruff | PASS | 2026-11-25 |
| Tests | PASS (9/9) | 2026-11-25 |
| Screenshots | PASS (real app under Xvfb, EN and PL) | 2026-11-25 |
| Full generation | NOT VERIFIED (needs paid OpenAI and AssemblyAI keys) | 2026-11-25 |

## Credits

[@oscie57](https://github.com/oscie57): [TikTok Voice TTS](https://github.com/oscie57/tiktok-voice).

## License

No licence file: all rights reserved. Ask before reusing the code. Author: WR.

Found a bug or have an idea? [Open an issue](../../issues).
