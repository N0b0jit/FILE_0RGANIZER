# 📁 File Organizer Pro v2.0

A powerful and feature-rich Python desktop application to organize files with an advanced GUI interface. **100% Free - No Login Required!**

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Version](https://img.shields.io/badge/version-2.0-brightgreen.svg)

## ✨ Features

### 🎨 **Beautiful UI/UX**
- Modern dark and light theme with toggle switch
- Tabbed interface for organized workflow
- Responsive design with smooth animations
- Professional color schemes

### 📂 **Smart Organization**
- Organize by **File Type** (Images, Videos, Documents, etc.)
- Organize by **Date Modified** (YYYY-MM format)
- Organize by **File Size** (Small, Medium, Large, Very Large)
- Custom categories with full control

### 🔍 **Advanced Preview**
- Real-time file scanning with progress bar
- Detailed tree view showing file name, type, size, and modified date
- Search/filter functionality to find specific files
- Preview mode to test without moving files

### 📊 **Statistics Dashboard**
- Total file count and size
- Category breakdown with percentages
- Visual progress bars for each category
- Real-time statistics updates

### ✏️ **Batch Rename**
- Add prefix or suffix to multiple files
- Find and replace in file names
- Sequential numbering support
- Live preview before applying changes

### 🔄 **Undo Functionality**
- Undo last organization with one click
- Complete movement history tracking
- Safe file operations

### ⚡ **Performance & Usability**
- Multi-threaded scanning and organizing
- Real-time progress tracking
- Keyboard shortcuts for power users
- Drag & drop folder support
- Settings persistence across sessions

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

**Basic Version:**
```bash
python file_organizer.py
```

**Enhanced Pro Version (Recommended):**
```bash
python file_organizer_pro.py
```

That's it! No additional dependencies required.

## 📖 How to Use

### Main Workflow

1. **Select a Folder** 
   - Click "Browse" or press `Ctrl+O`
   - Or drag & drop a folder into the application

2. **Choose Organization Mode**:
   - **File Type**: Organizes into categories (Images, Videos, Documents, etc.)
   - **Date Modified**: Organizes by modification date (YYYY-MM format)
   - **File Size**: Organizes by file size (Small, Medium, Large, Very Large)

3. **Configure Options**:
   - Enable/disable subfolder creation
   - Toggle preview mode to test without moving files

4. **Scan Folder** 
   - Click "🔍 Scan Folder" or press `Ctrl+S`
   - View all files in the preview table
   - Use search to filter specific files

5. **Review Statistics** 
   - Switch to "📊 Statistics" tab
   - View file distribution and sizes
   - Analyze your folder composition

6. **Organize** 
   - Click "✨ Organize Files" or press `Ctrl+Enter`
   - Watch the progress bar
   - Files are organized instantly!

7. **Undo if Needed**
   - Click "↶ Undo" or press `Ctrl+Z`
   - Reverts the last organization

### Batch Rename

1. Scan a folder first
2. Go to "✏️ Batch Rename" tab
3. Set your rename options:
   - Add prefix/suffix
   - Find and replace text
   - Add sequential numbers
4. Click "👁️ Preview Rename" to see changes
5. Click "✓ Apply Rename" to execute

### Keyboard Shortcuts

- `Ctrl+O` - Browse for folder
- `Ctrl+S` - Scan folder
- `Ctrl+Enter` - Organize files
- `Ctrl+Z` - Undo last action
- `F5` - Refresh statistics

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

- 📥 **Organize messy Downloads folder** - Clean up your downloads in seconds
- 🖼️ **Sort photo collections** - Organize photos by date or type
- 📚 **Arrange document libraries** - Keep documents organized by category
- 💿 **Organize media files** - Sort videos, music, and podcasts
- 🗂️ **Clean up project directories** - Organize code files and assets
- 📦 **Manage backup folders** - Structure backups efficiently
- 🎮 **Game file organization** - Sort mods, saves, and screenshots

## 🛠️ Features in Detail

### Preview Mode ✅
Test the organization without actually moving files. Perfect for:
- Verifying the organization structure
- Checking if files will be categorized correctly
- Ensuring no files will be lost or misplaced

### Smart Duplicate Handling ✅
If a file with the same name exists in the destination:
- Automatically appends a number to the filename
- Preserves both files without overwriting
- Example: `document.pdf` → `document_1.pdf`

### Settings Persistence ✅
Your preferences are automatically saved:
- Last used folder path
- Custom category configurations
- Theme preference
- Organization mode
- Loads automatically on next launch

### Progress Tracking ✅
Real-time feedback during operations:
- Visual progress bar
- Current file being processed
- Percentage completion
- Estimated time remaining

### Undo System ✅
Complete safety with undo functionality:
- Tracks all file movements
- One-click undo of last organization
- Maintains movement history
- Safe file operations

## 🎨 Themes

### Dark Theme (Default)
- Easy on the eyes for long sessions
- Modern catppuccin-inspired color palette
- Perfect for low-light environments

### Light Theme
- Clean and professional
- High contrast for better readability
- Great for bright environments

Toggle between themes with the 🌓 button!

## 🔮 Future Enhancements

Completed features (v2.0):
- ✅ Undo functionality
- ✅ Batch rename files
- ✅ Advanced filtering options
- ✅ Dark/Light theme toggle
- ✅ File search functionality
- ✅ Progress bars and tracking
- ✅ Statistics dashboard
- ✅ Keyboard shortcuts
- ✅ Organize by file size

Planned for future versions:
- [ ] Duplicate file detection by content hash
- [ ] Custom organization rules with regex
- [ ] Scheduled automatic organization
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] Export organization reports (PDF/HTML)
- [ ] File compression for archives
- [ ] Multi-language support
- [ ] Plugin system for custom rules
- [ ] Portable executable (no Python required)

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ by N0b0jit
