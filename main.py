import openpyxl, Pokemon
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
from customtkinter import *

#Day 1 of programming the Ultimate Gen 4 Dex Tracker (man that's a total mouthful)
#hopefully my code is organised lmao

#pokeball is 0
#greatball is 1
#ultraball is 2
global logos, intro, settings, dexEntry, logoButtons, currentTheme, labels, images, ctkWidgets, tkButtons, position
labels, images, ctkButtons, tkButtons, ctkEntries = set(), set(), set(), set(), set()
lastwindow = "checklist"
wbObj = openpyxl.load_workbook("National Dex Guide 1.xlsx")
sheetObj = wbObj.active

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
logoButtons = {
    "d": None,
    "p": None,
    "pl": None,
    "hg": None,
    "ss": None
}


#dsFont = font.Font(family = "Pokemon DS", size = 20)
if os.path.getsize("themes.txt") == 0:
    with open("themes.txt", "w") as file:
        file.write("0")


#opening the text file in read mode to get the contents of the file in the variable currentTheme
with open("themes.txt", "r") as file:
    for line in file:
        #print(line)
        currentTheme = line.strip()

#opening the text file in write mode if the contents of the file is not 0, 1 or 2
if currentTheme not in ["0", "1", "2", "3"]:
    with open("themes.txt", "w") as file:
        file.write("0")
        currentTheme = "0"

#shiiiiiit I hope this code isn't too messy lmao
def grey(game):
    global logos, logoButtons
    #print(game)
    if logos[game][2]:
        logoButtons[game].config(image=logos[game][1])
        logos[game][2] = False
    else:
        logos[game][2] = True
        logoButtons[game].config(image=logos[game][0])



def changeTheme():
    global main, settings, dexEntry, labels, images, ctkButtons, settings, settingsButton, settingsDict, currentTheme, logoButtons, leftArrowButton, rightArrowButton, upArrowButton, downArrowButton, leftArrows, rightArrows, downArrows, upArrows, tkButtons, ctkEntries, images
    #settings.configure(fg_color=primary[currentTheme])
    main.configure(fg_color=primary[currentTheme])
    settings.configure(fg_color = primary[currentTheme])

    for i in range(494):
        try:
            if dexEntry[i]:
                dexEntry[i].configure(fg_color = primary[currentTheme])


        except TclError:
            pass
    #print("leftArrows: ", leftArrows)
    #print(labels)


    settingsButton.configure(image=settingsDict[currentTheme], bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)


    if lastwindow == "checklist":
        try:
            rightArrowButton.configure(image=rightArrows[currentTheme], bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)
        except TclError:
            pass
    else:
        try:
            leftArrowButton.configure(image=leftArrows[currentTheme], bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)
        except TclError:
            pass

    try:
        upArrowButton.configure(image=upArrows[currentTheme], bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)
        downArrowButton.configure(image=downArrows[currentTheme], bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)
    except AttributeError:
        pass

    #leftArrowButton.configure(image=leftArrows[currentTheme], bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)
    #print(ctkButtons)
    for label in labels:
        #print(label)
        try:
            label.configure(bg = primary[currentTheme], fg = secondary[currentTheme])
        except TclError:
            continue
    for button in ctkButtons:
        try:
            button.configure(bg_color = primary[currentTheme], fg_color = secondary[currentTheme], hover_color = tertiary[currentTheme])
        except TclError:
            continue

    for entry in ctkEntries:
        try:
            entry.configure(bg_color = primary[currentTheme], fg_color = secondary[currentTheme])
        except TclError:
            continue
    for button in tkButtons:
        try:
            button.configure(bg = primary[currentTheme], fg = secondary[currentTheme], activebackground=primary[currentTheme])
        except TclError:
            continue

    for key, value in logoButtons.items():
        value.configure(bg=primary[currentTheme],activebackground=primary[currentTheme])

    #print(currentTheme)
    #settings.configure(image = settingsDict[currentTheme], bg = primary[currentTheme], activebackground = primary[currentTheme], highlightthickness=0, borderwidth = 0)




