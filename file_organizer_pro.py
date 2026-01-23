"""
File Organizer Pro - Enhanced Version
A powerful GUI application to organize files with advanced features
Author: N0b0jit
Date: 2026-01-23
Version: 2.0
"""

import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime
import json
import threading
import hashlib
from collections import defaultdict
import re

class FileOrganizerPro:
    """Enhanced File Organizer with advanced features"""
    
    # Default file categories
    DEFAULT_CATEGORIES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp', '.tiff'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
        'Code': ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php', '.rb', '.go', '.rs'],
        'Executables': ['.exe', '.msi', '.bat', '.sh', '.app', '.deb', '.rpm'],
        'Others': []
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer Pro v2.0")
        self.root.geometry("1100x800")
        
        # Variables
        self.source_folder = tk.StringVar()
        self.categories = self.DEFAULT_CATEGORIES.copy()
        self.organize_mode = tk.StringVar(value="category")
        self.create_subfolders = tk.BooleanVar(value=True)
        self.preview_mode = tk.BooleanVar(value=True)
        self.file_list = []
        self.undo_history = []
        self.theme = tk.StringVar(value="dark")
        self.search_var = tk.StringVar()
        
        # Theme colors
        self.themes = {
            'dark': {
                'bg': '#1e1e2e',
                'fg': '#cdd6f4',
                'accent': '#89b4fa',
                'button_bg': '#313244',
                'success': '#a6e3a1',
                'warning': '#f9e2af',
                'error': '#f38ba8'
            },
            'light': {
                'bg': '#eff1f5',
                'fg': '#4c4f69',
                'accent': '#1e66f5',
                'button_bg': '#ccd0da',
                'success': '#40a02b',
                'warning': '#df8e1d',
                'error': '#d20f39'
            }
        }
        
        self.current_theme = self.themes['dark']
        
        # Setup UI
        self.setup_ui()
        self.load_settings()
        self.setup_keyboard_shortcuts()
        
    def setup_ui(self):
        """Setup the enhanced user interface"""
        self.root.configure(bg=self.current_theme['bg'])
        
        # Style configuration
        self.setup_styles()
        
        # Main container with notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.organizer_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        self.rename_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.organizer_tab, text="📁 Organize")
        self.notebook.add(self.stats_tab, text="📊 Statistics")
        self.notebook.add(self.rename_tab, text="✏️ Batch Rename")
        self.notebook.add(self.settings_tab, text="⚙️ Settings")
        
        # Setup each tab
        self.setup_organizer_tab()
        self.setup_stats_tab()
        self.setup_rename_tab()
        self.setup_settings_tab()
        
        # Status bar
        self.setup_status_bar()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        bg = self.current_theme['bg']
        fg = self.current_theme['fg']
        accent = self.current_theme['accent']
        button_bg = self.current_theme['button_bg']
        
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground=accent)
        style.configure("TButton", background=button_bg, foreground=fg, borderwidth=0)
        style.configure("TCheckbutton", background=bg, foreground=fg)
        style.configure("TRadiobutton", background=bg, foreground=fg)
        style.configure("TNotebook", background=bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=button_bg, foreground=fg, padding=[20, 10])
        style.map("TNotebook.Tab", background=[("selected", accent)], foreground=[("selected", bg)])
        style.configure("Treeview", background=button_bg, foreground=fg, fieldbackground=button_bg)
        style.configure("Treeview.Heading", background=accent, foreground=bg, font=("Segoe UI", 10, "bold"))
        
    def setup_organizer_tab(self):
        """Setup the main organizer tab"""
        main_frame = ttk.Frame(self.organizer_tab, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with theme toggle
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(title_frame, text="📁 File Organizer Pro", style="Title.TLabel").pack(side=tk.LEFT)
        
        theme_btn = tk.Button(title_frame, text="🌓 Theme", command=self.toggle_theme,
                             bg=self.current_theme['button_bg'], fg=self.current_theme['fg'],
                             font=("Segoe UI", 10), relief=tk.FLAT, cursor="hand2", padx=15, pady=5)
        theme_btn.pack(side=tk.RIGHT)
        
        # Folder selection with drag & drop hint
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(folder_frame, text="Select Folder:").pack(side=tk.LEFT, padx=(0, 10))
        
        folder_entry = tk.Entry(folder_frame, textvariable=self.source_folder,
                               bg=self.current_theme['button_bg'], fg=self.current_theme['fg'],
                               font=("Segoe UI", 10), insertbackground=self.current_theme['fg'],
                               relief=tk.FLAT)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Enable drag and drop
        folder_entry.drop_target_register(tk.DND_FILES)
        folder_entry.dnd_bind('<<Drop>>', self.drop_folder)
        
        browse_btn = tk.Button(folder_frame, text="Browse", command=self.browse_folder,
                              bg=self.current_theme['button_bg'], fg=self.current_theme['fg'],
                              font=("Segoe UI", 10), relief=tk.FLAT, cursor="hand2", padx=15, pady=5)
        browse_btn.pack(side=tk.LEFT)
        
        # Search bar
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT, padx=(0, 10))
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               bg=self.current_theme['button_bg'], fg=self.current_theme['fg'],
                               font=("Segoe UI", 10), insertbackground=self.current_theme['fg'],
                               relief=tk.FLAT)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind('<KeyRelease>', self.filter_files)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Organization Options", padding="15")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        mode_frame = ttk.Frame(options_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(mode_frame, text="Organize by:").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(mode_frame, text="File Type", variable=self.organize_mode,
                       value="category").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(mode_frame, text="Date Modified", variable=self.organize_mode,
                       value="date").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(mode_frame, text="File Size", variable=self.organize_mode,
                       value="size").pack(side=tk.LEFT)
        
        ttk.Checkbutton(options_frame, text="Create subfolders for organization",
                       variable=self.create_subfolders).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Preview mode (don't move files)",
                       variable=self.preview_mode).pack(anchor=tk.W, pady=2)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        scan_btn = tk.Button(action_frame, text="🔍 Scan Folder (Ctrl+S)", command=self.scan_folder,
                            bg=self.current_theme['success'], fg=self.current_theme['bg'],
                            font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        scan_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        organize_btn = tk.Button(action_frame, text="✨ Organize Files (Ctrl+Enter)", command=self.organize_files,
                                bg=self.current_theme['accent'], fg=self.current_theme['bg'],
                                font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        undo_btn = tk.Button(action_frame, text="↶ Undo (Ctrl+Z)", command=self.undo_last_action,
                            bg=self.current_theme['warning'], fg=self.current_theme['bg'],
                            font=("Segoe UI", 10), relief=tk.FLAT, cursor="hand2", padx=15, pady=8)
        undo_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var,
                                           maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(self.progress_frame, text="")
        self.progress_label.pack()
        
        # Results frame with treeview
        results_frame = ttk.LabelFrame(main_frame, text="File Preview", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(tree_frame, columns=("File", "Type", "Size", "Modified", "Destination"),
                                show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.heading("File", text="File Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Modified", text="Modified")
        self.tree.heading("Destination", text="Destination Folder")
        
        self.tree.column("File", width=250)
        self.tree.column("Type", width=80)
        self.tree.column("Size", width=80)
        self.tree.column("Modified", width=120)
        self.tree.column("Destination", width=180)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
    def setup_stats_tab(self):
        """Setup statistics tab"""
        main_frame = ttk.Frame(self.stats_tab, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="📊 Folder Statistics", style="Title.TLabel").pack(pady=(0, 20))
        
        # Stats display frame
        self.stats_frame = ttk.Frame(main_frame)
        self.stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create stats labels
        self.total_files_label = ttk.Label(self.stats_frame, text="Total Files: 0", font=("Segoe UI", 12))
        self.total_files_label.pack(pady=5)
        
        self.total_size_label = ttk.Label(self.stats_frame, text="Total Size: 0 B", font=("Segoe UI", 12))
        self.total_size_label.pack(pady=5)
        
        # Category breakdown
        ttk.Label(self.stats_frame, text="\nCategory Breakdown:", font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        self.category_frame = ttk.Frame(self.stats_frame)
        self.category_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(main_frame, text="🔄 Refresh Statistics", command=self.update_statistics,
                               bg=self.current_theme['accent'], fg=self.current_theme['bg'],
                               font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        refresh_btn.pack(pady=10)
        
    def setup_rename_tab(self):
        """Setup batch rename tab"""
        main_frame = ttk.Frame(self.rename_tab, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="✏️ Batch Rename Files", style="Title.TLabel").pack(pady=(0, 20))
        
        # Rename options
        options_frame = ttk.LabelFrame(main_frame, text="Rename Options", padding="15")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Prefix
        prefix_frame = ttk.Frame(options_frame)
        prefix_frame.pack(fill=tk.X, pady=5)
        ttk.Label(prefix_frame, text="Add Prefix:").pack(side=tk.LEFT, padx=(0, 10))
        self.prefix_var = tk.StringVar()
        tk.Entry(prefix_frame, textvariable=self.prefix_var, bg=self.current_theme['button_bg'],
                fg=self.current_theme['fg'], font=("Segoe UI", 10), relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Suffix
        suffix_frame = ttk.Frame(options_frame)
        suffix_frame.pack(fill=tk.X, pady=5)
        ttk.Label(suffix_frame, text="Add Suffix:").pack(side=tk.LEFT, padx=(0, 10))
        self.suffix_var = tk.StringVar()
        tk.Entry(suffix_frame, textvariable=self.suffix_var, bg=self.current_theme['button_bg'],
                fg=self.current_theme['fg'], font=("Segoe UI", 10), relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Find and replace
        find_frame = ttk.Frame(options_frame)
        find_frame.pack(fill=tk.X, pady=5)
        ttk.Label(find_frame, text="Find:").pack(side=tk.LEFT, padx=(0, 10))
        self.find_var = tk.StringVar()
        tk.Entry(find_frame, textvariable=self.find_var, bg=self.current_theme['button_bg'],
                fg=self.current_theme['fg'], font=("Segoe UI", 10), relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        replace_frame = ttk.Frame(options_frame)
        replace_frame.pack(fill=tk.X, pady=5)
        ttk.Label(replace_frame, text="Replace:").pack(side=tk.LEFT, padx=(0, 10))
        self.replace_var = tk.StringVar()
        tk.Entry(replace_frame, textvariable=self.replace_var, bg=self.current_theme['button_bg'],
                fg=self.current_theme['fg'], font=("Segoe UI", 10), relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Numbering
        self.add_numbers = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Add sequential numbers", variable=self.add_numbers).pack(anchor=tk.W, pady=5)
        
        # Preview and apply buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        preview_btn = tk.Button(btn_frame, text="👁️ Preview Rename", command=self.preview_rename,
                               bg=self.current_theme['success'], fg=self.current_theme['bg'],
                               font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        apply_btn = tk.Button(btn_frame, text="✓ Apply Rename", command=self.apply_rename,
                             bg=self.current_theme['accent'], fg=self.current_theme['bg'],
                             font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        apply_btn.pack(side=tk.LEFT)
        
        # Preview area
        preview_frame = ttk.LabelFrame(main_frame, text="Rename Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        self.rename_text = tk.Text(preview_frame, bg=self.current_theme['button_bg'],
                                   fg=self.current_theme['fg'], font=("Consolas", 10),
                                   relief=tk.FLAT, padx=10, pady=10)
        self.rename_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_settings_tab(self):
        """Setup settings tab"""
        main_frame = ttk.Frame(self.settings_tab, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="⚙️ Settings & Categories", style="Title.TLabel").pack(pady=(0, 20))
        
        # Category editor
        category_frame = ttk.LabelFrame(main_frame, text="File Categories", padding="15")
        category_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(category_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.category_text = tk.Text(category_frame, bg=self.current_theme['button_bg'],
                                     fg=self.current_theme['fg'], font=("Consolas", 10),
                                     yscrollcommand=scrollbar.set, relief=tk.FLAT, padx=10, pady=10)
        self.category_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.category_text.yview)
        
        self.display_categories()
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        reset_btn = tk.Button(btn_frame, text="Reset to Default", command=self.reset_categories,
                             bg=self.current_theme['error'], fg=self.current_theme['bg'],
                             font=("Segoe UI", 10), relief=tk.FLAT, cursor="hand2", padx=15, pady=5)
        reset_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_btn = tk.Button(btn_frame, text="💾 Save Settings", command=self.save_settings,
                            bg=self.current_theme['success'], fg=self.current_theme['bg'],
                            font=("Segoe UI", 10), relief=tk.FLAT, cursor="hand2", padx=15, pady=5)
        save_btn.pack(side=tk.RIGHT)
        
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_var = tk.StringVar(value="Ready to organize files | Press Ctrl+O to browse folder")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN,
                             anchor=tk.W, bg=self.current_theme['button_bg'],
                             fg=self.current_theme['fg'], font=("Segoe UI", 9))
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-o>', lambda e: self.browse_folder())
        self.root.bind('<Control-s>', lambda e: self.scan_folder())
        self.root.bind('<Control-Return>', lambda e: self.organize_files())
        self.root.bind('<Control-z>', lambda e: self.undo_last_action())
        self.root.bind('<F5>', lambda e: self.update_statistics())
        
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.theme.get() == "dark":
            self.theme.set("light")
            self.current_theme = self.themes['light']
        else:
            self.theme.set("dark")
            self.current_theme = self.themes['dark']
        
        # Recreate UI with new theme
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.notebook = None
        self.setup_ui()
        self.status_var.set("Theme changed successfully")
        
    def drop_folder(self, event):
        """Handle drag and drop folder"""
        folder = event.data.strip('{}')
        if os.path.isdir(folder):
            self.source_folder.set(folder)
            self.status_var.set(f"Dropped folder: {folder}")
        
    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(title="Select Folder to Organize")
        if folder:
            self.source_folder.set(folder)
            self.status_var.set(f"Selected: {folder}")
            
    def scan_folder(self):
        """Scan the selected folder and preview organization"""
        folder = self.source_folder.get()
        
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid folder")
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.file_list = []
        self.progress_var.set(0)
        self.status_var.set("Scanning folder...")
        
        thread = threading.Thread(target=self._scan_folder_thread, args=(folder,))
        thread.daemon = True
        thread.start()
        
    def _scan_folder_thread(self, folder):
        """Thread function to scan folder"""
        try:
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            total = len(files)
            
            for i, filename in enumerate(files):
                filepath = os.path.join(folder, filename)
                file_ext = Path(filename).suffix.lower()
                file_size = os.path.getsize(filepath)
                mod_time = os.path.getmtime(filepath)
                mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M")
                
                destination = self._get_destination_folder(filepath, file_ext, file_size)
                
                file_info = {
                    'name': filename,
                    'path': filepath,
                    'ext': file_ext,
                    'size': file_size,
                    'modified': mod_date,
                    'destination': destination
                }
                
                self.file_list.append(file_info)
                self.root.after(0, self._add_tree_item, file_info)
                
                # Update progress
                progress = ((i + 1) / total) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda i=i, t=total: self.progress_label.config(
                    text=f"Scanning: {i+1}/{t} files"))
            
            self.root.after(0, lambda: self.status_var.set(f"Found {total} files"))
            self.root.after(0, lambda: self.progress_label.config(text="Scan complete!"))
            self.root.after(0, self.update_statistics)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Scan failed: {str(e)}"))
            
    def _get_destination_folder(self, filepath, extension, size):
        """Get destination folder based on organization mode"""
        mode = self.organize_mode.get()
        
        if mode == "category":
            for category, extensions in self.categories.items():
                if extension in extensions:
                    return category
            return "Others"
        elif mode == "date":
            mod_time = os.path.getmtime(filepath)
            date = datetime.fromtimestamp(mod_time)
            return date.strftime("%Y-%m")
        elif mode == "size":
            if size < 1024 * 1024:  # < 1MB
                return "Small (< 1MB)"
            elif size < 10 * 1024 * 1024:  # < 10MB
                return "Medium (1-10MB)"
            elif size < 100 * 1024 * 1024:  # < 100MB
                return "Large (10-100MB)"
            else:
                return "Very Large (> 100MB)"
        
        return "Others"
    
    def _add_tree_item(self, file_info):
        """Add item to treeview"""
        size_str = self._format_size(file_info['size'])
        self.tree.insert("", tk.END, values=(
            file_info['name'],
            file_info['ext'] or 'No ext',
            size_str,
            file_info['modified'],
            file_info['destination']
        ))
        
    def _format_size(self, size):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def filter_files(self, event=None):
        """Filter files based on search query"""
        query = self.search_var.get().lower()
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Re-add filtered items
        for file_info in self.file_list:
            if query in file_info['name'].lower() or query in file_info['ext'].lower():
                self._add_tree_item(file_info)
    
    def organize_files(self):
        """Organize files based on settings"""
        if not self.file_list:
            messagebox.showwarning("Warning", "Please scan a folder first")
            return
        
        if self.preview_mode.get():
            result = messagebox.askyesno("Preview Mode",
                                        "Preview mode is ON. Files will NOT be moved.\n"
                                        "Do you want to continue in preview mode?")
            if not result:
                return
        else:
            result = messagebox.askyesno("Confirm",
                                        f"This will organize {len(self.file_list)} files.\n"
                                        "Do you want to continue?")
            if not result:
                return
        
        thread = threading.Thread(target=self._organize_files_thread)
        thread.daemon = True
        thread.start()
        
    def _organize_files_thread(self):
        """Thread function to organize files"""
        try:
            folder = self.source_folder.get()
            moved_count = 0
            move_history = []
            total = len(self.file_list)
            
            for i, file_info in enumerate(self.file_list):
                self.root.after(0, lambda i=i, t=total: self.status_var.set(
                    f"Processing {i+1}/{t}..."))
                
                progress = ((i + 1) / total) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda i=i, t=total: self.progress_label.config(
                    text=f"Organizing: {i+1}/{t} files"))
                
                if self.create_subfolders.get():
                    dest_folder = os.path.join(folder, file_info['destination'])
                else:
                    dest_folder = folder
                
                if not self.preview_mode.get():
                    os.makedirs(dest_folder, exist_ok=True)
                    
                    dest_path = os.path.join(dest_folder, file_info['name'])
                    
                    if os.path.exists(dest_path) and dest_path != file_info['path']:
                        base, ext = os.path.splitext(file_info['name'])
                        counter = 1
                        while os.path.exists(dest_path):
                            dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                            counter += 1
                    
                    if dest_path != file_info['path']:
                        shutil.move(file_info['path'], dest_path)
                        move_history.append({
                            'from': file_info['path'],
                            'to': dest_path
                        })
                        moved_count += 1
            
            if not self.preview_mode.get() and move_history:
                self.undo_history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'moves': move_history
                })
            
            if self.preview_mode.get():
                self.root.after(0, lambda: messagebox.showinfo("Preview Complete",
                    f"Preview mode: {len(self.file_list)} files would be organized"))
            else:
                self.root.after(0, lambda: messagebox.showinfo("Success",
                    f"Successfully organized {moved_count} files!"))
            
            self.root.after(0, lambda: self.status_var.set("Organization complete"))
            self.root.after(0, lambda: self.progress_label.config(text="Complete!"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error",
                f"Organization failed: {str(e)}"))
    
    def undo_last_action(self):
        """Undo the last organization action"""
        if not self.undo_history:
            messagebox.showinfo("Info", "No actions to undo")
            return
        
        result = messagebox.askyesno("Confirm Undo",
                                    "This will undo the last organization.\n"
                                    "Do you want to continue?")
        if not result:
            return
        
        last_action = self.undo_history.pop()
        
        try:
            for move in reversed(last_action['moves']):
                if os.path.exists(move['to']):
                    shutil.move(move['to'], move['from'])
            
            messagebox.showinfo("Success", f"Undone {len(last_action['moves'])} file movements")
            self.status_var.set("Undo completed successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Undo failed: {str(e)}")
    
    def update_statistics(self):
        """Update statistics display"""
        if not self.file_list:
            return
        
        total_files = len(self.file_list)
        total_size = sum(f['size'] for f in self.file_list)
        
        self.total_files_label.config(text=f"Total Files: {total_files:,}")
        self.total_size_label.config(text=f"Total Size: {self._format_size(total_size)}")
        
        # Category breakdown
        for widget in self.category_frame.winfo_children():
            widget.destroy()
        
        category_counts = defaultdict(int)
        category_sizes = defaultdict(int)
        
        for file_info in self.file_list:
            dest = file_info['destination']
            category_counts[dest] += 1
            category_sizes[dest] += file_info['size']
        
        # Sort by count
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        
        for category, count in sorted_categories:
            size = category_sizes[category]
            percentage = (count / total_files) * 100
            
            frame = ttk.Frame(self.category_frame)
            frame.pack(fill=tk.X, pady=2)
            
            label = ttk.Label(frame, text=f"{category}:", font=("Segoe UI", 10, "bold"))
            label.pack(side=tk.LEFT, padx=(0, 10))
            
            info = ttk.Label(frame,
                           text=f"{count} files ({percentage:.1f}%) - {self._format_size(size)}",
                           font=("Segoe UI", 10))
            info.pack(side=tk.LEFT)
            
            # Simple progress bar
            bar_frame = ttk.Frame(frame)
            bar_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
            
            bar = tk.Canvas(bar_frame, height=15, bg=self.current_theme['button_bg'],
                          highlightthickness=0)
            bar.pack(fill=tk.X)
            
            bar_width = int((percentage / 100) * 200)
            bar.create_rectangle(0, 0, bar_width, 15, fill=self.current_theme['accent'], outline="")
    
    def preview_rename(self):
        """Preview batch rename"""
        if not self.file_list:
            messagebox.showwarning("Warning", "Please scan a folder first")
            return
        
        self.rename_text.delete(1.0, tk.END)
        
        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        find = self.find_var.get()
        replace = self.replace_var.get()
        add_numbers = self.add_numbers.get()
        
        self.rename_text.insert(tk.END, "Old Name → New Name\n")
        self.rename_text.insert(tk.END, "=" * 80 + "\n\n")
        
        for i, file_info in enumerate(self.file_list, 1):
            old_name = file_info['name']
            base, ext = os.path.splitext(old_name)
            
            new_base = base
            
            if find and replace is not None:
                new_base = new_base.replace(find, replace)
            
            if prefix:
                new_base = prefix + new_base
            
            if suffix:
                new_base = new_base + suffix
            
            if add_numbers:
                new_base = f"{new_base}_{i:03d}"
            
            new_name = new_base + ext
            
            self.rename_text.insert(tk.END, f"{old_name}\n  → {new_name}\n\n")
    
    def apply_rename(self):
        """Apply batch rename"""
        if not self.file_list:
            messagebox.showwarning("Warning", "Please scan a folder first")
            return
        
        result = messagebox.askyesno("Confirm",
                                    f"This will rename {len(self.file_list)} files.\n"
                                    "Do you want to continue?")
        if not result:
            return
        
        try:
            prefix = self.prefix_var.get()
            suffix = self.suffix_var.get()
            find = self.find_var.get()
            replace = self.replace_var.get()
            add_numbers = self.add_numbers.get()
            
            renamed_count = 0
            
            for i, file_info in enumerate(self.file_list, 1):
                old_path = file_info['path']
                old_name = file_info['name']
                base, ext = os.path.splitext(old_name)
                
                new_base = base
                
                if find and replace is not None:
                    new_base = new_base.replace(find, replace)
                
                if prefix:
                    new_base = prefix + new_base
                
                if suffix:
                    new_base = new_base + suffix
                
                if add_numbers:
                    new_base = f"{new_base}_{i:03d}"
                
                new_name = new_base + ext
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                
                if old_path != new_path and not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    file_info['name'] = new_name
                    file_info['path'] = new_path
                    renamed_count += 1
            
            messagebox.showinfo("Success", f"Successfully renamed {renamed_count} files!")
            self.scan_folder()  # Refresh the list
            
        except Exception as e:
            messagebox.showerror("Error", f"Rename failed: {str(e)}")
    
    def display_categories(self):
        """Display categories in settings"""
        self.category_text.delete(1.0, tk.END)
        
        for category, extensions in self.categories.items():
            self.category_text.insert(tk.END, f"{category}:\n", "category")
            self.category_text.insert(tk.END, f"  {', '.join(extensions)}\n\n")
        
        self.category_text.tag_config("category", foreground=self.current_theme['accent'],
                                     font=("Segoe UI", 10, "bold"))
    
    def reset_categories(self):
        """Reset categories to default"""
        result = messagebox.askyesno("Confirm", "Reset all categories to default?")
        if result:
            self.categories = self.DEFAULT_CATEGORIES.copy()
            self.display_categories()
            self.save_settings()
            messagebox.showinfo("Success", "Categories reset to default")
    
    def save_settings(self):
        """Save settings to file"""
        try:
            settings = {
                'categories': self.categories,
                'last_folder': self.source_folder.get(),
                'theme': self.theme.get(),
                'organize_mode': self.organize_mode.get(),
                'create_subfolders': self.create_subfolders.get()
            }
            
            settings_path = os.path.join(os.path.dirname(__file__), 'organizer_settings.json')
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=2)
            
            self.status_var.set("Settings saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def load_settings(self):
        """Load settings from file"""
        try:
            settings_path = os.path.join(os.path.dirname(__file__), 'organizer_settings.json')
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    self.categories = settings.get('categories', self.DEFAULT_CATEGORIES)
                    self.source_folder.set(settings.get('last_folder', ''))
                    self.theme.set(settings.get('theme', 'dark'))
                    self.organize_mode.set(settings.get('organize_mode', 'category'))
                    self.create_subfolders.set(settings.get('create_subfolders', True))
        except Exception as e:
            print(f"Failed to load settings: {e}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = FileOrganizerPro(root)
    
    root.protocol("WM_DELETE_WINDOW", lambda: [app.save_settings(), root.destroy()])
    
    root.mainloop()

if __name__ == "__main__":
    main()
