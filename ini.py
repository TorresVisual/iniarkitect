import os
import shutil
import sys
import json
import customtkinter as ctk
from tkinter import messagebox, filedialog
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

        self.title("INI ARKitect 2.5")
        self.geometry("700x600")
        
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

        # Load/Migrate configuration
        self.config_path = Path(os.path.abspath(".")) / "config.json"
        self.dest_dir, self.src_dir = self.initialize_config()
        
        # UI Setup
        self.setup_ui()
        
    def initialize_config(self):
        # Migration from INI if JSON doesn't exist
        ini_path = Path(os.path.abspath(".")) / "config.ini"
        
        # Default fallback values
        default_config = {
            "destination_dir": str(os.path.abspath(".")), # Use current dir as last resort
            "source_dir": str(Path(os.path.abspath(".")) / "inis")
        }

        if not self.config_path.exists():
            if ini_path.exists():
                try:
                    import configparser
                    config_ini = configparser.ConfigParser()
                    config_ini.read(ini_path)
                    data = {
                        "destination_dir": config_ini.get("Settings", "destination_dir", fallback=default_config["destination_dir"]),
                        "source_dir": config_ini.get("Settings", "source_dir", fallback=default_config["source_dir"])
                    }
                    self.save_config_data(data)
                    # Don't delete yet, just in case, or maybe rename it
                    ini_path.rename(ini_path.with_suffix(".ini.old"))
                except Exception as e:
                    print(f"Error migrating INI: {e}")
                    self.save_config_data(default_config)
            else:
                self.save_config_data(default_config)

        # Load and resolve
        return self.load_config_data()

    def load_config_data(self):
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
        except:
            data = {}

        dest = data.get("destination_dir")
        src = data.get("source_dir")
        
        # Base path for relative resolutions
        base_path = Path(os.path.abspath("."))
        
        def resolve_path(p, default_name):
            if not p:
                return base_path / default_name
            
            p_obj = Path(p)
            if p_obj.exists():
                return p_obj.absolute()
            
            # If absolute but doesn't exist, try resolving locally
            if p_obj.is_absolute():
                local_attempt = base_path / p_obj.name
                if local_attempt.exists():
                    return local_attempt.absolute()
                
            # If relative, resolve relative to base
            local_rel = base_path / p
            if local_rel.exists():
                return local_rel.absolute()
                
            return p_obj.absolute()

        return resolve_path(dest, "Config"), resolve_path(src, "inis")

    def save_config_data(self, data):
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=4)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tab View
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))
        
        self.tab_presets = self.tabview.add("Presets")
        self.tab_settings = self.tabview.add("Settings")
        
        self.setup_presets_tab()
        self.setup_settings_tab()

        # Footer / Status
        self.footer_frame = ctk.CTkFrame(self, corner_radius=0, height=30)
        self.footer_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(self.footer_frame, text="Ready", font=ctk.CTkFont(size=11))
        self.status_label.pack(side="left", padx=10)

    def setup_presets_tab(self):
        self.tab_presets.grid_columnconfigure(0, weight=1)
        self.tab_presets.grid_rowconfigure(0, weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_presets, label_text="Available Presets")
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.scroll_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Quick Actions
        self.preset_actions = ctk.CTkFrame(self.tab_presets)
        self.preset_actions.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        ctk.CTkButton(self.preset_actions, text="Refresh", command=self.populate_presets, width=100).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(self.preset_actions, text="Open Source", command=self.open_source, width=120).pack(side="right", padx=5, pady=5)
        ctk.CTkButton(self.preset_actions, text="Open Destination", command=self.open_dest, width=120).pack(side="right", padx=5, pady=5)

        self.populate_presets()

    def setup_settings_tab(self):
        self.tab_settings.grid_columnconfigure(1, weight=1)

        # Labels and Entries
        row = 0
        ctk.CTkLabel(self.tab_settings, text="Destination (ARK Config Path):", font=ctk.CTkFont(weight="bold")).grid(row=row, column=0, columnspan=3, sticky="w", padx=20, pady=(20, 5))
        row += 1
        self.entry_dest = ctk.CTkEntry(self.tab_settings, width=400)
        self.entry_dest.grid(row=row, column=0, columnspan=2, sticky="ew", padx=(20, 10), pady=5)
        self.entry_dest.insert(0, str(self.dest_dir))
        ctk.CTkButton(self.tab_settings, text="Browse", width=80, command=lambda: self.browse_path(self.entry_dest)).grid(row=row, column=2, padx=(0, 20))

        row += 1
        ctk.CTkLabel(self.tab_settings, text="Source (Presets Folder):", font=ctk.CTkFont(weight="bold")).grid(row=row, column=0, columnspan=3, sticky="w", padx=20, pady=(20, 5))
        row += 1
        self.entry_src = ctk.CTkEntry(self.tab_settings, width=400)
        self.entry_src.grid(row=row, column=0, columnspan=2, sticky="ew", padx=(20, 10), pady=5)
        self.entry_src.insert(0, str(self.src_dir))
        ctk.CTkButton(self.tab_settings, text="Browse", width=80, command=lambda: self.browse_path(self.entry_src)).grid(row=row, column=2, padx=(0, 20))

        row += 1
        self.btn_save = ctk.CTkButton(self.tab_settings, text="Save & Reload", command=self.save_settings_gui, fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_save.grid(row=row, column=0, columnspan=3, pady=40)

    def browse_path(self, entry_widget):
        path = filedialog.askdirectory()
        if path:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, path)

    def save_settings_gui(self):
        dest = self.entry_dest.get()
        src = self.entry_src.get()
        
        if not dest or not src:
            messagebox.showerror("Error", "Both paths are required.")
            return

        data = {
            "destination_dir": dest,
            "source_dir": src
        }
        
        try:
            self.save_config_data(data)
            self.dest_dir, self.src_dir = self.load_config_data()
            self.populate_presets()
            self.set_status("Settings saved and reloaded.")
            messagebox.showinfo("Success", "Configuration updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def populate_presets(self):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton): widget.destroy()
            if isinstance(widget, ctk.CTkLabel): widget.destroy()

        if not self.src_dir.exists():
            ctk.CTkLabel(self.scroll_frame, text=f"Source folder not found!\n({self.src_dir})", text_color="#e67e22").grid(row=0, column=0, columnspan=3, pady=20)
            return

        folders = [f for f in os.listdir(self.src_dir) if (self.src_dir / f).is_dir()]
        # Filter for folders that actually contain .ini files
        valid_folders = [f for f in folders if any((self.src_dir / f).glob("*.ini"))]
        valid_folders.sort(key=lambda x: x.lower() != "default")

        if not valid_folders:
            ctk.CTkLabel(self.scroll_frame, text="No valid INI presets found in source folder.").grid(row=0, column=0, columnspan=3, pady=20)
            return

        for idx, folder in enumerate(valid_folders):
            btn = ctk.CTkButton(self.scroll_frame, text=folder, command=lambda f=folder: self.apply_ini(f), height=40)
            btn.grid(row=idx // 3, column=idx % 3, padx=10, pady=10, sticky="nsew")

    def backup_inis(self):
        if not self.dest_dir.exists():
            return False, "Destination folder not found."
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.dest_dir.parent / "Backups" / f"backup_{timestamp}"
        
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            for ini in self.dest_dir.glob("*.ini"):
                shutil.copy2(ini, backup_dir)
            return True, f"Backup created in {backup_dir.name}"
        except Exception as e:
            return False, f"Backup failed: {e}"

    def apply_ini(self, folder_name):
        source_folder = self.src_dir / folder_name
        
        # Step 1: Backup
        success, msg = self.backup_inis()
        if not success:
            if not messagebox.askyesno("Backup Warning", f"Backup failed: {msg}\n\nDo you want to proceed anyway?"):
                return
        else:
            self.set_status(msg)

        # Step 2: Apply
        try:
            count = 0
            for ini in source_folder.glob("*.ini"):
                shutil.copy2(ini, self.dest_dir)
                count += 1
            
            self.set_status(f"Success: Applied {count} items from '{folder_name}'")
            messagebox.showinfo("Success", f"Successfully applied {count} configuration files!")
        except Exception as e:
            self.set_status(f"Error: {e}")
            messagebox.showerror("Error", f"Failed to apply files: {e}")

    def set_status(self, text):
        self.status_label.configure(text=text)

    def open_source(self):
        if self.src_dir.exists(): subprocess.run(['explorer', str(self.src_dir)])
        else: messagebox.showerror("Error", "Source folder does not exist.")

    def open_dest(self):
        if self.dest_dir.exists(): subprocess.run(['explorer', str(self.dest_dir)])
        else: messagebox.showerror("Error", "Destination folder does not exist.")

if __name__ == "__main__":
    app = INIArkitect()
    app.mainloop()