def settingsWindow():
    global logos, main, settings, logoButtons, labels, images, ctkButtons


    if settings is None or not settings.winfo_exists():
        settings = ctk.CTkToplevel(main)
        settings.title("Settings")
        settings.geometry(("300x200"))
        settings.configure(fg_color=primary[currentTheme])
        settings.resizable(False, False)
        settings.iconbitmap(f"ico files\{1}.ico")

    with open ("games.txt") as file:
        for (key, value), line in zip(logos.items(), file):
            if "True" in line:
                value[2] = True
            else:
                value[2] = False
            #logoButtons[key]



        def confirm():
            global currentTheme
            if checkGames():
                theme = comboBox.get()
                if theme == "Pokeball":
                    currentTheme = "0"
                elif theme == "Greatball":
                    currentTheme = "1"
                elif theme == "Ultraball":
                    currentTheme = "2"
                elif theme == "Masterball":
                    currentTheme = "3"

                with open("themes.txt", "w") as file:
                    file.write(str(currentTheme))

                with open("games.txt", "w") as file:

                    for key, value in logos.items():
                        if value[2]:
                            file.write(f"{key} True\n")
                            # print("hello")
                        else:
                            file.write(f"{key} False\n")

                messagebox.showinfo("Confirmed!", "Changes have been confirmed!")
            else:
                return
            #main.destroy()
            #newMain = mainWindow()
            #newMain.mainloop()

            changeTheme()


        themeLabel = tk.Label(settings, text = "Theme", font = ("Pokémon DS Font", 20), bg = primary[currentTheme], fg = secondary[currentTheme] )
        themeLabel.place(relx = .5, rely = .05, anchor = "center")

        comboBox = ctk.CTkComboBox(settings, values = ["Pokeball", "Greatball", "Ultraball", "Masterball"])
        comboBox.place(relx = .5, rely = .2, anchor = "center")

        gameLabel = tk.Label(settings, text = "Games", font = ("Pokémon DS Font", 20), bg = primary[currentTheme], fg = secondary[currentTheme])
        gameLabel.place(relx = .5, rely = .4, anchor = "center")

        confirmButton = ctk.CTkButton(settings, command = confirm, text = "Confirm", font=("Pokémon DS Font", 25), bg_color = primary[currentTheme], fg_color = secondary[currentTheme], hover_color = tertiary[currentTheme], text_color = "black")
        confirmButton.place(relx = .5, rely = .85, anchor = "center")


        x = .15
        y = .5
        for key, value in logos.items():
            if value[2]:
                logoButtons[key] = tk.Button(settings, image=value[0], borderwidth=0, bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, command=lambda k=key: grey(k))
            else:
                logoButtons[key] = tk.Button(settings, image=value[1], borderwidth=0, bg=primary[currentTheme],activebackground=primary[currentTheme], highlightthickness=0,command=lambda k=key: grey(k))
            logoButtons[key].place(relx=x, rely=y)
            # print(key)
            x += .14


        labels.add(themeLabel)
        labels.add(gameLabel)

        ctkButtons.add(confirmButton)
        settings.mainloop()
        images.add("settings")
