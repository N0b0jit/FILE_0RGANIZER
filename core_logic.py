
import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class OrganizerCore:
    """Independent logic for file organization and duplicate detection"""
    
    @staticmethod
    def get_file_hash(filepath, chunk_size=8192):
        """Calculate MD5 hash of a file using chunks to support large files."""
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (PermissionError, IOError):
            return None

    @staticmethod
    def format_size(size):
        """Format bytes to human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    @staticmethod
    def get_destination(filename, categories):
        """Determine folder name based on extension and categories."""
        ext = Path(filename).suffix.lower()
        for category, extensions in categories.items():
            if ext in extensions:
                return category
        return "Others"

    @staticmethod
    def find_duplicates(file_paths, progress_callback=None):
        """Find duplicate files based on content hash."""
        hash_map = defaultdict(list)
        total = len(file_paths)
        
        for i, path in enumerate(file_paths):
            f_hash = OrganizerCore.get_file_hash(path)
            if f_hash:
                hash_map[f_hash].append(path)
            
            if progress_callback:
                progress_callback(i + 1, total)
                
        return {k: v for k, v in hash_map.items() if len(v) > 1}

    @staticmethod
    def safe_move(src, dst_dir):
        """Move file with collision handling (e.g., file_1.txt)."""
        try:
            os.makedirs(dst_dir, exist_ok=True)
            filename = os.path.basename(src)
            base, ext = os.path.splitext(filename)
            
            dst_path = os.path.join(dst_dir, filename)
            counter = 1
            
            # Avoid overwriting and avoid moving to the same spot
            if os.path.abspath(src) == os.path.abspath(dst_path):
                return src, False

            while os.path.exists(dst_path):
                dst_path = os.path.join(dst_dir, f"{base}_{counter}{ext}")
                counter += 1
                
            shutil.move(src, dst_path)
            return dst_path, True
        except Exception as e:
            raise RuntimeError(f"Move failed: {e}")
