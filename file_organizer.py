"""
File Organizer - A GUI application to organize files in any folder
Author: Created with Antigravity AI
Date: 2026-01-23
"""

import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List
import threading

class FileOrganizer:
    """Main File Organizer Application"""
    
    # Default file categories
    DEFAULT_CATEGORIES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp', '.tiff'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
        'Code': ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php', '.rb', '.go', '.rs'],
        'Executables': ['.exe', '.msi', '.bat', '.sh', '.app', '.deb', '.rpm'],
        'Others': []  # Catch-all category
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer Pro")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2e")
        
        # Variables
        self.source_folder = tk.StringVar()
        self.categories = self.DEFAULT_CATEGORIES.copy()
        self.organize_mode = tk.StringVar(value="category")  # category or date
        self.create_subfolders = tk.BooleanVar(value=True)
        self.preview_mode = tk.BooleanVar(value=True)
        self.file_list = []
        
        # Setup UI
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = "#1e1e2e"
        fg_color = "#cdd6f4"
        accent_color = "#89b4fa"
        button_bg = "#313244"
        
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground=accent_color)
        style.configure("TButton", background=button_bg, foreground=fg_color, borderwidth=0, font=("Segoe UI", 10))
        style.map("TButton", background=[("active", accent_color)])
        style.configure("TCheckbutton", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        style.configure("TRadiobutton", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="📁 File Organizer Pro", style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Folder selection frame
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(folder_frame, text="Select Folder:").pack(side=tk.LEFT, padx=(0, 10))
        
        folder_entry = tk.Entry(folder_frame, textvariable=self.source_folder, 
                               bg="#313244", fg=fg_color, font=("Segoe UI", 10),
                               insertbackground=fg_color, relief=tk.FLAT)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(folder_frame, text="Browse", command=self.browse_folder,
                              bg=button_bg, fg=fg_color, font=("Segoe UI", 10),
                              relief=tk.FLAT, cursor="hand2", padx=15, pady=5)
        browse_btn.pack(side=tk.LEFT)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Organization Options", padding="15")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Mode selection
        mode_frame = ttk.Frame(options_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(mode_frame, text="Organize by:").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(mode_frame, text="File Type", variable=self.organize_mode, 
                       value="category").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(mode_frame, text="Date Modified", variable=self.organize_mode, 
                       value="date").pack(side=tk.LEFT)
        
        # Additional options
        ttk.Checkbutton(options_frame, text="Create subfolders for organization", 
                       variable=self.create_subfolders).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Preview mode (don't move files)", 
                       variable=self.preview_mode).pack(anchor=tk.W, pady=2)
        
        # Action buttons frame
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        scan_btn = tk.Button(action_frame, text="🔍 Scan Folder", command=self.scan_folder,
                            bg="#a6e3a1", fg="#1e1e2e", font=("Segoe UI", 11, "bold"),
                            relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        scan_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        organize_btn = tk.Button(action_frame, text="✨ Organize Files", command=self.organize_files,
                                bg=accent_color, fg="#1e1e2e", font=("Segoe UI", 11, "bold"),
                                relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        settings_btn = tk.Button(action_frame, text="⚙️ Categories", command=self.open_category_editor,
                                bg=button_bg, fg=fg_color, font=("Segoe UI", 10),
                                relief=tk.FLAT, cursor="hand2", padx=15, pady=8)
        settings_btn.pack(side=tk.LEFT)
        
        # Results frame with treeview
        results_frame = ttk.LabelFrame(main_frame, text="File Preview", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("File", "Type", "Size", "Destination"),
                                show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.heading("File", text="File Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Destination", text="Destination Folder")
        
        self.tree.column("File", width=250)
        self.tree.column("Type", width=100)
        self.tree.column("Size", width=100)
        self.tree.column("Destination", width=200)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to organize files")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
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
        
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.file_list = []
        self.status_var.set("Scanning folder...")
        
        # Run scan in thread to prevent UI freeze
        thread = threading.Thread(target=self._scan_folder_thread, args=(folder,))
        thread.daemon = True
        thread.start()
        
    def _scan_folder_thread(self, folder):
        """Thread function to scan folder"""
        try:
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            
            for filename in files:
                filepath = os.path.join(folder, filename)
                file_ext = Path(filename).suffix.lower()
                file_size = os.path.getsize(filepath)
                
                # Determine destination
                if self.organize_mode.get() == "category":
                    destination = self._get_category_folder(file_ext)
                else:
                    destination = self._get_date_folder(filepath)
                
                file_info = {
                    'name': filename,
                    'path': filepath,
                    'ext': file_ext,
                    'size': file_size,
                    'destination': destination
                }
                
                self.file_list.append(file_info)
                
                # Update UI in main thread
                self.root.after(0, self._add_tree_item, file_info)
            
            self.root.after(0, lambda: self.status_var.set(f"Found {len(files)} files"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Scan failed: {str(e)}"))
            
    def _add_tree_item(self, file_info):
        """Add item to treeview"""
        size_str = self._format_size(file_info['size'])
        self.tree.insert("", tk.END, values=(
            file_info['name'],
            file_info['ext'] or 'No extension',
            size_str,
            file_info['destination']
        ))
        
    def _get_category_folder(self, extension):
        """Get category folder for file extension"""
        for category, extensions in self.categories.items():
            if extension in extensions:
                return category
        return "Others"
    
    def _get_date_folder(self, filepath):
        """Get date-based folder name"""
        mod_time = os.path.getmtime(filepath)
        date = datetime.fromtimestamp(mod_time)
        return date.strftime("%Y-%m")
    
    def _format_size(self, size):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
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
        
        # Run organization in thread
        thread = threading.Thread(target=self._organize_files_thread)
        thread.daemon = True
        thread.start()
        
    def _organize_files_thread(self):
        """Thread function to organize files"""
        try:
            folder = self.source_folder.get()
            moved_count = 0
            
            for i, file_info in enumerate(self.file_list):
                self.root.after(0, lambda i=i: self.status_var.set(
                    f"Processing {i+1}/{len(self.file_list)}..."))
                
                if self.create_subfolders.get():
                    dest_folder = os.path.join(folder, file_info['destination'])
                else:
                    dest_folder = folder
                
                # Create destination folder if it doesn't exist
                if not self.preview_mode.get():
                    os.makedirs(dest_folder, exist_ok=True)
                    
                    # Move file
                    dest_path = os.path.join(dest_folder, file_info['name'])
                    
                    # Handle duplicate names
                    if os.path.exists(dest_path) and dest_path != file_info['path']:
                        base, ext = os.path.splitext(file_info['name'])
                        counter = 1
                        while os.path.exists(dest_path):
                            dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                            counter += 1
                    
                    # Move the file
                    if dest_path != file_info['path']:
                        shutil.move(file_info['path'], dest_path)
                        moved_count += 1
            
            if self.preview_mode.get():
                self.root.after(0, lambda: messagebox.showinfo("Preview Complete", 
                    f"Preview mode: {len(self.file_list)} files would be organized"))
            else:
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                    f"Successfully organized {moved_count} files!"))
            
            self.root.after(0, lambda: self.status_var.set("Organization complete"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", 
                f"Organization failed: {str(e)}"))
    
    def open_category_editor(self):
        """Open category editor window"""
        editor = tk.Toplevel(self.root)
        editor.title("Edit Categories")
        editor.geometry("600x500")
        editor.configure(bg="#1e1e2e")
        
        main_frame = ttk.Frame(editor, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="File Categories", 
                 font=("Segoe UI", 14, "bold")).pack(pady=(0, 15))
        
        # Category list
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        category_text = tk.Text(list_frame, bg="#313244", fg="#cdd6f4", 
                               font=("Consolas", 10), yscrollcommand=scrollbar.set,
                               relief=tk.FLAT, padx=10, pady=10)
        category_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=category_text.yview)
        
        # Display categories
        for category, extensions in self.categories.items():
            category_text.insert(tk.END, f"{category}:\n", "category")
            category_text.insert(tk.END, f"  {', '.join(extensions)}\n\n")
        
        category_text.tag_config("category", foreground="#89b4fa", font=("Segoe UI", 10, "bold"))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        reset_btn = tk.Button(btn_frame, text="Reset to Default", 
                             command=lambda: self.reset_categories(editor),
                             bg="#f38ba8", fg="#1e1e2e", font=("Segoe UI", 10),
                             relief=tk.FLAT, cursor="hand2", padx=15, pady=5)
        reset_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        close_btn = tk.Button(btn_frame, text="Close", command=editor.destroy,
                             bg="#313244", fg="#cdd6f4", font=("Segoe UI", 10),
                             relief=tk.FLAT, cursor="hand2", padx=15, pady=5)
        close_btn.pack(side=tk.RIGHT)
        
    def reset_categories(self, editor):
        """Reset categories to default"""
        result = messagebox.askyesno("Confirm", "Reset all categories to default?")
        if result:
            self.categories = self.DEFAULT_CATEGORIES.copy()
            self.save_settings()
            editor.destroy()
            messagebox.showinfo("Success", "Categories reset to default")
    
    def save_settings(self):
        """Save settings to file"""
        try:
            settings = {
                'categories': self.categories,
                'last_folder': self.source_folder.get()
            }
            
            settings_path = os.path.join(os.path.dirname(__file__), 'organizer_settings.json')
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")
    
    def load_settings(self):
        """Load settings from file"""
        try:
            settings_path = os.path.join(os.path.dirname(__file__), 'organizer_settings.json')
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    self.categories = settings.get('categories', self.DEFAULT_CATEGORIES)
                    self.source_folder.set(settings.get('last_folder', ''))
        except Exception as e:
            print(f"Failed to load settings: {e}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = FileOrganizer(root)
    
    # Save settings on close
    root.protocol("WM_DELETE_WINDOW", lambda: [app.save_settings(), root.destroy()])
    
    root.mainloop()

if __name__ == "__main__":
    main()
