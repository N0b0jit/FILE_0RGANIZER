
"""
File Organizer Ultimate - v3.1 (Refactored)
Advanced file organizer with animated UI, duplicate finder, and smart features
Author: N0b0jit
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
from core_logic import OrganizerCore

class AnimatedButton(tk.Canvas):
    """Animated button with hover effects and smooth transitions"""
    def __init__(self, parent, text, command, bg_color, fg_color, **kwargs):
        super().__init__(parent, height=45, highlightthickness=0, **kwargs)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.text = text
        self.command = command
        self.hover_color = self.adjust_brightness(bg_color, 1.2)
        
        self.rect = self.create_rectangle(0, 0, 400, 45, fill=bg_color, outline="", tags="bg")
        self.text_id = self.create_text(0, 22, text=text, fill=fg_color, font=("Segoe UI", 11, "bold"), anchor="w")
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<Configure>", self.on_resize)
        
    def on_resize(self, event):
        self.coords(self.rect, 0, 0, event.width, 45)
        self.coords(self.text_id, event.width//2, 22)
        self.itemconfig(self.text_id, anchor="center")

    def adjust_brightness(self, hex_color, factor):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(min(255, int(c * factor)) for c in rgb)
        return '#%02x%02x%02x' % new_rgb

    def on_enter(self, e):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor="hand2")
        
    def on_leave(self, e):
        self.itemconfig(self.rect, fill=self.bg_color)
        
    def on_click(self, e):
        self.itemconfig(self.rect, fill=self.adjust_brightness(self.bg_color, 0.8))
        self.after(100, lambda: self.itemconfig(self.rect, fill=self.hover_color))
        self.command()

class FileOrganizerUltimate:
    """Ultimate File Organizer with decoupled core logic"""
    
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
        self.root.title("File Organizer Ultimate v3.1")
        self.root.geometry("1100x800")
        
        self.source_folder = tk.StringVar()
        self.categories = self.DEFAULT_CATEGORIES.copy()
        self.file_list = []
        self.undo_history = []
        
        self.colors = {
            'bg': '#0f172a',
            'fg': '#f8fafc',
            'accent': '#38bdf8',
            'accent2': '#f43f5e',
            'success': '#10b981',
            'card': '#1e293b',
            'hover': '#334155'
        }
        
        self.setup_ui()
        self.pulse_title()
        
    def setup_ui(self):
        self.root.configure(bg=self.colors['bg'])
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['bg'], height=100)
        header.pack(fill=tk.X, pady=20)
        
        self.title_label = tk.Label(header, text="⚡ FILE ORGANIZER ULTIMATE",
                                   bg=self.colors['bg'], fg=self.colors['accent'],
                                   font=("Segoe UI", 28, "bold"))
        self.title_label.pack()
        
        # Main Layout
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Left Panel (Controls)
        left_panel = tk.Frame(main_container, bg=self.colors['card'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        self.setup_controls(left_panel)
        
        # Right Panel (Preview)
        right_panel = tk.Frame(main_container, bg=self.colors['bg'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.setup_preview(right_panel)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready ⚡")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bg=self.colors['card'],
                             fg=self.colors['accent'], font=("Segoe UI", 10),
                             anchor="w", padx=20, pady=5)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def setup_controls(self, parent):
        tk.Label(parent, text="FOLDER", bg=self.colors['card'], fg=self.colors['accent'],
                font=("Segoe UI", 10, "bold")).pack(pady=(20, 5))
        
        entry_frame = tk.Frame(parent, bg=self.colors['hover'], padx=5, pady=5)
        entry_frame.pack(fill=tk.X, padx=15)
        
        tk.Entry(entry_frame, textvariable=self.source_folder, bg=self.colors['hover'],
                fg=self.colors['fg'], font=("Segoe UI", 10), relief=tk.FLAT).pack(fill=tk.X)
        
        AnimatedButton(parent, "Browse Folder", self.browse_folder, 
                      self.colors['hover'], self.colors['fg']).pack(fill=tk.X, padx=15, pady=10)

        tk.Label(parent, text="TEMPLATES", bg=self.colors['card'], fg=self.colors['accent'],
                font=("Segoe UI", 10, "bold")).pack(pady=(20, 5))
        
        for name in self.TEMPLATES.keys():
            AnimatedButton(parent, name, lambda n=name: self.load_template(n),
                          self.colors['card'], self.colors['fg']).pack(fill=tk.X, padx=15, pady=2)

        tk.Label(parent, text="ACTIONS", bg=self.colors['card'], fg=self.colors['accent'],
                font=("Segoe UI", 10, "bold")).pack(pady=(20, 5))
        
        AnimatedButton(parent, "🔍 Scan Files", self.scan_folder, 
                      self.colors['success'], self.colors['bg']).pack(fill=tk.X, padx=15, pady=5)
        
        AnimatedButton(parent, "🔎 Find Duplicates", self.find_duplicates, 
                      self.colors['accent2'], self.colors['bg']).pack(fill=tk.X, padx=15, pady=5)
        
        AnimatedButton(parent, "✨ Organize Now", self.organize_files, 
                      self.colors['accent'], self.colors['bg']).pack(fill=tk.X, padx=15, pady=5)

        self.undo_btn = AnimatedButton(parent, "↶ Undo Last", self.undo_last, 
                                      self.colors['hover'], self.colors['fg'])
        self.undo_btn.pack(fill=tk.X, padx=15, pady=20)

    def setup_preview(self, parent):
        # Stats Cards
        stats_container = tk.Frame(parent, bg=self.colors['bg'])
        stats_container.pack(fill=tk.X, pady=(0, 20))
        
        self.stats = {}
        for label in ["Files", "Total Size", "Duplicates"]:
            card = tk.Frame(stats_container, bg=self.colors['card'], padx=15, pady=10)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            tk.Label(card, text=label.upper(), bg=self.colors['card'], fg=self.colors['accent'],
                    font=("Segoe UI", 9, "bold")).pack()
            
            val = tk.Label(card, text="0", bg=self.colors['card'], fg=self.colors['fg'],
                          font=("Segoe UI", 18, "bold"))
            val.pack()
            self.stats[label] = val

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(parent, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=10)

        # Treeview
        tree_frame = tk.Frame(parent, bg=self.colors['card'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.colors['card'], foreground=self.colors['fg'],
                       fieldbackground=self.colors['card'], borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=self.colors['hover'], foreground=self.colors['accent'],
                       font=("Segoe UI", 10, "bold"), borderwidth=0)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Size", "Type", "Dest"), show="headings")
        self.tree.heading("Name", text="FILE NAME")
        self.tree.heading("Size", text="SIZE")
        self.tree.heading("Type", text="TYPE")
        self.tree.heading("Dest", text="TARGET FOLDER")
        
        self.tree.column("Name", width=300)
        self.tree.column("Size", width=100)
        self.tree.column("Type", width=80)
        self.tree.column("Dest", width=150)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def pulse_title(self):
        current_color = self.title_label.cget("fg")
        next_color = self.colors['accent2'] if current_color == self.colors['accent'] else self.colors['accent']
        self.title_label.config(fg=next_color)
        self.root.after(1000, self.pulse_title)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.source_folder.set(path)
            self.show_status(f"Targeting: {path}")

    def load_template(self, name):
        self.categories = self.TEMPLATES[name].copy()
        messagebox.showinfo("Ultimate", f"Applied '{name}' template successfully!")

    def show_status(self, msg):
        self.status_var.set(f"⚡ {msg}")

    def scan_folder(self):
        folder = self.source_folder.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Invalid directory selected.")
            return
            
        self.progress_var.set(0)
        self.tree.delete(*self.tree.get_children())
        threading.Thread(target=self._scan_thread, args=(folder,), daemon=True).start()

    def _scan_thread(self, folder):
        try:
            self.file_list = []
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            total = len(files)
            total_bytes = 0

            for i, name in enumerate(files):
                path = os.path.join(folder, name)
                size = os.path.getsize(path)
                dest = OrganizerCore.get_destination(name, self.categories)
                
                info = {'name': name, 'path': path, 'size': size, 'dest': dest}
                self.file_list.append(info)
                total_bytes += size
                
                self.root.after(0, lambda f=info: self.tree.insert("", "end", values=(
                    f['name'], OrganizerCore.format_size(f['size']), 
                    os.path.splitext(f['name'])[1], f['dest']
                )))
                
                self.progress_var.set(((i+1)/total)*100)
            
            self.root.after(0, lambda: self.stats["Files"].config(text=str(total)))
            self.root.after(0, lambda: self.stats["Total Size"].config(text=OrganizerCore.format_size(total_bytes)))
            self.show_status(f"Found {total} files.")
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Scan Error", str(e)))

    def find_duplicates(self):
        if not self.file_list:
            messagebox.showwarning("Warning", "Scan a folder first.")
            return
            
        self.show_status("Hashing files (chunked)...")
        self.progress_var.set(0)
        threading.Thread(target=self._dup_thread, daemon=True).start()

    def _dup_thread(self):
        paths = [f['path'] for f in self.file_list]
        
        def update_p(curr, total):
            self.progress_var.set((curr/total)*100)

        dups = OrganizerCore.find_duplicates(paths, progress_callback=update_p)
        count = sum(len(v)-1 for v in dups.values())
        
        self.root.after(0, lambda: self.stats["Duplicates"].config(text=str(count)))
        self.show_status(f"Found {count} duplicate files.")
        
        if count > 0:
            self.root.after(0, lambda: self.show_dup_dialog(dups))

    def show_dup_dialog(self, dups):
        win = tk.Toplevel(self.root)
        win.title("Duplicate Finder Results")
        win.geometry("600x400")
        win.configure(bg=self.colors['bg'])
        
        txt = tk.Text(win, bg=self.colors['card'], fg=self.colors['fg'], font=("Consolas", 10), padx=10, pady=10)
        txt.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for h, paths in dups.items():
            txt.insert("end", f"HASH: {h}\n", "head")
            for p in paths:
                txt.insert("end", f"  • {os.path.basename(p)}\n")
            txt.insert("end", "\n")
            
        txt.tag_config("head", foreground=self.colors['accent'], font=("Consolas", 10, "bold"))

    def organize_files(self):
        if not self.file_list:
            messagebox.showwarning("Warning", "Scan a folder first.")
            return
            
        if not messagebox.askyesno("Confirm", f"Move {len(self.file_list)} files?"):
            return
            
        self.show_status("Organizing...")
        threading.Thread(target=self._org_thread, daemon=True).start()

    def _org_thread(self):
        moves = []
        folder = self.source_folder.get()
        
        for i, info in enumerate(self.file_list):
            dest_dir = os.path.join(folder, info['dest'])
            try:
                new_path, moved = OrganizerCore.safe_move(info['path'], dest_dir)
                if moved:
                    moves.append({'from': info['path'], 'to': new_path})
            except Exception as e:
                print(f"Error {info['name']}: {e}")
            
            self.progress_var.set(((i+1)/len(self.file_list))*100)
            
        if moves:
            self.undo_history.append(moves)
            
        self.show_status(f"Organized {len(moves)} files.")
        self.root.after(0, lambda: messagebox.showinfo("Ultimate", f"Successfully organized {len(moves)} files!"))

    def undo_last(self):
        if not self.undo_history:
            messagebox.showinfo("Undo", "Nothing left to undo.")
            return
            
        moves = self.undo_history.pop()
        for m in reversed(moves):
            if os.path.exists(m['to']):
                os.makedirs(os.path.dirname(m['from']), exist_ok=True)
                os.rename(m['to'], m['from'])
                
        self.show_status(f"Undid {len(moves)} movements.")
        messagebox.showinfo("Undo", "Successfully reverted last operation.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerUltimate(root)
    root.mainloop()
