import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "includes": ["tkinter"],
    "include_files": ["iniarkitect.ico", "D:\Coding\INIArkitect\inis"],
}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(
    script="ini.py",
    base=base,
)

setup(
    name="INIArkitect",
    version="0.1",
    description="INIArkitect",
    options={"build_exe": build_exe_options},
    executables=[exe]
)
