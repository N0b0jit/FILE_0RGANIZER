"""
File Organizer Ultimate - v3.0
Advanced file organizer with animated UI, duplicate finder, and smart features
Author: N0b0jit
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
import time

class AnimatedButton(tk.Canvas):
    """Animated button with hover effects"""
    def __init__(self, parent, text, command, bg_color, fg_color, **kwargs):
        super().__init__(parent, height=40, highlightthickness=0, **kwargs)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.text = text
        self.command = command
        self.hover = False
        
        self.rect = self.create_rectangle(0, 0, 200, 40, fill=bg_color, outline="", tags="bg")
        self.text_id = self.create_text(100, 20, text=text, fill=fg_color, font=("Segoe UI", 11, "bold"))
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", lambda e: command())
        
    def on_enter(self, e):
        self.hover = True
        self.animate_hover()
        
    def on_leave(self, e):
        self.hover = False
        
    def animate_hover(self):
        if self.hover:
            self.itemconfig(self.rect, fill=self.lighten_color(self.bg_color))
            self.after(50, self.animate_hover)
        else:
            self.itemconfig(self.rect, fill=self.bg_color)
            
    def lighten_color(self, color):
        # Simple color lightening
        return color

class FileOrganizerUltimate:
    """Ultimate File Organizer with advanced features"""
    
    DEFAULT_CATEGORIES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Code': ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php'],
        'Executables': ['.exe', '.msi', '.bat', '.sh'],
        'Others': []
    }
    
    TEMPLATES = {
        'Developer': {
            'Source Code': ['.py', '.js', '.java', '.cpp', '.c', '.h', '.cs'],
            'Web Files': ['.html', '.css', '.scss', '.jsx', '.tsx', '.vue'],
            'Config': ['.json', '.yaml', '.yml', '.xml', '.toml', '.ini'],
            'Documentation': ['.md', '.txt', '.pdf'],
            'Images': ['.png', '.jpg', '.svg', '.ico'],
            'Others': []
        },
        'Photographer': {
            'RAW': ['.raw', '.cr2', '.nef', '.arw', '.dng'],
            'JPEG': ['.jpg', '.jpeg'],
            'PNG': ['.png'],
            'Edited': ['.psd', '.ai', '.xcf'],
            'Videos': ['.mp4', '.mov', '.avi'],
            'Others': []
        },
        'Student': {
            'Assignments': ['.doc', '.docx', '.pdf'],
            'Presentations': ['.ppt', '.pptx'],
            'Spreadsheets': ['.xls', '.xlsx'],
            'Notes': ['.txt', '.md', '.odt'],
            'Research': ['.pdf'],
            'Others': []
        }
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer Ultimate v3.0")
        self.root.geometry("1200x850")
        
        self.source_folder = tk.StringVar()
        self.categories = self.DEFAULT_CATEGORIES.copy()
        self.organize_mode = tk.StringVar(value="category")
        self.file_list = []
        self.duplicates = {}
        self.undo_history = []
        self.theme = "dark"
        
        self.colors = {
            'bg': '#0f0f1e',
            'fg': '#e0e0e0',
            'accent': '#00d4ff',
            'accent2': '#ff006e',
            'success': '#00ff88',
            'card': '#1a1a2e',
            'hover': '#252540'
        }
        
        self.setup_ui()
        self.animate_startup()
        
    def setup_ui(self):
        """Setup animated UI"""
        self.root.configure(bg=self.colors['bg'])
        
        # Header with gradient effect
        header = tk.Canvas(self.root, height=80, bg=self.colors['bg'], highlightthickness=0)
        header.pack(fill=tk.X)
        
        # Animated title
        self.title_text = header.create_text(600, 40, text="⚡ FILE ORGANIZER ULTIMATE",
                                            fill=self.colors['accent'], 
                                            font=("Segoe UI", 24, "bold"))
        
        # Main container
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Controls
        left = tk.Frame(main, bg=self.colors['card'], width=350)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)
        
        self.setup_controls(left)
        
        # Right panel - Preview
        right = tk.Frame(main, bg=self.colors['card'])
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.setup_preview(right)
        
        # Status bar with animation
        self.status_bar = tk.Label(self.root, text="Ready ⚡", bg=self.colors['card'],
                                  fg=self.colors['accent'], font=("Segoe UI", 10),
                                  anchor=tk.W, padx=10)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def setup_controls(self, parent):
        """Setup control panel"""
        tk.Label(parent, text="📁 Folder Selection", bg=self.colors['card'],
                fg=self.colors['fg'], font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        # Folder entry
        folder_frame = tk.Frame(parent, bg=self.colors['card'])
        folder_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Entry(folder_frame, textvariable=self.source_folder, bg=self.colors['bg'],
                fg=self.colors['fg'], font=("Segoe UI", 10), relief=tk.FLAT).pack(fill=tk.X, pady=5)
        
        tk.Button(folder_frame, text="Browse", command=self.browse_folder,
                 bg=self.colors['accent'], fg=self.colors['bg'], relief=tk.FLAT,
                 font=("Segoe UI", 10, "bold"), cursor="hand2").pack(fill=tk.X)
        
        # Templates
        tk.Label(parent, text="🎨 Templates", bg=self.colors['card'],
                fg=self.colors['fg'], font=("Segoe UI", 12, "bold")).pack(pady=(20, 10))
        
        for template in self.TEMPLATES.keys():
            tk.Button(parent, text=template, command=lambda t=template: self.load_template(t),
                     bg=self.colors['hover'], fg=self.colors['fg'], relief=tk.FLAT,
                     font=("Segoe UI", 9), cursor="hand2").pack(fill=tk.X, padx=10, pady=2)
        
        # Actions
        tk.Label(parent, text="⚡ Actions", bg=self.colors['card'],
                fg=self.colors['fg'], font=("Segoe UI", 12, "bold")).pack(pady=(20, 10))
        
        actions = [
            ("🔍 Scan Files", self.scan_folder, self.colors['success']),
            ("🔎 Find Duplicates", self.find_duplicates, self.colors['accent2']),
            ("✨ Organize", self.organize_files, self.colors['accent']),
            ("↶ Undo", self.undo_last, self.colors['accent2'])
        ]
        
        for text, cmd, color in actions:
            tk.Button(parent, text=text, command=cmd, bg=color, fg=self.colors['bg'],
                     relief=tk.FLAT, font=("Segoe UI", 11, "bold"),
                     cursor="hand2", pady=8).pack(fill=tk.X, padx=10, pady=5)
        
        # Progress
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=20)
        
    def setup_preview(self, parent):
        """Setup preview panel"""
        tk.Label(parent, text="📊 File Preview", bg=self.colors['card'],
                fg=self.colors['fg'], font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        # Stats frame
        stats_frame = tk.Frame(parent, bg=self.colors['bg'])
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_labels = {}
        stats = [("Files", "0"), ("Size", "0 B"), ("Duplicates", "0")]
        
        for i, (label, value) in enumerate(stats):
            frame = tk.Frame(stats_frame, bg=self.colors['hover'])
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            tk.Label(frame, text=label, bg=self.colors['hover'], fg=self.colors['fg'],
                    font=("Segoe UI", 9)).pack()
            self.stats_labels[label] = tk.Label(frame, text=value, bg=self.colors['hover'],
                                               fg=self.colors['accent'], font=("Segoe UI", 16, "bold"))
            self.stats_labels[label].pack()
        
        # Tree view
        tree_frame = tk.Frame(parent, bg=self.colors['card'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Size", "Type", "Destination"),
                                show="headings", height=20)
        
        for col in ("Name", "Size", "Type", "Destination"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def animate_startup(self):
        """Startup animation"""
        self.pulse_title()
        
    def pulse_title(self, alpha=0):
        """Pulse animation for title"""
        colors = ['#00d4ff', '#ff006e', '#00ff88']
        color = colors[int(time.time() * 2) % 3]
        try:
            self.root.nametowidget(str(self.title_text))
            self.after_id = self.root.after(500, self.pulse_title)
        except:
            pass
            
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_folder.set(folder)
            self.update_status(f"Selected: {folder}")
            
    def load_template(self, template_name):
        self.categories = self.TEMPLATES[template_name].copy()
        self.update_status(f"Loaded template: {template_name}")
        messagebox.showinfo("Template", f"Loaded {template_name} template!")
        
    def scan_folder(self):
        folder = self.source_folder.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Select a valid folder")
            return
            
        self.progress.start()
        threading.Thread(target=self._scan_thread, args=(folder,), daemon=True).start()
        
    def _scan_thread(self, folder):
        self.file_list = []
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            total_size = 0
            
            for filename in files:
                filepath = os.path.join(folder, filename)
                size = os.path.getsize(filepath)
                ext = Path(filename).suffix.lower()
                dest = self._get_destination(ext)
                
                self.file_list.append({
                    'name': filename,
                    'path': filepath,
                    'size': size,
                    'ext': ext,
                    'dest': dest
                })
                
                total_size += size
                
                self.root.after(0, lambda f=filename, s=size, e=ext, d=dest: 
                              self.tree.insert("", tk.END, values=(f, self._format_size(s), e, d)))
            
            self.root.after(0, lambda: self.stats_labels["Files"].config(text=str(len(files))))
            self.root.after(0, lambda: self.stats_labels["Size"].config(text=self._format_size(total_size)))
            self.root.after(0, lambda: self.update_status(f"Scanned {len(files)} files"))
            
        finally:
            self.root.after(0, self.progress.stop)
            
    def find_duplicates(self):
        if not self.file_list:
            messagebox.showwarning("Warning", "Scan folder first")
            return
            
        self.progress.start()
        threading.Thread(target=self._find_duplicates_thread, daemon=True).start()
        
    def _find_duplicates_thread(self):
        hash_map = defaultdict(list)
        
        for file_info in self.file_list:
            try:
                with open(file_info['path'], 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                    hash_map[file_hash].append(file_info['name'])
            except:
                pass
        
        self.duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}
        dup_count = sum(len(v) - 1 for v in self.duplicates.values())
        
        self.root.after(0, lambda: self.stats_labels["Duplicates"].config(text=str(dup_count)))
        self.root.after(0, lambda: self.update_status(f"Found {dup_count} duplicates"))
        self.root.after(0, self.progress.stop)
        
        if self.duplicates:
            self.root.after(0, self.show_duplicates)
            
    def show_duplicates(self):
        win = tk.Toplevel(self.root)
        win.title("Duplicate Files")
        win.geometry("600x400")
        win.configure(bg=self.colors['bg'])
        
        text = tk.Text(win, bg=self.colors['card'], fg=self.colors['fg'], font=("Consolas", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for files in self.duplicates.values():
            text.insert(tk.END, "Duplicates:\n", "header")
            for f in files:
                text.insert(tk.END, f"  • {f}\n")
            text.insert(tk.END, "\n")
            
        text.tag_config("header", foreground=self.colors['accent'], font=("Segoe UI", 10, "bold"))
        
    def organize_files(self):
        if not self.file_list:
            messagebox.showwarning("Warning", "Scan folder first")
            return
            
        if not messagebox.askyesno("Confirm", f"Organize {len(self.file_list)} files?"):
            return
            
        self.progress.start()
        threading.Thread(target=self._organize_thread, daemon=True).start()
        
    def _organize_thread(self):
        folder = self.source_folder.get()
        moves = []
        
        for file_info in self.file_list:
            dest_folder = os.path.join(folder, file_info['dest'])
            os.makedirs(dest_folder, exist_ok=True)
            
            dest_path = os.path.join(dest_folder, file_info['name'])
            if dest_path != file_info['path']:
                shutil.move(file_info['path'], dest_path)
                moves.append({'from': file_info['path'], 'to': dest_path})
        
        if moves:
            self.undo_history.append(moves)
            
        self.root.after(0, lambda: self.update_status(f"Organized {len(moves)} files"))
        self.root.after(0, self.progress.stop)
        self.root.after(0, lambda: messagebox.showinfo("Success", f"Organized {len(moves)} files!"))
        
    def undo_last(self):
        if not self.undo_history:
            messagebox.showinfo("Info", "Nothing to undo")
            return
            
        moves = self.undo_history.pop()
        for move in reversed(moves):
            if os.path.exists(move['to']):
                shutil.move(move['to'], move['from'])
                
        self.update_status("Undo complete")
        messagebox.showinfo("Success", f"Undone {len(moves)} moves")
        
    def _get_destination(self, ext):
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        return "Others"
        
    def _format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
        
    def update_status(self, text):
        self.status_bar.config(text=f"⚡ {text}")

def main():
    root = tk.Tk()
    app = FileOrganizerUltimate(root)
    root.mainloop()

if __name__ == "__main__":
    main()
