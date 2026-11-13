from tkinter import messagebox
from theme import Theme
from PIL import Image, ImageTk

import os, glob

primary = {
    Theme.POKEBALL: "#a9181e",  # Pokeball
    Theme.GREATBALL: "#3b5998",  # Greatball
    Theme.ULTRABALL: "#282424",  # Ultraball
    Theme.MASTERBALL: "#673a8f"   # Masterball
}

secondary = {
    Theme.POKEBALL: "#f7f7f7",  # Pokeball
    Theme.GREATBALL: "#a9181e",  # Greatball
    Theme.ULTRABALL: "#f0bc2c",  # Ultraball
    Theme.MASTERBALL: "#9b0f4a"   # Masterball
}

tertiary = {
    Theme.POKEBALL: "#cccbcb",  # Pokeball
    Theme.GREATBALL: "#af141a",  # Greatball
    Theme.ULTRABALL: "#a07d1b",  # Ultraball
    Theme.MASTERBALL: "#b30f54"   # Masterball
}
logos = {
    "d": [None, None, False],
    "p": [None, None, False],
    "pl": [None, None, False],
    "hg": [None, None, False],
    "ss": [None, None, False]
    }

logoButtons = {
    "d": None,
    "p": None,
    "pl": None,
    "hg": None,
    "ss": None
}
def get_last_screen(path):
    with open(path) as file:
        if os.path.getsize(path) == 0:
            file.write("checklist")
        else:
            for line in file:
                if line == "checklist".lower():
                    last_screen = "checklist"
                elif line == "dex".lower():
                    last_screen = "dex"
    return last_screen

def setPosition(path):
    positions = [i for i in range(1, 722, 52)]
    with open(path) as file:
        for line in file:
            try:
                position = int(line)
            except ValueError:
                valueErrorFix("position.txt")

        if position not in positions:
            position = 1
        return position, positions

def valueErrorFix(filePath):
    with open(filePath, "w") as file:
        file.write("1")
        position = 1



def check_games():
    anyTrue = False
    for key, value in logos.items():
        if value[2]:
            anyTrue = True

    if not anyTrue:
        messagebox.showerror("No games!", "You have selected zero games!")
        return False
    else:
        return True

def hasMultipleForms(path, dex):
    directories = []
    filePaths = []
    count = 0

    range = len(str(dex))
    if range < 3:
        return directories

    pattern = f"{path}/*.png"
    print(pattern)

    [filePaths.append(filePath) for filePath in glob.iglob(pattern)]

    [directories.append(filePath) for filePath in filePaths if str(dex) in filePath]


    return directories[::-1]



