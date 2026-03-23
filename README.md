# 📝 Editx — Notepad Clone v2

A lightweight but feature-rich Notepad clone built with Python (Tkinter).

## ⚙️ Tech Stack
- Python 3
- Tkinter (standard library — no extra dependencies)

## 🚀 Features

### v2.0 (Latest)
- 🌙 Dark mode toggle
- 🔍 Find & Replace with match highlighting
- 🔤 Font selector (family + size, with live preview)
- 🔢 Line numbers panel
- 📊 Live word & character count in status bar
- ↩️ Word wrap (text fits the window, no horizontal scroll)
- ⚠️ Unsaved changes warning on New / Open
- Bold & Italic formatting
- Keyboard shortcuts: `Ctrl+S`, `Ctrl+O`, `Ctrl+N`, `Ctrl+H`, `Ctrl+B`, `Ctrl+I`, `Ctrl+D`

### v1.0
- Create, open, save, and save-as text files
- Simple Tkinter GUI

## 📂 Project Structure
```
Notepad-Clone/
├── textEditor.py   # Main source code
├── .gitignore
└── dist/           # Generated exe (not in repo — see Releases)
```

## ▶️ How to Run (Source Code)

1. Clone the repo:
```bash
git clone https://github.com/iaamhammad/Notepad-Clone.git
cd Notepad-Clone
```

2. Run:
```bash
python textEditor.py
```

No pip installs needed — uses only Python's standard library.

## 🏗️ How to Build the EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed textEditor.py
```

The executable will be inside the `dist/` folder.

## 📥 Download EXE

Download the pre-built `.exe` from the [Releases](https://github.com/iaamhammad/Notepad-Clone/releases) section.

## 👨‍💻 Author
**Hammad Muhammad** — [@iaamhammad](https://github.com/iaamhammad)