def introWindow():
    global logos, intro, logoButtons
    intro = ctk.CTk()
    intro.title("Ultimate Gen 4 Dex Tracker")
    intro.geometry("500x250")
    intro.configure(fg_color=primary[currentTheme])

    #index 0 is for the regular icon, index 1 is for the grey icon and index 2 is the boolean where False
    #means that the user doesn't have the game and True is where the user has it

    # opening this text file to check what games the user has
    #with open("games.txt") as file:

    for key, value in logos.items():
        originalImage = Image.open(f"{key}.png")
        originalImage2 = Image.open(f"{key} grey.png")
        resizedImage = originalImage.resize((50, 50), Image.Resampling.LANCZOS)
        resizedImage2 = originalImage2.resize((50, 50), Image.Resampling.LANCZOS)
        logos[key][0] = ImageTk.PhotoImage(resizedImage)
        logos[key][1] = ImageTk.PhotoImage(resizedImage2)


    #functions to make them grey and stuff


    #function to write True/False state of pokemon games to the data file
    def confirm():
        if checkGames():
            with open("games.txt", "w") as file:

                for key, value in logos.items():
                    if value[2]:
                        file.write(f"{key} True\n")
                        #print("hello")
                    else:
                        file.write(f"{key} False\n")

                mainWindow()
        else:
            return


    #widgets
    title = tk.Label(intro, text = "Ultimate Gen 4 Dex Tracker", font = ("Pokémon DS Font", 30), bg = primary[currentTheme], fg = secondary[currentTheme])
    title.place(relx = .5, rely = .1, anchor = "center")

    please = tk.Label(intro, text = "Please select your games", font = ("Pokémon DS Font", 20), bg = primary[currentTheme], fg = secondary[currentTheme])
    please.place(relx = .5, rely = .25, anchor = "center")

    change = tk.Label(intro, text="(You can change these later)", font=("Pokémon DS Font", 15), bg=primary[currentTheme],fg=secondary[currentTheme])
    change.place(relx=.5, rely=.4, anchor="center")

    confirmb = ctk.CTkButton(master = intro, command = confirm, text = "Confirm", font=("Pokémon DS Font", 25), bg_color = primary[currentTheme], fg_color = secondary[currentTheme], hover_color = tertiary[currentTheme], text_color = "black")
    confirmb.place(relx = .5, rely = .9, anchor = "center")

    #testImage = tk.Button(image = logos["pl"][0], borderwidth = 0, bg = primary[currentTheme], activebackground= primary[currentTheme], highlightthickness=0, command = lambda: grey(key))
    #testImage.place(relx = .5, rely = .6, anchor = "center")

    #for loop to optimise place the game logos

    x = .25
    y = .6
    for key, value in logos.items():
        logoButtons[key] = tk.Button(intro, image = value[1], borderwidth = 0, bg = primary[currentTheme], activebackground= primary[currentTheme], highlightthickness=0, command = lambda k=key: grey(k))
        logoButtons[key].place(relx = x, rely = y)
        #print(key)
        x += .1




    #logoButtons["p"].place(relx = .5, y = .6)



    intro.mainloop()

