from cx_Freeze import setup, Executable
import py2exe

setup(
    name = "Ultimate Gen 4 Dex Tracker",
    version = "1.0",
    author = "Thierry-Cruz",
    description = "The perfect software to accompany you on your gen 4 living dex!",
    executables = [
        Executable("windows.py",
                   )
    ]

)
