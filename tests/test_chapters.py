import unittest

from clipcraft.chapters import split_into_chapters


class ChaptersTest(unittest.TestCase):
    def test_groups_sentences_under_limit(self):
        text = "One. Two. Three is longer!"
        self.assertEqual(split_into_chapters(text, 10), ["One. Two.", "Three is longer!"])

    def test_keeps_long_sentence_whole(self):
        self.assertEqual(split_into_chapters("A very long sentence here.", 5), ["A very long sentence here."])

    def test_normalises_whitespace(self):
        self.assertEqual(split_into_chapters("  Hi.\n\nBye?  ", 100), ["Hi. Bye?"])

    def test_empty(self):
        self.assertEqual(split_into_chapters("   ", 100), [])

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            split_into_chapters("x", 0)


if __name__ == "__main__":
    unittest.main()