def mainWindow():
    global logos, main, images, labels, ctkButtons, settingsDict, settingsButton, leftArrows, rightArrows, upArrows, downArrows, checklistWidgets, dexWidgets, leftArrowButton, rightArrowButton,  downArrowButton, upArrowButton, ctkEntries, pokemon, currentWindow
    settingsDict, leftArrows, rightArrows, upArrows, downArrows = {}, {}, {}, {}, {}
    upArrowButton, downArrowButton = None, None
    currentWindow = None



    if intro:
        intro.destroy()


    main = ctk.CTk()



    screenWidth, screenHeight = main.winfo_screenwidth(), main.winfo_screenheight() # your resolutiom


    baseWidth, baseHeight = 1920, 1080 # the resolution of me (the creator's) display
    baseWindowWidth, baseWindowHeight = 500, 250 # the base resolution of this window on a 1920x1080 display

    width, height = int(screenWidth/baseWidth*baseWindowWidth), int(screenHeight/baseHeight*baseWindowHeight)

    #print(f"{screenWidth}/{baseWidth}={screenWidth/baseWidth}")
    main.title("Ultimate Gen 4 Dex Tracker")
    #main.geometry(f"{width}x{height}") # ensure that it is relative across devices
    main.geometry(f"{500}x{250}")
    main.tk.call("tk", "scaling", 2.0)
    main.resizable(width = True, height = True)
    main.configure(fg_color=primary[currentTheme])
    #main.iconphoto(False, tk.PhotoImage(file = "hg.png"))
    main.iconbitmap(f"ico files\{1}.ico")

    for setting in range(len(primary)):
        originalImage = Image.open(f"settings\{setting}.png")
        resizedImage = originalImage.resize((50, 50), Image.Resampling.LANCZOS)
        settingsDict[str(setting)] = ImageTk.PhotoImage(resizedImage)

    for rightArrow in range(len(primary)):
        originalImage = Image.open(f"right\{rightArrow}.png")
        resizedImage = originalImage.resize((60, 45), Image.Resampling.LANCZOS)
        rightArrows[str(rightArrow)] = ImageTk.PhotoImage(resizedImage)

    for leftArrow in range(len(primary)):
        originalImage = Image.open(f"left\{leftArrow}.png")
        resizedImage = originalImage.resize((60, 45), Image.Resampling.LANCZOS)
        leftArrows[str(leftArrow)] = ImageTk.PhotoImage(resizedImage)  #

    for downArrow in range(len(primary)):
        originalImage = Image.open(f"down\{downArrow}.png")
        resizedImage = originalImage.resize((50, 45), Image.Resampling.LANCZOS)
        downArrows[str(downArrow)] = ImageTk.PhotoImage(resizedImage)

    for upArrow in range(len(primary)):
        originalImage = Image.open(f"up\{upArrow}.png")
        resizedImage = originalImage.resize((50, 45), Image.Resampling.LANCZOS)
        upArrows[str(upArrow)] = ImageTk.PhotoImage(resizedImage)

    images.add("left")
    images.add("right")
    images.add("up")
    images.add("down")

    #getting logos
    for key, value in logos.items():
        originalImage = Image.open(f"{key}.png")
        originalImage2 = Image.open(f"{key} grey.png")
        resizedImage = originalImage.resize((50, 50), Image.Resampling.LANCZOS)
        resizedImage2 = originalImage2.resize((50, 50), Image.Resampling.LANCZOS)
        logos[key][0] = ImageTk.PhotoImage(resizedImage)
        logos[key][1] = ImageTk.PhotoImage(resizedImage2)



    names, d, p, pl, hg, ss, caught = [sheetObj.cell(row, 2).value for row in range(5, 498)], [sheetObj.cell(row, 3).value for row in range(5, 498)], [sheetObj.cell(row, 4).value for row in range(5, 498)], [sheetObj.cell(row, 5).value for row in range(5, 498)], [sheetObj.cell(row, 6).value for row in range(5, 498)], [sheetObj.cell(row, 7).value for row in range(5, 498)], [sheetObj.cell(row, 9).value for row in range(5, 498)]
    names, d, p, pl, hg, ss, caught = [None]+names, [None]+d, [None]+p, [None]+pl, [None]+hg, [None]+ss, [None]+caught
    #print(ss)
    #getting the pokemon sprites
    pokemon = [None] #element at index 0 has to be None because pokedex starts at 1
    for dex in range(1, 494):
        originalImage = Image.open(f"icons\{dex}.png")
        originalGreyImage = Image.open(f"grey icons\{dex}.png")
        originalBackImage = Image.open(f"back sprites\{dex}.png")

        resizedImage = originalImage.resize((40, 40), Image.Resampling.LANCZOS)
        resizedGreyImage = originalGreyImage.resize((40, 40), Image.Resampling.LANCZOS)
        resizedBackImage = originalBackImage.resize((100, 90), Image.Resampling.LANCZOS)

        pokemon.append({"dex":dex,
                        "name":names[dex],
                        "diamond":d[dex],
                        "pearl":p[dex],
                        "platinum":pl[dex],
                        "heartgold":hg[dex],
                        "soulsilver":ss[dex],
                        "caught":caught[dex],
                        "icon":ImageTk.PhotoImage(resizedImage),
                        "grey":ImageTk.PhotoImage(resizedGreyImage),
                        "back":ImageTk.PhotoImage(resizedBackImage)}
                       )




        #indexes
        #0 - dex No
        #1 - name
        #2 - Diamond location
        #3 - Pearl Location
        #4 = Platinum location
        #5 - HeartGold location
        #6 - SoulSilver location
        #7 - Caught?
        #8 - Icon
        #9 - Grey Icon
        #10 - Back Sprite
        #im gonna have to switch this into a list of dictionaries cause this just kinda sucks doesn't it



    #testSprite = tk.Button(image = pokemon[251], bg = primary[currentTheme], activebackground= primary[currentTheme], highlightthickness=0, borderwidth = 0)
    #testSprite.place(relx = .5, rely = .5, anchor = "center")

    checklistWidgets, dexWidgets = set(), set()

    def switch(screen):
        if screen == "dex":
            delete(screen)
            dex(main)
        else:
            delete(screen)
            checklist(main)

    def delete(window):
        if window == "dex":
            # print(checklistWidgets)
            for widget in checklistWidgets:
                widget.destroy()
        else:
            for widget in dexWidgets:
                widget.destroy()

    def checklist(root):
        global checklistWidgets, labels, settingsButton, rightArrowButton, leftArrowButton, upArrowButton, downArrowButton, settingsDict, leftArrows, rightArrows, upArrows, downArrows, tkButtons, pokemonButtons, position, destroyedUp, destroyedDown, currentPokemon, testPosition, lastwindow, checklistLabel, currentWindow
        currentWindow = "checklist"

        checklistLabel = tk.Label(main, text = "Ultimate Checklist", font = ("Pokémon DS Font", 30), bg = primary[currentTheme], fg = secondary[currentTheme])
        checklistLabel.place(relx = .5, rely = .1, anchor = "center")

        settingsButton = tk.Button(main, command = settingsWindow, image = settingsDict[currentTheme], bg = primary[currentTheme], activebackground = primary[currentTheme], highlightthickness=0, borderwidth = 0 )
        settingsButton.place(relx = .02, rely = .03, anchor = "nw")

        rightArrowButton = tk.Button(main, image = rightArrows[currentTheme], command = lambda w = "dex": switch(w), bg = primary[currentTheme], activebackground = primary[currentTheme], highlightthickness=0, borderwidth = 0 )
        rightArrowButton.place(relx = .9, rely = .1, anchor = "e")

        #print(upArrows)
        def scrollUp():
            global position, pokemonButtons, destroyedUp, destroyedDown, testPosition

            if position - 52 < 0:
                return
            position -= 52
            #testPosition.configure(text=position)

            if position <= 1:
                #print("yooo")
                upArrowButton.place_forget()
                destroyedUp = True

            with open("position.txt", "w") as file:
                file.write(str(position))
            #print("destroyedUp: ", destroyedUp)
            if destroyedDown:
                #print("hi")
                downArrowButton.place(relx=.99, rely=.7, anchor="e")
                destroyedDown = False

            displayMons()

        def scrollDown():
            global position, pokemonButtons, destroyedUp, destroyedDown, testPosition
            if position + 52 > 493:
                return
            position += 52
            #testPosition.configure(text = position)

            if position + 52 >= 493:
                downArrowButton.place_forget()
                destroyedDown = True

            with open("position.txt", "w") as file:
                file.write(str(position))

            #print("destroyedDown: ", destroyedDown)
            if destroyedUp:
                #print("hi")
                upArrowButton.place(relx=.99, rely=.4, anchor="e")
                destroyedUp = False

            displayMons()

        def displayMons():
            global position, pokemonButtons, currentPokemon
            try:
                [mon.destroy() for mon in currentPokemon]
                currentPokemon = []
                #print("test")
            except AttributeError:
                pass
            x, y = .1, .2
             #we're supposed to get this from a data file but this will do
            for i in range(position,494):
                try:
                    if pokemon[i]["caught"]:
                        pokemonButtons[i] = tk.Button(main, command = lambda dex = i: tick(dex), image = pokemon[i]["icon"], bg = primary[currentTheme], activebackground = primary[currentTheme], highlightthickness=0, borderwidth = 0)
                    else:
                        pokemonButtons[i] = tk.Button(main, command = lambda dex = i: tick(dex), image=pokemon[i]["grey"], bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)
                    currentPokemon.append(pokemonButtons[i])
                except TclError:
                    continue

                checklistWidgets.add(pokemonButtons[i])
                tkButtons.add(pokemonButtons[i])
                pokemonButtons[i].place(relx = x, rely = y)
                x += .06
                if x > .85:
                    x = .1
                    y += .2

                if y > .8:
                    break
        pokemonButtons = [None for _ in range(494)]
        currentPokemon = []
        print(position)
        #position = 1

        #testPosition = tk.Label(main, text = position, font = ("Pokémon DS Font", 25), bg = primary[currentTheme], fg = secondary[currentTheme])
        #testPosition.place(relx = .04, rely = .5)


        upArrowButton = tk.Button(main, image = upArrows[currentTheme], command = scrollUp, bg = primary[currentTheme], activebackground = primary[currentTheme], highlightthickness=0, borderwidth = 0 )
        downArrowButton = tk.Button(main, image=downArrows[currentTheme], command= scrollDown, bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)

        destroyedUp, destroyedDown = False, False

        if position-52 > 0:
            #print("hi")
            upArrowButton.place(relx = .99, rely = .4, anchor = "e")
        else:
            destroyedUp = True

        if position+52 < 493:
            downArrowButton.place(relx=.99, rely=.7, anchor="e")
        else:
            destroyedDown = True

        print(position)

        def scroll_up(event):
            scrollUp()

        def scroll_down(event):
            scrollDown()


        main.bind("<MouseWheel>", lambda e: scroll_up(e) if e.delta > 0 else scroll_down(e))
        displayMons()

        labels.add(checklistLabel)

        checklistWidgets.add(checklistLabel)
        checklistWidgets.add(settingsButton)
        checklistWidgets.add(rightArrowButton)
        def tick(dex):
            try: #checking if the spreadsheet is open and if it is, give an error message
                wbObj.save("National Dex Guide 1.xlsx")

            except PermissionError:
                messagebox.showerror("Error!", "You must close National Dex Guide 1.xlsx")
                return False

            pokemon[dex]["caught"] = not pokemon[dex]["caught"] #inverting the boolean
            image = pokemon[dex]["icon"] if pokemon[dex]["caught"] else pokemon[dex]["grey"]

            pokemonButtons[dex].configure(image= image) #changing image to corresponding boolean
            cell = sheetObj.cell(row = dex+4, column = 9) #getting the correct cell for the current pokemon
            cell.value = pokemon[dex]["caught"] #actually modifying the cell

            wbObj.save("National Dex Guide 1.xlsx")
            return True

        lastwindow = "checklist"
        with open("lastwindow.txt", "w") as file:
            file.write("checklist")

    def dex(root):
        global dexWidgets, labels, leftArrowButton, settingsButton, ctkButtons, ctkEntries, leftArrows, lastwindow, currentPokemon, pokemonButtons, dexWidgets, dexLabel, currentWindow
        currentWindow = "dex"
        currentPokemon = None #keeps track of all the pokemon currently on screen
        pokemonButtons = [None for _ in range(494)]

        def search(*args):#OH MY FUCKING GOD I SOMEHOW MADE THIS WORK LMAO
            global position, pokemonButtons, currentPokemon

            try:
                if currentPokemon:
                    [mon.destroy() for mon in currentPokemon] #checking if there are any pokemon on screen, if there are then delete them
                currentPokemon = []
                # print("test")
            except AttributeError:
                pass

            searchString = searchEntry.get().title() #get text from the search entry then turning first character capitalised and the
                                                     #rest lowercase because that's how the names are formatted in the spreadsheet
            searchLength = len(searchString)
            #print(search in pokemon[1][1][:searchLength+1])
            if searchString == "":
                with open("search.txt", "w") as file:
                    file.write(searchString.lower())
                try:
                    if currentPokemon:
                        [mon.destroy() for mon in currentPokemon]
                    currentPokemon = []
                    # print("test")
                except AttributeError:
                    pass

                return
            x, y = .15, .4
            for i in range(1, 494):
                try:
                    if searchString in pokemon[i]["name"][:searchLength+1]: #checks if the searchString matcheds with any pokemon names
                        pokemonButtons[i] = tk.Button(main, command=lambda dex=i: dexEntryWindow(dex), image=pokemon[i]["icon"], bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)
                        currentPokemon.append(pokemonButtons[i])
                        #print(pokemon[i][1])
                    elif searchString == str(pokemon[i]["dex"]): #this checks for the actual dex number
                        pokemonButtons[i] = tk.Button(main, command=lambda dex=i: dexEntryWindow(dex), image=pokemon[i]["icon"], bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)
                        currentPokemon.append(pokemonButtons[i])
                        dexWidgets.add(pokemonButtons[i])
                    else:
                        continue

                except TclError:
                    continue

                checklistWidgets.add(pokemonButtons[i])
                tkButtons.add(pokemonButtons[i])
                dexWidgets.add(pokemonButtons[i])
                try:
                    pokemonButtons[i].place(relx=x, rely=y)
                except AttributeError:
                    pass
                x += .06
                if x > .85:
                    x = .15
                    y += .2

                if y > .8:
                    break
            pass

            with open("search.txt", "w") as file:
                file.write(searchString.lower())

        dexLabel = tk.Label(main, text = "Ultimate Pokédex", font = ("Pokémon DS Font", 25), bg = primary[currentTheme], fg = secondary[currentTheme])
        dexLabel.place(relx = .5, rely = .1, anchor = "center")

        leftArrowButton = tk.Button(main, image = leftArrows[currentTheme], command = lambda w = "checklist": switch(w), bg = primary[currentTheme], activebackground = primary[currentTheme], highlightthickness=0, borderwidth = 0)
        leftArrowButton.place(relx = .02, rely = .1, anchor = "w")

        settingsButton = tk.Button(main, command=settingsWindow, image=settingsDict[currentTheme],bg=primary[currentTheme], activebackground=primary[currentTheme], highlightthickness=0, borderwidth=0)
        settingsButton.place(relx=.98, rely=.03, anchor="ne")

        searchVar = tk.StringVar()
        searchVar.trace_add("write", search
                            )
        searchEntry = CTkEntry(main, placeholder_text = "Enter Pokémon Name...", textvariable = searchVar, width = 250, height = 20,font = ("Pokémon DS Font", 30), justify = "center", bg_color = primary[currentTheme], fg_color = secondary[currentTheme] )
        searchEntry.place(relx = .5, rely = .25, anchor = "center")



        with open("search.txt") as file:
            for line in file:
                searchEntry.insert(0, line)

        if upArrowButton:
            upArrowButton.place_forget()

        if downArrowButton:
            downArrowButton.place_forget()



        labels.add(dexLabel)

        ctkEntries.add(searchEntry)


        dexWidgets.add(dexLabel)
        dexWidgets.add(leftArrowButton)
        dexWidgets.add(searchEntry)
        dexWidgets.add(settingsButton)

        lastwindow = "dex"
        with open("lastwindow.txt", "w") as file:
            file.write("dex")





        #def scrollDown()
    if lastwindow == "checklist":
        checklist(main)
    else:
        dex(main)



    def resizeWidgets(event):
        width = main.winfo_width()
        height = main.winfo_height()
        font_size = max(12, int(height * 0.06))
        buttonHeight = height*0.13
        buttonWidth = width*0.1

        if currentWindow == "dex":
            dexLabel.configure(font = ("Pokémon DS Font", font_size))
            dexLabel.place(relx=.5, rely=.1, anchor="center", relwidth=0.5, relheight=0.5)

            leftArrowButton.place(relx = .02, rely = .1, anchor = "w", height = buttonHeight, width = buttonWidth)
        elif currentWindow == "checklist":
            checklistLabel.configure(font = ("Pokémon DS Font", font_size))
            checklistLabel.place(relx=.5, rely=.1, anchor="center", relwidth=0.5, relheight=0.5)


    main.bind("<Configure>", resizeWidgets)
    main.mainloop()

