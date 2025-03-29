import unittest
import re
from hregex import HRegex

class TestHRegex(unittest.TestCase):

    def test_digit(self):
        pattern = HRegex().digit().to_string()
        self.assertEqual(pattern, r"\d")
        self.assertTrue(re.match(pattern, "5"))
        self.assertFalse(re.match(pattern, "a"))

    def test_word(self):
        pattern = HRegex().word().to_string()
        self.assertEqual(pattern, r"\w")
        self.assertTrue(re.match(pattern, "a"))
        self.assertTrue(re.match(pattern, "1"))
        self.assertFalse(re.match(pattern, "@"))

    def test_whitespace(self):
        pattern = HRegex().whitespace().to_string()
        self.assertEqual(pattern, r"\s")
        self.assertTrue(re.match(pattern, " "))
        self.assertFalse(re.match(pattern, "a"))

    def test_non_whitespace(self):
        pattern = HRegex().non_whitespace().to_string()
        self.assertEqual(pattern, r"\S")
        self.assertTrue(re.match(pattern, "a"))
        self.assertFalse(re.match(pattern, " "))

    def test_literal(self):
        pattern = HRegex().literal("hello").to_string()
        self.assertEqual(pattern, r"hello")
        self.assertTrue(re.match(pattern, "hello"))
        self.assertFalse(re.match(pattern, "Hello"))

    def test_or(self):
        pattern = HRegex().literal("yes").or_().literal("no").to_string()
        self.assertEqual(pattern, r"yes|no")
        self.assertTrue(re.match(pattern, "yes"))
        self.assertTrue(re.match(pattern, "no"))
        self.assertFalse(re.match(pattern, "maybe"))

    def test_range(self):
        pattern = HRegex().range_("letter").to_string()
        self.assertEqual(pattern, r"[a-zA-Z]")
        self.assertTrue(re.match(pattern, "a"))
        self.assertTrue(re.match(pattern, "Z"))
        self.assertFalse(re.match(pattern, "1"))

    def test_not_range(self):
        pattern = HRegex().not_range("0-9").to_string()
        self.assertEqual(pattern, r"[^0-9]")
        self.assertTrue(re.match(pattern, "a"))
        self.assertFalse(re.match(pattern, "5"))

    def test_lazy(self):
        pattern = HRegex().digit().lazy().to_string()
        self.assertEqual(pattern, r"\d?")
        self.assertTrue(re.match(pattern, "5"))
        self.assertTrue(re.match(pattern, ""))  # Lazy allows zero occurrences

    def test_quantifiers(self):
        pattern = HRegex().digit().one_or_more().to_string()
        self.assertEqual(pattern, r"\d+")
        self.assertTrue(re.match(pattern, "123"))
        self.assertFalse(re.match(pattern, "abc"))

        pattern = HRegex().digit().zero_or_more().to_string()
        self.assertEqual(pattern, r"\d*")
        self.assertTrue(re.match(pattern, "123"))
        self.assertTrue(re.match(pattern, ""))  # Zero occurrences valid

    def test_anchors(self):
        pattern = HRegex().start_anchor().literal("hello").end_anchor().to_string()
        self.assertEqual(pattern, r"^hello$")
        self.assertTrue(re.fullmatch(pattern, "hello"))
        self.assertFalse(re.fullmatch(pattern, "hello world"))

    def test_flags(self):
        pattern = HRegex().literal("hello").non_sensitive().to_regexp()
        self.assertTrue(pattern.match("HELLO"))
        self.assertFalse(pattern.match("HELLO") is None)

        pattern = HRegex().literal("hello").multiline().to_regexp()
        self.assertTrue(pattern.match("hello"))

    def test_unicode(self):
        pattern = HRegex().unicode_digit().to_string()
        self.assertEqual(pattern, r"\p{N}")
        
        pattern = HRegex().unicode_char().to_string()
        self.assertEqual(pattern, r"\p{L}")

    def test_path(self):
        pattern = HRegex().path().to_string()
        self.assertEqual(pattern, r"(/\w+)*")
        self.assertTrue(re.match(pattern, "/home/user/docs"))
        self.assertTrue(re.match(pattern, "/index.html"))

    def test_named_group(self):
        pattern = HRegex().start_named_group("number").digit().end_group().to_string()
        self.assertEqual(pattern, r"(?P<number>\d)")
        match = re.match(pattern, "5")
        self.assertIsNotNone(match)
        self.assertEqual(match.group("number"), "5")

    def test_capture_group(self):
        pattern = HRegex().start_capture_group().digit().end_group().to_string()
        self.assertEqual(pattern, r"(\d)")
        match = re.match(pattern, "5")
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "5")

if __name__ == "__main__":
    unittest.main()
    