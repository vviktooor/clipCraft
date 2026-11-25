"""Settings read from the environment so API keys never pass through the UI or logs. Author: WR"""

import os
import shutil
from dataclasses import dataclass

IMAGE_SIZES = ("1024x1792", "1024x1024", "1792x1024")


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    assemblyai_api_key: str
    imagemagick: str
    subtitle_font: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
            assemblyai_api_key=os.environ.get("ASSEMBLYAI_API_KEY", ""),
            imagemagick=os.environ.get("IMAGEMAGICK_BINARY") or shutil.which("magick") or shutil.which("convert") or "",
            subtitle_font=os.environ.get("SUBTITLE_FONT", "Poppins-Bold"),
        )

    def missing(self, images: bool, subtitles: bool) -> list[str]:
        """Names of environment variables the selected steps still need."""
        needed = []
        if images and not self.openai_api_key:
            needed.append("OPENAI_API_KEY")
        if subtitles and not self.assemblyai_api_key:
            needed.append("ASSEMBLYAI_API_KEY")
        if subtitles and not self.imagemagick:
            needed.append("IMAGEMAGICK_BINARY")
        return needed
