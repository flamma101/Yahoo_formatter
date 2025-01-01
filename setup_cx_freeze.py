import sys
from cx_Freeze import setup, Executable
import os

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Paths to the downloaded 64-bit Visual C++ Redistributable DLLs
vcruntime_dlls = [
    "vcruntime140.dll",  # Update with the actual path
    "vcruntime140_1.dll"  # Update with the actual path
]

executables = [Executable("src/yahoo_formater_UI.py", base=base)]

setup(
    name="yahoo_formatter_app",
    version="1.0.0",
    description="A GUI application for formatting Yahoo credentials using proxies.",
    executables=executables,
    options={
        "build_exe": {
            "packages": ["tkinter", "requests"],
            "include_files": vcruntime_dlls,
        }
    },
)