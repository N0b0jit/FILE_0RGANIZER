# 📁 File Organizer Pro

A powerful and user-friendly Python desktop application to organize files in any folder with a beautiful GUI interface.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## ✨ Features

- 🎨 **Modern Dark-Themed UI** - Beautiful and intuitive interface built with tkinter
- 📂 **Smart Organization** - Organize files by type or date modified
- 🔍 **Preview Mode** - See what will happen before moving files
- 🎯 **Custom Categories** - Fully customizable file type categories
- 📊 **File Preview** - View all files in a detailed tree view before organizing
- 💾 **Settings Persistence** - Remembers your preferences and last used folder
- 🔄 **Duplicate Handling** - Automatically handles duplicate file names
- ⚡ **Multi-threaded** - Smooth UI experience even with large folders

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- tkinter (usually comes with Python)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/N0b0jit/FILE_0RGANIZER.git
cd FILE_0RGANIZER
```

2. Run the application:
```bash
python file_organizer.py
```

That's it! No additional dependencies required.

## 📖 How to Use

1. **Select a Folder** - Click "Browse" to choose the folder you want to organize
2. **Choose Organization Mode**:
   - **File Type**: Organizes files into categories (Images, Videos, Documents, etc.)
   - **Date Modified**: Organizes files by modification date (YYYY-MM format)
3. **Configure Options**:
   - Enable/disable subfolder creation
   - Toggle preview mode to test without moving files
4. **Scan Folder** - Click "🔍 Scan Folder" to preview the organization
5. **Organize** - Click "✨ Organize Files" to execute the organization

## 📋 Default File Categories

- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.ico`, `.webp`, `.tiff`
- **Videos**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`
- **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a`
- **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz`
- **Code**: `.py`, `.java`, `.cpp`, `.c`, `.js`, `.html`, `.css`, `.php`, `.rb`, `.go`, `.rs`
- **Executables**: `.exe`, `.msi`, `.bat`, `.sh`, `.app`, `.deb`, `.rpm`
- **Others**: All other file types

## 🎯 Use Cases

- 📥 Organize messy Downloads folder
- 🖼️ Sort photo collections
- 📚 Arrange document libraries
- 💿 Organize media files
- 🗂️ Clean up project directories
- 📦 Manage backup folders

## 🛠️ Features in Detail

### Preview Mode
Test the organization without actually moving files. Perfect for:
- Verifying the organization structure
- Checking if files will be categorized correctly
- Ensuring no files will be lost or misplaced

### Smart Duplicate Handling
If a file with the same name exists in the destination:
- Automatically appends a number to the filename
- Preserves both files without overwriting
- Example: `document.pdf` → `document_1.pdf`

### Settings Persistence
Your preferences are automatically saved:
- Last used folder path
- Custom category configurations
- Loads automatically on next launch

## 🎨 Screenshots

The application features:
- Clean, modern dark theme
- Color-coded UI elements
- Responsive layout
- Professional typography
- Intuitive controls

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**N0b0jit**
- GitHub: [@N0b0jit](https://github.com/N0b0jit)

## ⭐ Show Your Support

If you find this project useful, please consider giving it a star on GitHub!

## 🔮 Future Enhancements

- [ ] Undo functionality
- [ ] Batch rename files
- [ ] Advanced filtering options
- [ ] Custom folder naming patterns
- [ ] File search functionality
- [ ] Drag and drop support
- [ ] Export organization reports

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ by N0b0jit
