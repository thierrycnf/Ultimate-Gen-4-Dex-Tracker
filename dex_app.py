import openpyxl
import Setup


class DexApp:
    def __init__(self):
        self.current_theme = self.load_theme()
        self.last_window = Setup.getLastWindow("lastwindow.txt")

        self.workbook = openpyxl.load_workbook("National Dex Guide 1.xlsx")
        self.sheet = self.workbook.active

        self.main = None
        self.pokemon = []
        self.current_window = None

    def load_theme(self):
        with open("themes.txt", "r") as file:
            theme = file.read().strip()

        return theme if theme in ["0","1","2","3"] else "0"