def dexEntryWindow(dex):
    global dexEntry, labels, images, backSprite, tkButtons

    if dexEntry[dex] is None or not dexEntry[dex].winfo_exists():
        dexEntry[dex] = ctk.CTkToplevel(main)
        dexEntry[dex].title(pokemon[dex]["name"])
        dexEntry[dex].geometry(("250x225"))
        dexEntry[dex].configure(fg_color=primary[currentTheme])
        dexEntry[dex].resizable(False, False)
        #dexEntry[dex].iconphoto(False, pokemon[dex]["icon"])
        #dexEntry[dex].iconbitmap(f"ico files\{dex}.ico")

        backSprite = tk.Button(dexEntry[dex], image = pokemon[dex]["back"], bg = primary[currentTheme], activebackground = primary[currentTheme], highlightthickness=0, borderwidth = 0)
        backSprite.place(relx = .5, rely = .2, anchor = "center")

        x, y = .5, .4
        titles = ["Diamond", "Pearl", "Platinum", "Heart Gold", "Soul Silver"]
        keys = ["diamond", "pearl", "platinum", "heartgold", "soulsilver"]
        indexes = [num for num in range(5)]
        locations = [None for _ in range(5)]

        for title, key, i in zip(titles, keys, indexes):
            locations[i] = tk.Label(dexEntry[dex], text = f"{title} Obtainment: {pokemon[dex][key]}", font = ("Pokémon DS Font", 10), bg = primary[currentTheme], fg = secondary[currentTheme])
            locations[i].place(relx = x, rely = y, anchor = "center")
            labels.add(locations[i])

            y += .12

        tkButtons.add(backSprite)


