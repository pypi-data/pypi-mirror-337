from typing import List, Set
import re
from .__version__ import *

class Flags:
    GLOBAL: str = "g"
    NON_SENSITIVE: str = "i"
    MULTILINE: str = "m"
    DOT_ALL: str = "s"
    UNICODE: str = "u"
    STICKY: str = "y"

class Ranges:
    digit: str = "0-9"
    lowercase_letter: str = "a-z"
    uppercase_letter: str = "A-Z"
    letter: str = "a-zA-Z"
    alphanumeric: str = "a-zA-Z0-9"
    any_character: str = "."

class Quantifiers:
    zero_or_more: str = "*"
    one_or_more: str = "+"
    optional: str = "?"
    exactly: str = "exactly"
    at_least: str = "atLeast"
    at_most: str = "atMost"
    between: str = "between"
    repeat: str = "repeat"

class HRegex:
    def __init__(self):
        self.parts: List[str] = []
        self.flags: Set[str] = set()
    
    def add(self, part: str):
        self.parts.append(part)
        return self
    
    def digit(self):
        return self.add(r"\d")
    
    def special(self):
        return self.add(r"(?=.*[!@#$%^&*])")
    
    def word(self):
        return self.add(r"\w")
    
    def whitespace(self):
        return self.add(r"\s")
    
    def non_whitespace(self):
        return self.add(r"\S")
    
    def literal(self, text: str):
        return self.add(re.escape(text))
    
    def or_(self):
        return self.add("|")
    
    def range_(self, name: str):
        range_value = getattr(Ranges, name, None)
        if not range_value:
            raise ValueError(f"Unknown range: {name}")
        
        return self.add(f"[{range_value}]")
    
    def not_range(self, chars: str):
        return self.add(f"[^{chars}]")
    
    def lazy(self):
        if not self.parts:
            raise ValueError("No quantifier to make lazy")
        self.parts[-1] += "?"
        return self
    
    def letter(self):
        return self.add(f"[{Ranges.letter}]")
    
    def any_character(self):
        return self.add(Ranges.any_character)
    
    def has_special_character(self):
        return self.add(r"(?=.*[!@#$%^&*])")

    def has_digit(self):
        return self.add(r"(?=.*\d)")

    def has_letter(self):
        return self.add(r"(?=.*[a-zA-Z])")

    def optional(self):
        return self.add(Quantifiers.optional)
    
    def exactly(self, n: int):
        return self.add(f"{{{n}}}")

    def at_least(self, n: int):
        return self.add(f"{{{n},}}")

    def at_most(self, n: int):
        return self.add(f"{{0,{n}}}")

    def between(self, min_: int, max_: int):
        return self.add(f"{{{min_},{max_}}}")
    
    def one_or_more(self):
        return self.add(Quantifiers.one_or_more)

    def zero_or_more(self):
        return self.add(Quantifiers.zero_or_more)

    def start_named_group(self, name: str):
        return self.add(f"(?P<{name}>")

    def start_group(self):
        return self.add("(?:")  

    def start_capture_group(self):
        return self.add("(")
    
    def word_boundary(self):
        return self.add(r"\b")

    def non_word_boundary(self):
        return self.add(r"\B")

    def end_group(self):
        return self.add(")")

    def start_anchor(self):
        return self.add("^")

    def end_anchor(self):
        return self.add("$")

    def global_(self):
        self.flags.add(Flags.GLOBAL)
        return self
    
    def non_sensitive(self):
        self.flags.add(Flags.NON_SENSITIVE)
        return self

    def multiline(self):
        self.flags.add(Flags.MULTILINE)
        return self

    def dot_all(self):
        self.flags.add(Flags.DOT_ALL)
        return self
    
    def unicode_char(self, variant: str = ""):
        if variant not in {"u", "l", "t", "m", "o", ""}:
            raise ValueError(f"Invalid Unicode letter variant: {variant}")
        self.flags.add(Flags.UNICODE)
        return self.add(fr"\p{{L{variant}}}")

    def unicode_digit(self):
        self.flags.add(Flags.UNICODE)
        return self.add(r"\p{N}")

    def unicode_punctuation(self):
        self.flags.add(Flags.UNICODE)
        return self.add(r"\p{P}")

    def unicode_symbol(self):
        self.flags.add(Flags.UNICODE)
        return self.add(r"\p{S}")
    
    def repeat(self, count: int):
        if not self.parts:
            raise ValueError("No pattern to repeat")
        self.parts[-1] = f"({self.parts[-1]}){{{count}}}"
        return self

    def path(self):
        return self.add(r"(/\w+)*")

    def to_string(self):
        return "".join(self.parts)

    def to_regexp(self):
        flags = 0
        if Flags.MULTILINE in self.flags:
            flags |= re.MULTILINE
        if Flags.NON_SENSITIVE in self.flags:
            flags |= re.IGNORECASE
        if Flags.DOT_ALL in self.flags:
            flags |= re.DOTALL
        return re.compile(self.to_string(), flags)
