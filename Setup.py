from tkinter import messagebox
from PIL import Image, ImageTk

import os, glob

primary = {
    "0": "#a9181e",  # Pokeball
    "1": "#3b5998",  # Greatball
    "2": "#282424",  # Ultraball
    "3": "#673a8f"   # Masterball
}

secondary = {
    "0": "#f7f7f7",  # Pokeball
    "1": "#a9181e",  # Greatball
    "2": "#f0bc2c",  # Ultraball
    "3": "#9b0f4a"   # Masterball
}

tertiary = {
    "0": "#cccbcb",  # Pokeball
    "1": "#af141a",  # Greatball
    "2": "#a07d1b",  # Ultraball
    "3": "#b30f54"   # Masterball
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
def getLastWindow(path):
    with open(path) as file:
        if os.path.getsize(path) == 0:
            file.write("checklist")
        else:
            for line in file:
                if line == "checklist".lower():
                    lastwindow = "checklist"
                elif line == "dex".lower():
                    lastwindow = "dex"

def setPosition(path):
    with open(path) as file:
        for line in file:
            try:
                position = int(line)
            except ValueError:
                valueErrorFix("position.txt")

        if position not in [1,53,105,157,209,261,313,365,417,469]:
            position = 1

def valueErrorFix(filePath):
    with open(filePath, "w") as file:
        file.write("1")
        position = 1



def checkGames():
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

    [filePaths.append(filePath) for filePath in glob.iglob(pattern)]

    [directories.append(filePath) for filePath in filePaths if str(dex) in filePath]


    return directories[::-1]