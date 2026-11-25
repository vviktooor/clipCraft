import os
import unittest
from unittest import mock

from clipcraft import i18n
from clipcraft.config import Settings
from clipcraft.pipeline import steps


class ConfigTest(unittest.TestCase):
    def test_keys_from_env(self):
        env = {"OPENAI_API_KEY": "o", "ASSEMBLYAI_API_KEY": "a", "IMAGEMAGICK_BINARY": "/bin/magick"}
        with mock.patch.dict(os.environ, env):
            s = Settings.from_env()
        self.assertEqual((s.openai_api_key, s.assemblyai_api_key, s.imagemagick), ("o", "a", "/bin/magick"))
        self.assertEqual(s.missing(True, True), [])

    def test_missing_only_for_selected_steps(self):
        s = Settings("", "", "", "Poppins-Bold")
        self.assertEqual(s.missing(False, False), [])
        self.assertEqual(s.missing(True, False), ["OPENAI_API_KEY"])
        self.assertEqual(s.missing(False, True), ["ASSEMBLYAI_API_KEY", "IMAGEMAGICK_BINARY"])

    def test_steps_order(self):
        self.assertEqual(steps(True, True, True), ["images", "voices", "video", "subtitles"])
        self.assertEqual(steps(False, False, True), ["subtitles"])

    def test_locales_match(self):
        self.assertEqual(set(i18n.load("en")), set(i18n.load("pl")))
        for lang in i18n.LANGUAGES:
            self.assertTrue(all(i18n.load(lang).values()), lang)


if __name__ == "__main__":
    unittest.main()
