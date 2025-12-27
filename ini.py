import os
import shutil
import sys
import configparser
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path
import subprocess

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class INIArkitect(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("INI ARKitect")
        self.geometry("600x500")
        
        # Set appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Set icon
        try:
            icon_path = resource_path("iniarkitect.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Warning: failed to load icon: {e}")

        # Load configuration
        self.dest_dir, self.src_dir = self.load_config()
        
        # UI Setup
        self.setup_ui()
        
    def load_config(self):
        config = configparser.ConfigParser()
        # Look for config.ini in the same directory as the script/exe
        config_path = os.path.join(os.path.abspath("."), 'config.ini')
        
        if not os.path.exists(config_path):
            # Fallback to bundled config if not found externally
            config_path = resource_path('config.ini')

        config.read(config_path)
        
        dest = config.get('Settings', 'destination_dir', fallback=None)
        src = config.get('Settings', 'source_dir', fallback=None)
        
        # Final fallbacks if config is missing or incomplete
        if not dest:
            dest = resource_path('Config')
        if not src:
            src = resource_path('inis')
            
        return Path(dest), Path(src)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="INI ARKitect", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=5)
        
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Manage your ARK configurations with ease", font=ctk.CTkFont(size=12))
        self.subtitle_label.pack(pady=(0, 10))

        # Main Content Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Available Presets")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.populate_presets()

        # Footer / Status
        self.footer_frame = ctk.CTkFrame(self, corner_radius=0, height=40)
        self.footer_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(self.footer_frame, text="Ready", font=ctk.CTkFont(size=11))
        self.status_label.pack(side="left", padx=10)

        self.btn_refresh = ctk.CTkButton(self.footer_frame, text="Refresh", command=self.populate_presets, width=60, height=24, font=ctk.CTkFont(size=10))
        self.btn_refresh.pack(side="right", padx=10, pady=5)

        # Action Buttons
        self.actions_frame = ctk.CTkFrame(self, corner_radius=0)
        self.actions_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self.btn_open_src = ctk.CTkButton(self.actions_frame, text="Open Source", command=self.open_source, width=120)
        self.btn_open_src.pack(side="left", padx=10, pady=10)
        
        self.btn_open_dest = ctk.CTkButton(self.actions_frame, text="Open Destination", command=self.open_dest, width=120)
        self.btn_open_dest.pack(side="left", padx=10, pady=10)

    def populate_presets(self):
        # Clear existing buttons
        for widget in self.scroll_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()

        if not self.src_dir.exists():
            ctk.CTkLabel(self.scroll_frame, text="Source directory not found!").grid(row=0, column=0, columnspan=3, pady=20)
            return

        folders = [
            f for f in os.listdir(self.src_dir)
            if (self.src_dir / f).is_dir() and any((self.src_dir / f).glob("*.ini"))
        ]
        folders.sort(key=lambda x: x.lower() != "default")

        for idx, folder in enumerate(folders):
            btn = ctk.CTkButton(
                self.scroll_frame, 
                text=folder, 
                command=lambda f=folder: self.apply_ini(f),
                height=40
            )
            btn.grid(row=idx // 3, column=idx % 3, padx=5, pady=5, sticky="nsew")

    def backup_inis(self):
        if not self.dest_dir.exists():
            return False, "Destination directory does not exist."
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_parent = self.dest_dir.parent / "Backups"
        backup_dir = backup_parent / f"backup_{timestamp}"
        
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            for ini_file in self.dest_dir.glob("*.ini"):
                shutil.copy2(ini_file, backup_dir)
            return True, f"Backup created: {backup_dir.name}"
        except Exception as e:
            return False, f"Backup failed: {e}"

    def apply_ini(self, folder_name):
        source_folder = self.src_dir / folder_name
        
        # Step 1: Backup
        success, msg = self.backup_inis()
        if not success:
            messagebox.showwarning("Backup Warning", f"Proceeding without backup: {msg}")
        else:
            self.set_status(msg)

        # Step 2: Apply
        try:
            count = 0
            for ini_file in source_folder.glob("*.ini"):
                shutil.copy2(ini_file, self.dest_dir)
                count += 1
            
            self.set_status(f"Success: Applied {count} INI files from '{folder_name}'")
            messagebox.showinfo("Success", f"Applied {count} INI files successfully.")
        except Exception as e:
            self.set_status(f"Error applying INI: {e}")
            messagebox.showerror("Error", f"Failed to apply INI:\n{e}")

    def set_status(self, text):
        self.status_label.configure(text=text)

    def open_source(self):
        if self.src_dir.exists():
            subprocess.run(['explorer', str(self.src_dir)])
        else:
            messagebox.showerror("Error", "Source directory does not exist.")

    def open_dest(self):
        if self.dest_dir.exists():
            subprocess.run(['explorer', str(self.dest_dir)])
        else:
            messagebox.showerror("Error", "Destination directory does not exist.")

if __name__ == "__main__":
    app = INIArkitect()
    app.mainloop()

