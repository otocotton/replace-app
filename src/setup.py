import sys
from cx_Freeze import setup, Executable

includes = ["PySide.QtCore", "PySide.QtGui", "PySide.QtXml", "chardet", "mainUI"] 

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "",
        version = "",
        options = {"build_exe": {"includes": includes}},
        executables = [Executable("replace-app.py", base=base)])