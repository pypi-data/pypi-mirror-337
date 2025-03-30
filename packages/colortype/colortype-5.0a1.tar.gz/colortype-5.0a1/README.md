# colortype

**colortype** is a simple ANSI color formatting library for Python. It helps you easily apply colors, styles, and cursor controls in terminal applications.

## Installation

You can install colortype via pip:
```sh
pip install colortype
```

## Features

### **1. Foreground Colors**
- Standard colors: `red`, `green`, `blue`, `yellow`, `purple`, `black`, `white`
- Light colors: `light_red`, `light_green`, `light_blue`, `light_yellow`, `light_magenta`, `light_black`, `light_white`

### **2. Background Colors**
- Standard and light background colors available with `b_` prefix.

### **3. Text Styles**
- `bold`, `dim`, `underline`, `blink`, `reverse`

### **4. Cursor Control**
- `[up]`, `[down]`, `[left]`, `[right]`
- `[delete_line]` (New in v5.0a1!)
- `[down_to_first_character]` or `[dtfc]`

### **5. RGB Support**
Use custom RGB colors:
```python
from colortype import rgbcolor
print(rgbcolor(255, 0, 0) + "Red Text" + "\033[0m")
```

## Usage
```python
from colortype import fore, back, style, goto, console

print(fore.red + "This is red text" + style.reset)
print(back.yellow + "This has a yellow background" + style.reset)
print(style.bold + "This is bold text" + style.reset)
```

Or use `[tags]` with `console()`:
```python
print(console("[red]This is red text[reset]"))
print(console("[b_yellow]Yellow background[reset]"))
```

## Changelog (v5.0a1)
- **New Features:**
  - `[delete_line]` for clearing current line.
  - `[dtfc]` moves down to the first character.
  - `[dim]` text style re-added.
- **Fixes:**
  - `console()` issue resolved.
  - `dim` was missing and now restored.

## Contact
- Email 1: [himnnha23@gmail.com](mailto:himnnha23@gmail.com)
- Email 2: [k.noob1517@gmail.com](mailto:k.noob1517@gmail.com)

_Thank you for using colortype!_