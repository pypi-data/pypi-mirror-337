# 🔍 HRegex – A Pythonic Human-Readable Regex Builder  

[![PyPI Version](https://img.shields.io/pypi/v/hregex?color=blue&label=PyPI&logo=pypi)](https://pypi.org/project/hregex/)
[![Build](https://img.shields.io/github/actions/workflow/status/farhaanaliii/hregex/.github/workflows/tests.yml?logo=github&label=Build)](https://github.com/farhaanaliii/hregex/actions)
[![License](https://img.shields.io/github/license/farhaanaliii/hregex?color=brightgreen)](LICENSE)  
[![Issues](https://img.shields.io/github/issues/farhaanaliii/hregex?color=yellow)](https://github.com/farhaanaliii/hregex/issues)  
[![Stars](https://img.shields.io/github/stars/farhaanaliii/hregex?style=social)](https://github.com/farhaanaliii/hregex)  

HRegex is a **Python version** of the [human-regex](https://github.com/rajibola/human-regex) project, designed to simplify regex creation using an **intuitive, chainable API**. This allows developers to write **cleaner, more readable** regular expressions without dealing with cryptic syntax.  

---

## ✨ Features  

✅ **Human-Readable API** – No more regex headaches!  
✅ **Fluent Method Chaining** – Build patterns step by step.  
✅ **Predefined Ranges & Quantifiers** – Easily match letters, digits, symbols, and more.  
✅ **Unicode Support** – Handle multilingual characters effortlessly.  
✅ **Advanced Flags & Groups** – Apply regex modifiers and groups with ease.  

---

## 📦 Installation  

### ⏳ Install via pip  

```sh
pip install hregex
```

### 🛠 Manual Installation  

```sh
git clone https://github.com/farhaanaliii/hregex.git
cd hregex
python setup.py install
```

---

## 🚀 Quick Start  

### 🔢 Match Digits and Special Characters  

```python
from hregex import HRegex  

pattern = HRegex().has_digit().has_special_character().to_regexp()  
match = pattern.match("Hello@123")  

print(bool(match))  # True
```

### 📧 Validate Email  

```python
pattern = HRegex().word().one_or_more().literal("@").word().one_or_more().literal(".").word().one_or_more().to_regexp()  

print(bool(pattern.match("user@example.com")))  # True
print(bool(pattern.match("invalid-email")))  # False
```


---

## 🛠 API Reference  

### 📌 Character Classes  

| Method | Description |
|--------|------------|
| `.digit()` | Matches any digit (`\d`). |
| `.word()` | Matches any word character (`\w`). |
| `.whitespace()` | Matches whitespace (`\s`). |
| `.non_whitespace()` | Matches non-whitespace (`\S`). |
| `.letter()` | Matches any letter (A-Z, a-z). |
| `.any_character()` | Matches any character (`.`). |

### 📌 Quantifiers  

| Method | Description |
|--------|------------|
| `.optional()` | Matches 0 or 1 occurrence (`?`). |
| `.one_or_more()` | Matches 1 or more occurrences (`+`). |
| `.zero_or_more()` | Matches 0 or more occurrences (`*`). |
| `.exactly(n)` | Matches exactly `n` times (`{n}`). |
| `.at_least(n)` | Matches `n` or more times (`{n,}`). |
| `.at_most(n)` | Matches up to `n` times (`{0,n}`). |
| `.between(min, max)` | Matches between `min` and `max` times (`{min,max}`). |

### 📌 Grouping & Anchors  

| Method | Description |
|--------|------------|
| `.start_group()` | Starts a non-capturing group (`(?: ... )`). |
| `.start_capture_group()` | Starts a capturing group (`( ... )`). |
| `.end_group()` | Closes a group (`)`). |
| `.start_named_group(name)` | Starts a named capturing group (`(?P<name> ... )`). |
| `.start_anchor()` | Matches the start of a string (`^`). |
| `.end_anchor()` | Matches the end of a string (`$`). |

### 📌 Flags  

| Method | Description |
|--------|------------|
| `.global_()` | Enables global matching (`g`). |
| `.non_sensitive()` | Case-insensitive matching (`i`). |
| `.multiline()` | Multi-line mode (`m`). |
| `.dot_all()` | Allows `.` to match newlines (`s`). |
| `.unicode_digit()` | Matches Unicode digits (`\p{N}`). |
| `.unicode_punctuation()` | Matches Unicode punctuation (`\p{P}`). |
| `.unicode_symbol()` | Matches Unicode symbols (`\p{S}`). |

---

## 🧪 Running Tests  

Run the test suite using:  

```sh
python -m unittest discover -s tests
```

---

## 📜 License  

This project is licensed under the [Apache License](LICENSE).  

---

## 🤝 Contributing  

Contributions are welcome! Feel free to:  

- Open an [issue](https://github.com/farhaanaliii/hregex/issues) for bug reports or feature requests.  
- Submit a pull request with improvements.  

---

## ⭐ Show Your Support  

If you like this project, please consider **starring** ⭐ it on GitHub!  

[![Stars](https://img.shields.io/github/stars/farhaanaliii/hregex?style=social)](https://github.com/farhaanaliii/hregex)  
