# 📁 File Organizer Ultimate v3.1

A professional, high-performance desktop application to organize messy folders instantly. Built with a stunning animated UI and a powerful multi-threaded engine.

**100% Free • Portable EXE • No Installation Required**

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

---

## 🚀 Why File Organizer Ultimate?

Most file organizers crash on large files or overwrite your documents. **Version 3.1** introduces a decoupled core engine designed for safety and speed.

### ✨ Key Features

- **⚡ Ultimate Performance**: Chunk-based hashing (8KB steps) allows you to scan multi-gigabyte files without high RAM usage.
- **🎨 Premium Animated UI**: Modern "Sky & Slate" dark theme with smooth hover transitions and real-time pulse effects.
- **🔍 Smart Duplicate Detection**: Find identical files by content (MD5), not just by name.
- **🛡️ Collision Shield**: Automatically renames files (e.g., `file_1.txt`) if a name conflict exists in the target folder.
- **🔄 One-Click Undo**: Made a mistake? Revert your entire organization session instantly.
- **📊 Live Dashboard**: Watch your folder composition update in real-time with visual stats cards.

---

## 📦 Getting Started

### 1. Portable EXE (Easiest)
No Python needed. Just download and run.
- Go to the [`dist/`](./dist/) folder.
- Download `FileOrganizerUltimate.exe`.
- Double-click to launch!

### 2. Run from Source
If you are a developer and want to customize the tool:
```bash
# Clone the repo
git clone https://github.com/N0b0jit/FILE_0RGANIZER.git

# Run the ultimate version
python file_organizer_ultimate.py
```

---

## 🛠️ Project Structure

- `file_organizer_ultimate.py`: The main GUI application.
- `core_logic.py`: The standalone engine handle hashing and file movements.
- `file_organizer_pro.py`: Classic version with light/dark theme toggle.
- `dist/`: Contains the standalone Windows executable.

---

## 📖 How to Use

1. **Select Folder**: Choose the messy directory you want to clean.
2. **Apply Template**: Choose from presets like "Developer", "Photographer", or "Student".
3. **Scan**: Click the Scan button to see a preview of how files will be moved.
4. **Organize**: Hit "Organize Now" to execute. 
5. **Clean Duplicates**: Use the duplicate finder to identify redundant copies taking up space.

---

## 📞 Support & Contribution

Found a bug or have a feature request? Open an issue! 

Made with ❤️ by [N0b0jit](https://github.com/N0b0jit)
