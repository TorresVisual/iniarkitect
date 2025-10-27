import os
import shutil
import sys
import tkinter as tk
from tkinter import messagebox
import configparser

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_config():
    config = configparser.ConfigParser()
    config_path = resource_path('config.ini')
    config.read(config_path)
    # Your fixed destination path
    destination_dir = r"C:\Program Files (x86)\Steam\steamapps\common\ARK\Engine\Config"
    # The bundled or local 'inis' folder
    source_dir = resource_path('inis')
    return destination_dir, source_dir

def apply_ini(selected_folder, source_dir, destination_dir):
    source_folder = os.path.join(source_dir, selected_folder)
    if not os.path.exists(source_folder):
        messagebox.showerror("Error", "The selected INI does not exist.")
        return
    try:
        for filename in os.listdir(source_folder):
            shutil.copy(os.path.join(source_folder, filename), destination_dir)
        messagebox.showinfo("Success", "INI applied successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy files:\n{e}")

def create_gui():
    root = tk.Tk()
    root.title("INI ARKitect")


    # Use iconphoto instead of iconbitmap
    from tkinter import PhotoImage
    icon_path = resource_path("iniarkitect.ico")
    try:
        icon_img = PhotoImage(file=icon_path)
        root.iconphoto(False, icon_img)
    except Exception as e:
        print(f"Warning: failed to load icon: {e}")

    root.configure(bg="#333333")

    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    button_frame = tk.Frame(root, bg="#333333", relief="flat")
    button_frame.pack(padx=10, pady=10, fill="both", expand=True)

    destination_dir, source_dir = load_config()

    def create_button(folder):
        return tk.Button(
            button_frame,
            text=folder,
            width=12,
            height=2,
            font=("Acumin Pro Regular", 12),
            bg="#555555",
            fg="white",
            relief="raised",
            bd=0,
            command=lambda: apply_ini(folder, source_dir, destination_dir)
        )

    # Get all subfolders inside source_dir that contain any .ini files
    folders_with_inis = [
        folder for folder in os.listdir(source_dir)
        if os.path.isdir(os.path.join(source_dir, folder)) and
        any(filename.endswith(".ini") for filename in os.listdir(os.path.join(source_dir, folder)))
    ]

    folders_with_inis.sort(key=lambda x: x != "Default")

    num_buttons = len(folders_with_inis)
    num_columns = 3
    num_rows = (num_buttons + num_columns - 1) // num_columns

    for i in range(num_rows):
        button_frame.grid_rowconfigure(i, weight=1)
    for i in range(num_columns):
        button_frame.grid_columnconfigure(i, weight=1)

    for idx, folder in enumerate(folders_with_inis):
        button = create_button(folder)
        row = idx // num_columns
        column = idx % num_columns
        button.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
