import glob
class Pokemon:
    def __init__(self, dex = None, name = None, diamond = None, pearl = None, platinum = None, heartgold = None, soulsilver = None, caught = None, icon = None, grey = None, back = None):
        self.dex = dex
        self.name = name
        self.diamond = diamond
        self.pearl = pearl
        self.platinum = platinum
        self.heartgold = heartgold
        self.soulsilver = soulsilver
        self.caught = caught
        self.icon = icon
        self.grey = grey
        self.back = back
        self.formsDirectory = []
        self.otherBack = []
        self.cry = self.getCry("cries")
        self.getFilterData()

    def __str__(self):
        return f"dex number: {self.dex}\nname: {self.name}\ndiamond: {self.diamond}\npearl: {self.pearl}\nplatinum: {self.platinum}\nheartgold: {self.heartgold}\nsoulsilver: {self.soulsilver}\ncaught?: {self.caught}\nicon: {self.icon}\ngrey: {self.grey}\nback: {self.back}\n"

    def getLocation(self, key):
        if key == "diamond":
            return self.diamond
        elif key == "pearl":
            return self.pearl
        elif key == "platinum":
            return self.platinum
        elif key == "heartgold":
            return self.heartgold
        elif key == "soulsilver":
            return self.soulsilver
        else:
            return "N/A"

    def getCry(self, path):
        pattern = f"{path}/*.wav"

        for filePath in glob.iglob(pattern):
            currentPath = filePath[6:]
            currentPath = currentPath[:-4]
            if str(currentPath) == str(self.dex):
                return filePath
                # print("Equals!")

    def getFilterData(self):
        #self.inDiamond = (self.diamond != "—")

        if self.diamond != '—':
            self.inDiamond = True
        else:
            self.inDiamond = False

        if self.pearl != '—':
            self.inPearl = True
        else:
            self.inPearl = False

        if self.platinum != '—':
            self.inPlatinum = True
        else:
            self.inPlatinum= False

        if self.heartgold != "—":
            self.inHeartGold = True
        else:
            self.inHeartGold= False

        if self.soulsilver != '—':
            self.inSoulSilver = True
        else:
            self.inSoulSilver = False

    def __add__(self, other):
        return self.dex + other.dex