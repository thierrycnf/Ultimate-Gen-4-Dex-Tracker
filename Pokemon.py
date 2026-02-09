class Pokemon:
    def __init__(self, dex, name, diamond, pearl, platinum, heartgold, soulsilver, caught, icon, grey, back):
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

    def __add__(self, other):
        return self.dex + other.dex