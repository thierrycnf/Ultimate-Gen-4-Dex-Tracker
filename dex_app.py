import openpyxl, setup, pokemon
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from screen import Screen
from theme import Theme



class DexApp:
    total_pokemon = 493
    pokemon_page = 52
    dex_app = None


    def __init__(self) -> None:
        self.current_theme = self.load_theme()
        self.position = setup.setPosition("position.txt")[0]
        self.last_position = setup.setPosition("position.txt")[1]
        self.current_search = ""

        self.workbook = openpyxl.load_workbook("National Dex Guide 1.xlsx")
        self.sheet = self.workbook.active

        # Window variables
        self.intro = None
        self.main = None
        self.settings = None
        self.current_screen = setup.get_last_screen("lastscreen.txt")

        # Widget variables
        self.logos = setup.logos
        self.logo_buttons = setup.logoButtons
        self.settings_dict, self.left_arrows, self.right_arrows, self.up_arrows, self.down_arrows, self.filters = [{} for _ in range(6)]
        self.up_arrow_button = self.down_arrow_button = self.left_arrow_button = self.right_arrow_button = None
        self.destroyed_up = self.destroyed_down = None
        self.checklist_label = self.dex_label = None
        self.settings_button = None
        self.filter_button = None
        self.search_entry = None
        (self.labels, self.images, self.ctk_buttons, self.tk_buttons, self.ct_entries,
         self.checklist_widgets, self.dex_widgets) = [set() for _ in range(7)]



        self.loaded_pokemon = []
        self.pokemon_on_screen = []
        self.pokemon_buttons = []

    @classmethod
    def create_dex_app(cls):
        if cls.dex_app is None:
            DexApp.dex_app = DexApp()
            print(type(DexApp.dex_app))

        return DexApp.dex_app

    @staticmethod
    def load_theme() -> Theme:
        with open("themes.txt", "r") as file:
            theme = file.read().strip()

        return Theme(theme) if theme in ["0","1","2","3"] else Theme.POKEBALL

    def open_window(self, path: str) -> None:
        with open(path) as file:
            i = 0
            check = False
            if os.path.getsize(path) == 0:  # checking if the data file is empty, if so then just open the intro window
                print("empty file")
                self.intro_window()
            else:
                # length = len(file.readlines())

                for (key, value), line in zip(setup.logos.items(), file):
                    # print(key)
                    if key in line and "True" in line:
                        value[2] = True
                    elif key in line and "False" in line:
                        value[2] = False
                    else:
                        print("formatting error")
                        self.intro_window()

                    i += 1
                    if key == "ss":
                        check = True

                        self.main_window()

                if len(file.readlines()) != 5 and not check:  # using file.readlines() before the loop just fucked everything up so this is how it is ig
                    print("incorrect number of lines")
                    self.intro_window()  # this does mean that the data file can look like absolute rubbish as long as {key} true/false is in the first 5 lines, everything else is fair game lol

    def load_pokemon(self) -> list[pokemon.Pokemon]:
        names, d, p, pl, hg, ss, caught = ([self.sheet.cell(row, 2).value for row in range(5, 498)],
                                           [self.sheet.cell(row, 3).value for row in range(5, 498)],
                                           [self.sheet.cell(row, 4).value for row in range(5, 498)],
                                           [self.sheet.cell(row, 5).value for row in range(5, 498)],
                                           [self.sheet.cell(row, 6).value for row in range(5, 498)],
                                           [self.sheet.cell(row, 7).value for row in range(5, 498)],
                                           [self.sheet.cell(row, 9).value for row in range(5, 498)])
        names, d, p, pl, hg, ss, caught = [None] + names, [None] + d, [None] + p, [None] + pl, [None] + hg, [ None] + ss, [
                                              None] + caught

        loaded_pokemon = [pokemon.Pokemon()]  # element at index 0 has to be None because pokedex starts at 1

        for dex in range(1, self.total_pokemon + 1):
            original_image = Image.open(f"icons\{dex}.png")
            original_grey_image = Image.open(f"grey icons\{dex}.png")
            original_back_image = Image.open(f"back sprites\{dex}.png")

            resized_image = original_image.resize((40, 40), Image.Resampling.LANCZOS)
            resized_grey_image = original_grey_image.resize((40, 40), Image.Resampling.LANCZOS)
            resized_back_image = original_back_image.resize((100, 90), Image.Resampling.LANCZOS)

            loaded_pokemon.append(pokemon.Pokemon(dex, names[dex], d[dex], p[dex], pl[dex], hg[dex], ss[dex],caught[dex],
                                           ImageTk.PhotoImage(resized_image), ImageTk.PhotoImage(resized_grey_image),
                                           ImageTk.PhotoImage(resized_back_image)))

        return loaded_pokemon


    def grey(self, game : str) -> None:
        if self.logos[game][2]:
            self.logo_buttons[game].config(image=self.logos[game][1])
            self.logos[game][2] = False
        else:
            self.logos[game][2] = True
            self.logo_buttons[game].config(image=self.logos[game][0])
        
    def intro_window(self) -> None:
        self.intro = ctk.CTk()
        self.intro.title("Ultimate Gen 4 Dex Tracker")
        self.intro.geometry("500x250")
        self.intro.configure(fg_color=setup.primary[self.current_theme])

        for key, value in self.logos.items():
            original_image = Image.open(f"{key}.png")
            original_image2 = Image.open(f"{key} grey.png")
            resized_image = original_image.resize((50, 50), Image.Resampling.LANCZOS)
            resized_image2 = original_image2.resize((50, 50), Image.Resampling.LANCZOS)
            setup.logos[key][0] = ImageTk.PhotoImage(resized_image)
            setup.logos[key][1] = ImageTk.PhotoImage(resized_image2)

        def confirm_intro() -> None:
            if setup.check_games():
                with open("games.txt", "w") as file:

                    for key, value in setup.logos.items():
                        if value[2]:
                            file.write(f"{key} True\n")
                            # print("hello")
                        else:
                            file.write(f"{key} False\n")

                    self.main_window()
            else:
                return

        title = tk.Label(self.intro, text="Ultimate Gen 4 Dex Tracker", font=("Pokémon DS Font", 30),
                         bg=setup.primary[self.current_theme],
                         fg=setup.secondary[self.current_theme])
        title.place(relx=.5, rely=.1, anchor="center")

        please = tk.Label(self.intro, text="Please select your games", font=("Pokémon DS Font", 20),
                          bg=setup.primary[self.current_theme],
                          fg=setup.secondary[self.current_theme])
        please.place(relx=.5, rely=.25, anchor="center")

        change = tk.Label(self.intro, text="(You can change these later)", font=("Pokémon DS Font", 15),
                          bg=setup.primary[self.current_theme],
                          fg=setup.secondary[self.current_theme])
        change.place(relx=.5, rely=.4, anchor="center")

        confirm = ctk.CTkButton(master=self.intro, command= confirm_intro, text="Confirm", font=("Pokémon DS Font", 25),
                                bg_color=setup.primary[self.current_theme], fg_color=setup.secondary[self.current_theme],
                                hover_color=setup.tertiary[self.current_theme], text_color="black")
        confirm.place(relx=.5, rely=.9, anchor="center")

        x = .25
        y = .6
        for key, value in setup.logos.items():
            setup.logoButtons[key] = tk.Button(self.intro, image=value[1], borderwidth=0, bg=setup.primary[self.current_theme],
                                               activebackground=setup.primary[self.current_theme], highlightthickness=0,
                                               command=lambda k=key: self.grey(k))
            setup.logoButtons[key].place(relx=x, rely=y)
            # print(key)
            x += .1

        self.intro.mainloop()

    def main_window(self) -> None:

        if self.intro:
            self.intro.destroy()

        self.main = ctk.CTk()
        self.main.title("Ultimate Gen 4 Dex Tracker")
        self.main.geometry(f"{500}x{250}")
        self.main.tk.call("tk", "scaling", 2.0)
        self.main.resizable(width=True, height=True)
        self.main.configure(fg_color=setup.primary[self.current_theme])

        self.loaded_pokemon = self.load_pokemon()

        for setting in range(len(setup.primary)):
            original_image = Image.open(f"settings\{setting}.png")
            resized_image = original_image.resize((50, 50), Image.Resampling.LANCZOS)
            self.settings_dict[Theme(str(setting))] = ImageTk.PhotoImage(resized_image)

        for right_arrow in range(len(setup.primary)):
            original_image = Image.open(f"right\{right_arrow}.png")
            resized_image = original_image.resize((60, 45), Image.Resampling.LANCZOS)
            self.right_arrows[Theme(str(right_arrow))] = ImageTk.PhotoImage(resized_image)

        for left_arrow in range(len(setup.primary)):
            original_image = Image.open(f"left\{left_arrow}.png")
            resized_image = original_image.resize((60, 45), Image.Resampling.LANCZOS)
            self.left_arrows[Theme(str(left_arrow))] = ImageTk.PhotoImage(resized_image)  #

        for down_arrow in range(len(setup.primary)):
            original_image = Image.open(f"down\{down_arrow}.png")
            resized_image = original_image.resize((50, 45), Image.Resampling.LANCZOS)
            self.down_arrows[Theme(str(down_arrow))] = ImageTk.PhotoImage(resized_image)

        for up_arrow in range(len(setup.primary)):
            original_image = Image.open(f"up\{up_arrow}.png")
            resized_image = original_image.resize((50, 45), Image.Resampling.LANCZOS)
            self.up_arrows[Theme(str(up_arrow))] = ImageTk.PhotoImage(resized_image)

        for filter in range(len(setup.primary)):
            original_image = Image.open(f"sorting\{filter}.png")
            resized_image = original_image.resize((50, 50), Image.Resampling.LANCZOS)
            self.filters[Theme(str(filter))] = ImageTk.PhotoImage(resized_image)

        self.images.add("left")
        self.images.add("right")
        self.images.add("up")
        self.images.add("down")

        for key, value in setup.logos.items():
            original_image = Image.open(f"{key}.png")
            original_image2 = Image.open(f"{key} grey.png")
            resized_image = original_image.resize((50, 50), Image.Resampling.LANCZOS)
            resized_image2 = original_image2.resize((50, 50), Image.Resampling.LANCZOS)
            self.logos[key][0] = ImageTk.PhotoImage(resized_image)
            self.logos[key][1] = ImageTk.PhotoImage(resized_image2)

        def checklist() -> None:
            self.current_screen = Screen.CHECKLIST
            with open("lastscreen.txt", "w") as file:
                file.write(Screen.CHECKLIST.value)
            self.checklist_label = tk.Label(self.main, text="Ultimate Checklist", font=("Pokémon DS Font", 30),
                                      bg=setup.primary[self.current_theme],
                                      fg=setup.secondary[self.current_theme])
            self.checklist_label.place(relx=.5, rely=.1, anchor="center")

            settings_button = tk.Button(self.main, command=self.settings_window, image=self.settings_dict[self.current_theme],
                                       bg=setup.primary[self.current_theme],
                                       activebackground=setup.primary[self.current_theme], highlightthickness=0,
                                       borderwidth=0)
            settings_button.place(relx=.02, rely=.03, anchor="nw")

            right_arrow_button = tk.Button(self.main, image=self.right_arrows[self.current_theme], command=switch_screen,
                                         bg=setup.primary[self.current_theme],
                                         activebackground=setup.primary[self.current_theme], highlightthickness=0,
                                         borderwidth=0)
            right_arrow_button.place(relx=.9, rely=.1, anchor="e")

            def scroll_up() -> None:

                if self.position - self.pokemon_page < 0:
                    return
                self.position -= self.pokemon_page
                # testPosition.configure(text=position)

                if self.position <= 1:
                    # print("yooo")
                    self.up_arrow_button.place_forget()
                    self.destroyed_up = True

                with open("position.txt", "w") as file:
                    file.write(str(self.position))
                # print("destroyedUp: ", destroyedUp)
                if self.destroyed_down:
                    # print("hi")
                    self.down_arrow_button.place(relx=.99, rely=.7, anchor="e")
                    self.destroyed_down = False

                display_mons()

            def scroll_down() -> None:
                if self.position + self.pokemon_page > self.total_pokemon:
                    return
                self.position += self.pokemon_page
                # testPosition.configure(text = position)

                if self.position + self.pokemon_page >= self.total_pokemon:
                    self.down_arrow_button.place_forget()
                    self.destroyed_down = True

                with open("position.txt", "w") as file:
                    file.write(str(self.position))

                if self.destroyed_up:
                    # print("hi")
                    self.up_arrow_button.place(relx=.99, rely=.4, anchor="e")
                    self.destroyed_up = False

                display_mons()

            def display_mons():
                try:
                    [mon.destroy() for mon in self.pokemon_on_screen]
                    self.pokemon_on_screen = []
                    # print("test")
                except AttributeError:
                    pass
                x, y = .1, .2
                # we're supposed to get this from a data file but this will do
                for i in range(self.position, self.total_pokemon + 1):
                    try:
                        if self.loaded_pokemon[i].caught:
                            self.pokemon_buttons[i] = tk.Button(self.main, command=lambda dex_num=i: tick(dex_num), image=self.loaded_pokemon[i].icon,
                                                          bg=setup.primary[self.current_theme],
                                                          activebackground=setup.primary[self.current_theme],
                                                          highlightthickness=0, borderwidth=0)
                        else:
                            self.pokemon_buttons[i] = tk.Button(self.main, command=lambda dex_num=i: tick(dex_num), image=self.loaded_pokemon[i].grey,
                                                          bg=setup.primary[self.current_theme],
                                                          activebackground=setup.primary[self.current_theme],
                                                          highlightthickness=0, borderwidth=0)
                        self.pokemon_on_screen.append(self.pokemon_buttons[i])
                    except TclError:
                        continue

                    self.checklist_widgets.add(self.pokemon_buttons[i])
                    self.tk_buttons.add(self.pokemon_buttons[i])
                    self.pokemon_buttons[i].place(relx=x, rely=y)
                    x += .06
                    if x > .85:
                        x = .1
                        y += .2

                    if y > .8:
                        break

            self.pokemon_buttons = [None for _ in range(self.total_pokemon + 1)]
            self.pokemon_on_screen = []
            print(self.position)
            # position = 1

            # testPosition = tk.Label(main, text = position, font = ("Pokémon DS Font", 25), bg = primary[self.current_theme], fg = secondary[self.current_theme])
            # testPosition.place(relx = .04, rely = .5)
            if self.up_arrow_button:
                self.up_arrow_button.destroy()
                self.up_arrow_button = None

            if self.down_arrow_button:
                self.down_arrow_button.destroy()
                self.down_arrow_button = None

            self.up_arrow_button = tk.Button(self.main, image=self.up_arrows[self.current_theme], command=scroll_up,
                                      bg=setup.primary[self.current_theme],
                                      activebackground=setup.primary[self.current_theme], highlightthickness=0, borderwidth=0)
            self.down_arrow_button = tk.Button(self.main, image=self.down_arrows[self.current_theme], command=scroll_down,
                                        bg=setup.primary[self.current_theme],
                                        activebackground=setup.primary[self.current_theme], highlightthickness=0,
                                        borderwidth=0)

            self.destroyed_up = self.destroyed_down = False

            if self.position - self.pokemon_page > 0:
                # print("hi")
                self.up_arrow_button.place(relx=.99, rely=.4, anchor="e")
            else:
                self.destroyed_up = True

            if self.position + self.pokemon_page < 493:
                self.down_arrow_button.place(relx=.99, rely=.7, anchor="e")
            else:
                self.destroyed_down = True

            print(self.position)

            def scroll_up_event(event) -> None:
                scroll_up()

            def scroll_down_event(event) -> None:
                scroll_down()

            self.main.bind("<MouseWheel>", lambda e: scroll_up_event(e) if e.delta > 0 else scroll_down_event(e))
            display_mons()

            self.labels.add(self.checklist_label)

            self.checklist_widgets.add(self.checklist_label)
            self.checklist_widgets.add(settings_button)
            self.checklist_widgets.add(right_arrow_button)
            self.checklist_widgets.add(self.up_arrow_button)
            self.checklist_widgets.add(self.down_arrow_button)

            def tick(dex : int) -> bool:
                try:  # checking if the spreadsheet is open and if it is, give an error message
                    self.workbook.save("National Dex Guide 1.xlsx")

                except PermissionError:
                    messagebox.showerror("Error!", "You must close National Dex Guide 1.xlsx")
                    return False

                self.loaded_pokemon[dex].caught = not self.loaded_pokemon[dex].caught  # inverting the boolean
                image = self.loaded_pokemon[dex].icon if self.loaded_pokemon[dex].caught else self.loaded_pokemon[dex].grey

                self.pokemon_buttons[dex].configure(image=image)  # changing image to corresponding boolean
                cell = self.sheet.cell(row=dex + 4, column=9)  # getting the correct cell for the current pokemon
                cell.value = self.loaded_pokemon[dex].caught  # actually modifying the cell

                self.workbook.save("National Dex Guide 1.xlsx")
                return True

        def dex() -> None:
            self.current_screen = Screen.DEX
            with open("lastscreen.txt", "w") as file:
                file.write(Screen.DEX.value)

            self.pokemon_on_screen = []
            self.pokemon_buttons = [None for _ in range(self.total_pokemon + 1)]

            def check_search_text_file(path : str) -> None:
                with open(path) as file:
                    for line in file:
                        self.search_entry.insert(0, line)

            def write_to_search_text_file(path : str, search_string : str) -> None:
                with open(path, "w") as file:
                    file.write(search_string.lower())

            def search(*args, start=1, dex_positions=None, page=0) -> None:  # OH MY FUCKING GOD I SOMEHOW MADE THIS WORK LMAO

                final_pokemon, display_up_arrow, display_down_arrow = False, start != 1, False
                final_pokemon = False
                if dex_positions is None:
                    dex_positions = [1]
                if self.down_arrow_button:
                    self.down_arrow_button.destroy()
                    self.down_arrow_button = None

                if self.up_arrow_button:
                    self.up_arrow_button.destroy()
                    self.up_arrow_button = None

                try:
                    if self.pokemon_on_screen:
                        [mon.destroy() for mon in
                         self.pokemon_on_screen]  # checking if there are any pokemon on screen, if there are then delete them
                    self.pokemon_on_screen = []
                    # print("test")
                except AttributeError:
                    pass

                search_string = self.search_entry.get().title()  # get text from the search entry then turning first character capitalised and the
                # rest lowercase because that's how the names are formatted in the spreadsheet
                search_length = len(search_string)
                # print(search in pokemon[1][1][:search_length+1])
                # if search_string == "":
                #     writeToSearchTextFile("search.txt", search_string)
                #     try:
                #         if self.pokemon_on_screen:
                #             [mon.destroy() for mon in self.pokemon_on_screen]
                #         self.pokemon_on_screen = []
                #         # print("test")
                #     except AttributeError:
                #         pass
                #
                #     return
                x, y = .1, .4

                for i in range(start, 494):
                    if ((setup.logos["d"][2] and self.loaded_pokemon[i].inDiamond) or (setup.logos["p"][2] and self.loaded_pokemon[i].inPearl) or 
                        (setup.logos["pl"][2] and self.loaded_pokemon[i].inPlatinum) or (setup.logos["hg"][2] and self.loaded_pokemon[i].inHeartGold) or
                        (setup.logos["ss"][2] and self.loaded_pokemon[i].inSoulSilver)):
                        pass
                    else:
                        print(f"I skipped {self.loaded_pokemon[i].name}")
                        continue
                    try:
                        if search_string in self.loaded_pokemon[i].name[
                            :search_length + 1]:  # checks if the search_string matcheds with any pokemon names
                            if final_pokemon:
                                display_down_arrow = True
                                break
                            self.pokemon_buttons[i] = tk.Button(self.main, command=lambda dex=i: self.dex_entry_window(dex),
                                                          image=self.loaded_pokemon[i].icon,
                                                          bg=setup.primary[self.current_theme],
                                                          activebackground=setup.primary[self.current_theme],
                                                          highlightthickness=0, borderwidth=0)
                            self.pokemon_on_screen.append(self.pokemon_buttons[i])
                            # print(pokemon[i][1])
                        elif search_string == str(self.loaded_pokemon[i].dex):  # this checks for the actual dex number
                            if final_pokemon:
                                display_down_arrow = True
                                break
                            self.pokemon_buttons[i] = tk.Button(self.main, command=lambda dex=i: self.dex_entry_window(dex),
                                                          image=self.loaded_pokemon[i].icon,
                                                          bg=setup.primary[self.current_theme],
                                                          activebackground=setup.primary[self.current_theme],
                                                          highlightthickness=0, borderwidth=0)
                            self.pokemon_on_screen.append(self.pokemon_buttons[i])
                            self.dex_widgets.add(self.pokemon_buttons[i])
                        else:
                            continue

                    except TclError:
                        continue

                    self.checklist_widgets.add(self.pokemon_buttons[i])
                    self.tk_buttons.add(self.pokemon_buttons[i])
                    self.dex_widgets.add(self.pokemon_buttons[i])
                    try:
                        self.pokemon_buttons[i].place(relx=x, rely=y)
                    except AttributeError:
                        pass
                    x += .06
                    if x > .85:
                        x = .1
                        y += .2

                    if y > .8:
                        dex_positions.append(i + 1)
                        final_pokemon = True
                        continue



                write_to_search_text_file("search.txt", search_string)
                dex_positions = list(dict.fromkeys(dex_positions))

                if display_down_arrow:
                    self.down_arrow_button = tk.Button(self.main, image=self.down_arrows[self.current_theme], bg=setup.primary[self.current_theme],
                                                activebackground=setup.primary[self.current_theme], highlightthickness=0,
                                                borderwidth=0,
                                                command=lambda: search(start=dex_positions[page + 1],
                                                                       dex_positions=dex_positions, page=page + 1))
                    self.down_arrow_button.place(relx=.99, rely=.7, anchor="e")

                    print(display_down_arrow)

                if display_up_arrow:
                    self.up_arrow_button = tk.Button(self.main, image=self.up_arrows[self.current_theme], bg=setup.primary[self.current_theme],
                                              activebackground=setup.primary[self.current_theme], highlightthickness=0,
                                              borderwidth=0,
                                              command=lambda: search(start=dex_positions[page - 1],
                                                                     dex_positions=dex_positions, page=page - 1))
                    self.up_arrow_button.place(relx=.99, rely=.4, anchor="e")

                return

            self.current_search = search

            def scroll_search(event) -> None:
                if event.delta < 0 and self.down_arrow_button:
                    self.down_arrow_button.invoke()
                elif event.delta > 0 and self.up_arrow_button:
                    self.up_arrow_button.invoke()

            self.main.bind("<MouseWheel>", scroll_search)
            self.dex_label = tk.Label(self.main, text="Ultimate Pokédex", font=("Pokémon DS Font", 25),
                                bg=setup.primary[self.current_theme],
                                fg=setup.secondary[self.current_theme])
            self.dex_label.place(relx=.5, rely=.1, anchor="center")

            self.left_arrow_button = tk.Button(self.main, image=self.left_arrows[self.current_theme], command=switch_screen,
                                        bg=setup.primary[self.current_theme], activebackground=setup.primary[self.current_theme],
                                        highlightthickness=0,
                                        borderwidth=0)
            self.left_arrow_button.place(relx=.02, rely=.1, anchor="w")

            self.settings_button = tk.Button(self.main, command=self.settings_window, image=self.settings_dict[self.current_theme],
                                       bg=setup.primary[self.current_theme],
                                       activebackground=setup.primary[self.current_theme], highlightthickness=0,
                                       borderwidth=0)
            self.settings_button.place(relx=.98, rely=.03, anchor="ne")

            self.filter_button = tk.Button(self.main, command=self.filter_window, image=self.filters[self.current_theme],
                                     bg=setup.primary[self.current_theme],
                                     activebackground=setup.primary[self.current_theme], highlightthickness=0, borderwidth=0)

            self.filter_button.place(relx=.8, rely=.25, anchor="center")

            search_var = tk.StringVar()
            search_var.trace_add("write", search)
            self.search_entry = CTkEntry(self.main, placeholder_text="Enter Pokémon Name...", textvariable=search_var, width=250,
                                   height=20, font=("Pokémon DS Font", 30), justify="center",
                                   bg_color=setup.primary[self.current_theme],
                                   fg_color=setup.secondary[self.current_theme])
            self.search_entry.place(relx=.5, rely=.25, anchor="center")

            search()



        def delete_screen() -> None:
            if self.current_screen == Screen.DEX:
                for widget in self.checklist_widgets:
                    widget.destroy()
            else:
                for widget in self.dex_widgets:
                    widget.destroy()

        def switch_screen() -> None:
            delete_screen()
            if self.current_screen == Screen.DEX:
                checklist()
            else:
                dex()

        def resize_widgets(event) -> None:
            width = self.main.winfo_width()
            height = self.main.winfo_height()
            font_size = max(12, int(height * 0.06))
            buttonHeight = height * 0.13
            buttonWidth = width * 0.1

            if self.current_screen == Screen.DEX:
                self.dex_label.configure(font=("Pokémon DS Font", font_size))
                self.dex_label.place(relx=.5, rely=.1, anchor="center", relwidth=0.5, relheight=0.5)

                self.left_arrow_button.place(relx=.02, rely=.1, anchor="w", height=buttonHeight, width=buttonWidth)
            elif self.current_screen == Screen.CHECKLIST:
                self.checklist_label.configure(font=("Pokémon DS Font", font_size))
                self.checklist_label.place(relx=.5, rely=.1, anchor="center", relwidth=0.5, relheight=0.5)


        if self.current_screen == Screen.DEX.value:
            dex()
        else:
            checklist()

        self.main.bind("<Configure>", resize_widgets)
        self.main.mainloop()
    def settings_window(self) -> None:
        pass
    
    def dex_entry_window(self, dex : int) -> None:
        pass

    def filter_window(self) -> None:
        pass




dex_app = DexApp.create_dex_app()
dex_app.open_window("games.txt")