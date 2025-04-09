import os
import shutil
import tkinter as tk
from tkinter import messagebox
import configparser

def load_config():
    # Read config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    destination_dir = config.get('Settings', 'destination_dir')
    source_dir = config.get('Settings', 'source_dir')
    return destination_dir, source_dir

def apply_ini(selected_folder, source_dir, destination_dir):
    source_folder = os.path.join(source_dir, selected_folder)
    if not os.path.exists(source_folder):
        messagebox.showerror("Error", "The selected INI does not exist.")
        return
    for filename in os.listdir(source_folder):
        shutil.copy(os.path.join(source_folder, filename), destination_dir)
    messagebox.showinfo("Success", "INI applied successfully.")

def create_gui():
    root = tk.Tk()
    root.title("INI ARKitect")
    root.iconbitmap("iniarkitect.ico")

    # Set the background color
    root.configure(bg="#333333")

    # Set window size and position
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a frame with padding and rounded corners
    button_frame = tk.Frame(root, bg="#333333", relief="flat")
    button_frame.pack(padx=10, pady=10)

    # Define a function to create styled buttons
    def create_button(folder):
        return tk.Button(button_frame, text=folder, width=12, height=2, font=("Acumin Pro Regular", 12), bg="#555555", fg="white", relief="raised", bd=0, command=lambda: apply_ini(folder))

    # Detect folders containing INI files
    source_dir = r"D:\Coding\INIArkitect\inis"
    folders_with_inis = [folder for folder in os.listdir(source_dir) if any(filename.endswith(".ini") for filename in os.listdir(os.path.join(source_dir, folder)))]

    # Sort the list of folders with "Default" as the first element
    folders_with_inis.sort(key=lambda x: x != "Default")

    # Calculate number of rows and columns based on the number of buttons
    num_buttons = len(folders_with_inis)
    num_columns = 3  # Number of columns you want to have
    num_rows = (num_buttons + num_columns - 1) // num_columns  # Calculate number of rows needed

    # Configure grid layout to expand
    for i in range(num_rows):
        button_frame.grid_rowconfigure(i, weight=1)
    for i in range(num_columns):
        button_frame.grid_columnconfigure(i, weight=1)

    # Create buttons with modern styling
    for idx, folder in enumerate(folders_with_inis):
        button = create_button(folder)
        row = idx // num_columns
        column = idx % num_columns
        button.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")  # Use sticky to fill the cell

    root.mainloop()

if __name__ == "__main__":
    create_gui()
