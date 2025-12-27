import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "packages": ["os", "customtkinter", "darkdetect"],
    "include_files": [
        "iniarkitect.ico",
        "inis/",
        "config.json"
    ],
}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(
    script="ini.py",
    base=base,
    icon="iniarkitect.ico"
)

setup(
    name="INIArkitect",
    version="1.0",
    description="Massively improved INI management for ARK",
    options={"build_exe": build_exe_options},
    executables=[exe]
)