intro, settings, dexEntry = None, None, [None for _ in range(494)] #
def valueErrorFix(filePath):
    with open(filePath, "w") as file:
        file.write("1")
        position = 1

def fixEmptyLastWindow(filePath):
    with open(filePath, "w") as file:
        file.write(lastwindow)

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


# getting the game logos
logos = {
    "d": [None, None, False],
    "p": [None, None, False],
    "pl": [None, None, False],
    "hg": [None, None, False],
    "ss": [None, None, False]
    }

with open("lastwindow.txt") as file:
    if os.path.getsize("lastwindow.txt") == 0:
        fixEmptyLastWindow("lastwindow.txt")
    else:
        for line in file:
            if line == "checklist".lower():
                lastwindow = "checklist"
            elif line == "dex".lower():
                lastwindow = "dex"


position = 1
with open("position.txt") as file:
    for line in file:
        try:
            position = int(line)
        except ValueError:
            valueErrorFix("position.txt")

    if position not in [1,53,105,157,209,261,313,365,417,469]:
        position = 1


with open("games.txt") as file:
    i = 0
    check = False
    if os.path.getsize("games.txt") == 0: #checking if the data file is empty, if so then just open the intro window
        print("empty file")
        introWindow()
    else:
        #length = len(file.readlines())

        for (key, value), line in zip(logos.items(), file):
            #print(key)
            if key in line and "True" in line:
                value[2] = True
            elif key in line and "False" in line:
                value[2] = False
            else:
                print("formatting error")
                introWindow()

            i += 1
            if key == "ss":
                check = True

                mainWindow()

        if len(file.readlines()) != 5 and not check: #using file.readlines() before the loop just fucked everything up so this is how it is ig
            print("incorrect number of lines")
            introWindow() #this does mean that the data file can look like absolute rubbish as long as {key} true/false is in the first 5 lines, everything else is fair game lol







