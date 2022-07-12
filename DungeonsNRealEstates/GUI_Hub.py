# Author: JT Mitchell
# GitHub username: JtMitchellOsuStudent
# Date: 6/1/22
# Description: Week 9 - PortfolioProject GUI_Hub.
# Description: GUI_Hub.py uses the built-in tkinter module to create a GUI for RealEstateGame.py.
# GUI_Hub.py contains a number of classes and methods for creating and manipulating GUI elements
# used for playing a monopoly-esque game called Real Estate Game (or Dungeons and Real Estates).

"""
Code Outline:

10 classes:
GuiHub: The GUI Hub class builds and holds a reference to all GUI elements in the game.
GuiGameBoard: A simple class that creates the GUI representation of the game board.
GuiSpaces: GuiSpaces creates a GUI representation of the 25 spaces for the real estate game.
GuiStatWindow: Creates the GUI display windows that show various player stats during game play.
GuiAddPlayerButton: Creates the GUI elements for the Add Player Button and contains some player creation logic.
GuiDiceButton: Creates the GUI elements for the dice button, and contains some dice logic.
GuiBuyButton: Creates the GUI elements for the buy button, and contains some space purchasing logic.
GuiPlayerMovement: Contains some logic for manipulating the location of the player GUI elements.
GuiGameLogic: GuiGameLogic manages the core game logic whenever the game is played using the GUI.
    Including the AI player logic.
GuiPlayer: Creates the GUI representation of the player object.

4 non-class functions:
get_players: Gets the player dictionary as it currently is in the real estate game.
get_spaces: Gets the spaces list as it currently is in the real estate game.
get_players_as_list: Returns a list of all player names.
draw_a_dragon: Draws a dragon using vertex points.
"""

from tkinter import *
import random


class GuiHub:
    """ The GUI Hub class builds and holds a reference to all GUI elements in the game.
    Additionally, it contains a few methods that are called by GUI buttons, and the RealEstateGame class.  """

    def __init__(self, master, real_estate_game):
        """ Initializes and creates all GUI elements. """
        self._canvas = Canvas(master, width=1400, height=1080)
        self._reg = real_estate_game  # reg short for real estate game.
        self.create_game_board()
        self._stats = GuiStatWindow(self._canvas, self._reg)
        self._add_button = GuiAddPlayerButton(self._canvas, self._reg, self)
        self._dice_button = GuiDiceButton(self._canvas, self)
        self._buy_button = GuiBuyButton(self._canvas, self._reg, self)
        self._player_movement = GuiPlayerMovement(self._dice_button, self._canvas, self._reg)
        self._logic = GuiGameLogic(self._canvas, self._reg, self)
        self._canvas.pack()

    def create_game_board(self):
        """ Creates the game board. """
        GuiGameBoard(self._canvas)
        GuiSpaces(self._canvas, self._reg)

    def update_stats(self):
        """ Updates player stats in GUI. """
        self._stats.build_player_color_key()
        self._stats.set_all_stat()

    def get_stats(self):
        return self._stats

    def get_add_button(self):
        return self._add_button

    def get_dice_button(self):
        return self._dice_button

    def get_buy_button(self):
        return self._buy_button

    def get_player_movement(self):
        return self._player_movement

    def get_logic(self):
        return self._logic


class GuiGameBoard:
    """ A simple class that creates the GUI representation of the game board. """

    def __init__(self, canvas):
        self._dusty_blue = "#%02x%02x%02x" % (76, 104, 181)  # Dusty blue color (prevents clashing with blue players).
        canvas.create_rectangle(0, 0, 1400, 1080, fill="brown")
        canvas.create_rectangle(135, 135, 945, 945, fill=self._dusty_blue, outline="black", width=13.5)
        canvas.create_text(525, 500, text="Dungeons & Real Estates", font=("bold", 30))


class GuiSpaces:
    """ GuiSpaces creates a GUI representation of the 25 spaces for the real estate game. """

    def __init__(self, canvas, real_estate_game):
        self._canvas = canvas
        self._spaces = get_spaces(real_estate_game)
        self.create_spaces()
        self.set_game_space_colors()
        self.set_go_space_color()

    def create_spaces(self):
        """ Creates the GUI representation of each space and organizes them into a square. """
        dir_x = 99
        dir_y = 99
        my_dir = 99

        for index in range(0, 25):
            space_obj, text_obj = self.build_space_obj_tuple(index, 148.5, 236.25)

            if index == 1:  # Manually set location of the second space.
                self.move_obj(text_obj, my_dir, 0)
                self.move_obj(space_obj, my_dir, 0)

            if index > 1:
                dir_x, dir_y = self.determine_space_location(index, my_dir, dir_x, dir_y)
                self.move_obj(space_obj, dir_x, dir_y)
                self.move_obj(text_obj, dir_x, dir_y)

    def build_space_obj_tuple(self, index, ulc, lrc):
        """ Returns a tuple with two GUI elements that represent a space on the game board. """
        space_obj = self._canvas.create_rectangle(ulc, ulc, lrc, lrc, fill="white", outline="black")
        my_text = self.build_space_text(index)
        text_obj = self._canvas.create_text(ulc + 35, ulc + 32, text=my_text)
        self._spaces[index].set_gui_element(space_obj)
        return space_obj, text_obj

    def build_space_text(self, index):
        """ Builds and returns a string representing some key information about the space at the given index. """
        space = self._spaces[index]
        if index == 0:
            payout = space.get_payout()
            return f"1\nGO\nCollect: {payout}"
        else:
            name = space.get_name()
            name = name[0:7]  # Only use a slice of the name, prevents text from overlapping.
            rent = space.get_rent()
            price = space.get_purchase_amt()
            my_text = f"{index + 1}\n{name}\nrent:{rent}\nprice:{price}"
            return my_text

    @staticmethod
    def determine_space_location(index, my_dir, dir_x, dir_y):
        """ Determines the location each space should be in the GUI game board.
        Returns the x and y directions that the space should be moved. """
        if 1 < index <= 6:  # space is from upper left corner to upper right corner
            return dir_x + my_dir, 0
        elif index == 7:  # cut upper right corner
            return dir_x + my_dir, my_dir
        elif 7 < index <= 12:  # space is from upper right corner to lower right corner
            return dir_x, dir_y + my_dir
        elif index == 13:  # cut lower right corner
            return dir_x - my_dir, dir_y + my_dir
        elif 13 < index <= 18:  # space is from lower right corner to lower left corner
            return dir_x - my_dir, dir_y
        elif index == 19:  # cut lower left corner
            return dir_x - my_dir, dir_y - my_dir
        elif 19 < index <= 24:  # space is from lower left corner to upper left corner
            return dir_x, dir_y - my_dir
        return dir_x, dir_y

    def move_obj(self, obj, x_axis, y_axis):
        """ Moves a GUI object. """
        self._canvas.move(obj, x_axis, y_axis)

    def set_game_space_colors(self):
        """ Sets the starting colors for each GUI space element in the game board. """
        tog = False  # Bool to toggle color every other space.
        for space in self._spaces:
            element = space.get_gui_element()
            if tog:
                self._canvas.itemconfig(element, fill='grey')
            else:
                self._canvas.itemconfig(element, fill="white")
            tog = not tog

    def set_go_space_color(self):
        """ Sets the color of the GO space. """
        go = self._spaces[0]
        go_element = go.get_gui_element()
        self._canvas.itemconfig(go_element, fill="orange")


class GuiStatWindow:
    """ Creates the GUI display windows that show various player stats during game play.  """

    def __init__(self, canvas, real_estate_game):
        self._canvas = canvas
        self._reg = real_estate_game
        self._dusty_blue = "#%02x%02x%02x" % (76, 104, 181)
        self._cur_player_color = None
        self._color_key = []
        self._all_stat_window = None
        self._cur_stat_window = None
        self._cur_stat_outline = None
        self.create_window()

    def create_window(self):
        """ Creates the various GUI windows for displaying player stats. """
        self._canvas.create_rectangle(995, 135, 1345, 945, fill=self._dusty_blue, outline="black", width=13.5)
        self._cur_stat_outline = self._canvas.create_rectangle(1030, 320, 1310, 420)
        self._cur_player_color = self._canvas.create_rectangle(1030, 320, 1310, 347)
        self._canvas.create_text(1160, 300, text="Current Player:", font=("bold", 20))
        self._cur_stat_window = self._canvas.create_text(1160, 370, font=("bold", 15))
        all_stat = self.set_all_stat()
        self._all_stat_window = self._canvas.create_text(1160, 675, text=all_stat, font=("bold", 15))

    def build_player_color_key(self):
        """ Builds GUI elements for the player color key. """
        top = 640
        bottom = 660
        players = get_players(self._reg)
        if len(self._color_key) < len(players):
            if len(self._color_key) >= 1:
                last_key = self._color_key[len(self._color_key) - 1]
                key_coord = self._canvas.coords(last_key)
                key = self._canvas.create_oval(1020, key_coord[1] + 25, 1040, key_coord[3] + 25, fill="white")
            else:
                key = self._canvas.create_oval(1020, top, 1040, bottom, fill="white")
            self._color_key.append(key)
        self.set_color_key_colors()

    def set_color_key_colors(self):
        """ Sets the color of each GUI element in the player color keys. """
        player_list = get_players_as_list(self._reg)
        for i in range(0, len(player_list)):
            name = player_list[i]
            color = self.get_player_color(name)
            self._canvas.itemconfig(self._color_key[i], fill=color)
            if len(player_list) > 2:
                self._canvas.move(self._color_key[i], 0, -10)

    def set_all_stat(self):
        """ Creates a string containing each player's name and how much money they have.
        Then, sets the all_stat_window GUI element's text equal to that string. """
        players = get_players(self._reg)
        all_stat = ""
        for player in players:
            bal = players[player].get_balance()
            all_stat += f"{player}: {bal}$\n"
        self._canvas.itemconfig(self._all_stat_window, text=all_stat)
        return all_stat

    def show_cur_player_stats(self, cur_player_name):
        """ Displays all stats for the current player. """
        spaces = get_spaces(self._reg)
        pos = self.get_player_pos(cur_player_name)
        color = self.get_player_color(cur_player_name)
        money = self.get_player_money(cur_player_name)
        space = spaces[pos]
        space_gui = space.get_gui_element()
        space_color = self._canvas.itemcget(space_gui, "fill")
        self._canvas.itemconfig(self._cur_stat_outline, fill=space_color)
        space_name = space.get_name()
        space_rent = space.get_rent()
        space_amt = space.get_purchase_amt()
        my_text = f"{cur_player_name}: {money}$\nLocation: {space_name}\n-- Rent: " \
                  f"{space_rent}$ --\n-- Buy: {space_amt}$ --"
        self._canvas.itemconfig(self._cur_stat_window, text=my_text)
        self._canvas.itemconfig(self._cur_player_color, fill=color)
        self.set_all_stat()

    def get_player_color(self, name):
        """ Returns the players color. """
        players = get_players(self._reg)
        player_obj = players[name]
        player_gui = player_obj.get_gui_element()
        color = self._canvas.itemcget(player_gui, "fill")
        return color

    def get_player_pos(self, name):
        """ Returns the players current position. """
        pos = self._reg.get_player_current_position(name)
        return pos

    def get_player_money(self, name):
        """ Returns the players current account balance. """
        money = self._reg.get_player_account_balance(name)
        return money


class GuiAddPlayerButton:
    """ Creates the GUI elements for the Add Player Button and contains some player creation logic. """

    def __init__(self, canvas, real_estate_game, hub):
        self._canvas = canvas
        self._hub = hub
        self._name_entry = StringVar()
        self._color_entry = StringVar()
        self._reg = real_estate_game
        self._color_options = ["red", "blue", "purple", "green", "yellow", "pink", "orange", "black",
                               "white", "cyan", "brown"]
        self._icon_button = None
        self._icon_text = StringVar()
        self._cur_icon = 0
        self._icon_choices = ["Dragon", "Mage", "Unicorn", "Knight"]
        self._ai_button = None
        self._ai_bool = False
        self._ai_text = StringVar()
        self.create_add_player_button()

    def create_add_player_button(self):
        """ Creates all GUI elements associated with the Add Player Button. """
        add_button = Button(self._canvas, text="add player", command=self.add_player_button_press, font=("bold", 10))
        add_button.place(x=1150, y=900)
        self.create_labels()
        self.create_player_entry()
        self.create_ai_button()
        self.create_icon_button()

    def create_labels(self):
        """ Creates all labels associated with the add player GUI. """
        self._canvas.create_text(1150, 770, text="ADD PLAYER:", font=("bold", 20))
        self._canvas.create_text(500, 100, text="(Add player's at the bottom right to begin.)", font=10)
        self._canvas.create_text(1090, 800, text="new player name:", font=("bold", 10))
        self._canvas.create_text(1090, 820, text="new player color:", font=("bold", 10))
        self._canvas.create_text(1090, 880, text="new player icon:", font=("bold", 10))

    def create_player_entry(self):
        """ Creates the GUI elements for the custom player entry settings. """
        player_name_entry = Entry(self._canvas, textvariable=self._name_entry)
        player_color_entry = Entry(self._canvas, textvariable=self._color_entry)
        player_name_entry.place(x=1150, y=790)
        player_color_entry.place(x=1150, y=810)

    def create_ai_button(self):
        """ Creates the GUI elements for the Human/AI toggle button. """
        self._canvas.create_text(1090, 850, text="new player type:", font=("bold", 10))
        self._ai_text.set("Human")
        self._ai_button = Button(self._canvas, textvariable=self._ai_text, command=self.set_ai, font=("bold", 10))
        self._ai_button.place(x=1150, y=835)

    def create_icon_button(self):
        """ Creates the GUI elements for the icon selection button."""
        self._icon_text.set("Dragon")
        self._icon_button = Button(self._canvas, textvariable=self._icon_text, command=self.icon_switch,
                                   font=("bold", 10))
        self._icon_button.place(x=1150, y=867)

    def add_player_button_press(self):
        """ Logic to be called when the add player button is pressed. """
        name = self._name_entry.get()
        if name == "":
            name = self.random_name()
        name = self._reg.repeated_name_check(name)
        self._reg.create_player(name, 1000)
        color = self._color_entry.get()
        if color == "" or color not in self._color_options:
            color = self.pick_some_color()
        icon = self.get_icon()
        self.create_player(name, color, icon)
        self._hub.update_stats()
        logic = self._hub.get_logic()
        logic.set_cur_player(name)
        self.ai_player_check(name)
        self.icon_switch()


    @staticmethod
    def random_name():
        """ Returns a random name from the some_names list. """
        some_names = ["Forgle gnome", "Drax vampire", "Spoon goblin",  "Vroll the gnoll", "tkinter",
                      "Callegari lich", "Lenore", "D.M.onster", "Agent Ethel", "P.I. Mildred", "Bonk", "Grunx",
                      "bard Brhudvi", "Grunkle", "Finn", "Jake", "Dax", "Kellanved", "Beans", "Roo", "Alton", "Rue",
                      "Fenna", "Uncle Bob", "Frank Dopple", "Cron"]
        name = some_names[random.randrange(0, len(some_names) - 1)]
        return name

    def pick_some_color(self):
        """ Picks and returns a color out of the color options list. """
        some_colors = self._color_options
        count = len(get_players(self._reg))
        if count < len(some_colors) - 1:
            return some_colors[count - 1]
        else:
            return some_colors[random.randrange(0, len(some_colors) - 1)]

    def create_player(self, name, color="red", shape_key="d"):
        """ Creates the GUI elements for a player. """
        player = GuiPlayer(self._canvas, color, shape_key)
        player_gui = player.create_player()
        players = get_players(self._reg)
        p_parent = players[name]
        p_parent.set_gui_element(player_gui)
        self.move_player_to_go_space(player_gui)

    def move_player_to_go_space(self, player_gui):
        """ Moves the player to the go space, and shifts their start position slightly to prevent overlap. """
        spaces = get_spaces(self._reg)
        go_space = spaces[0].get_gui_element()
        go_coord = self._canvas.coords(go_space)
        x_pos = go_coord[1] + random.randint(-20, -15)
        y_pos = x_pos + random.randint(16, 20)
        self._canvas.move(player_gui, x_pos, y_pos)

    def set_ai(self):
        """ Determines weather the player being created will be an AI or a human player. """
        if self._ai_bool:
            self._ai_text.set("Human")
        else:
            self._ai_text.set(" AI ")
        self._ai_bool = not self._ai_bool

    def ai_player_check(self, name):
        """ Sets the player objects AI status variable to True. """
        if self._ai_bool:
            players = get_players(self._reg)
            player = players[name]
            player.enable_ai()

    def icon_switch(self):
        """ Cycles through the icon options. """
        if self._cur_icon < len(self._icon_choices) - 1:
            self._cur_icon += 1
        else:
            self._cur_icon = 0
        self._icon_text.set(self._icon_choices[self._cur_icon])

    def get_icon(self):
        """ Returns the shape key for the current icon. """
        if self._cur_icon == 0:
            return "d"
        if self._cur_icon == 1:
            return "m"
        if self._cur_icon == 2:
            return "u"
        if self._cur_icon == 3:
            return "k"


class GuiDiceButton:
    """ Creates the GUI elements for the dice button, and contains some dice logic. """

    def __init__(self, canvas, hub):
        self._canvas = canvas
        self._hub = hub
        self._dice_text = None
        self._dice_num = 0
        self._dice_button = None
        self.create_dice()

    def create_dice(self):
        """ Creates the GUI elements for the dice button. """
        self._canvas.create_rectangle(1200, 175, 1250, 225, fill="white", outline="black", width=6.75)
        self._dice_button = dice_button = Button(self._canvas, text="roll dice", command=self.roll_dice, font=("bold", 20))
        self._dice_text = self._canvas.create_text(1224, 202, text=self._dice_num, font=("bold", 40))
        self._dice_button.place(x=1050, y=173)

    def roll_dice(self):
        """ Logic to be called when the dice button is pressed. """
        self._dice_num = random.randint(1, 6)
        self._canvas.itemconfig(self._dice_text, text=self._dice_num)
        logic = self._hub.get_logic()
        logic.move_player(self._dice_num)

    def hide_dice(self):
        self._dice_button.place(x=100000, y=173)

    def show_dice(self):
        self._dice_button.place(x=1050, y=173)


class GuiBuyButton:
    """ Creates the GUI elements for the buy button, and contains some space purchasing logic. """

    def __init__(self, canvas, real_estate_game, hub):
        self._canvas = canvas
        self._reg = real_estate_game
        self._hub = hub
        self._buy_button_outline = None
        self._button = None
        self.buy_button()

    def buy_button(self):
        """ Creates the GUI elements for the buy button. """
        self._buy_button_outline = self._canvas.create_rectangle(1040, 460, 1240, 545, fill="red", outline="black")
        self._button = Button(self._canvas, text="Buy Property", command=self.buy_button_press, font=("bold", 20))
        self._button.place(x=1050, y=475)

    def set_buy_button_color(self, cur_player):
        """ Sets the color of the buy_button_outline GUI element to be the current players color if the current
        player can buy their current space or clear if they can't. """
        pos = self._reg.get_player_current_position(cur_player)
        if pos == 0:
            self._button.place(x=4050, y=475)
            self._canvas.itemconfig(self._buy_button_outline, fill="", outline="")
            return
        spaces = get_spaces(self._reg)
        money = self._reg.get_player_account_balance(cur_player)
        cost = spaces[pos].get_purchase_amt()
        owner = spaces[pos].get_owner()
        if money > cost and owner is None:
            self._button.place(x=1050, y=475)
            color = get_cur_player_color(self._canvas, self._reg, cur_player)
            self._canvas.itemconfig(self._buy_button_outline, fill=color, outline="black")
        else:
            self._button.place(x=4050, y=475)
            self._canvas.itemconfig(self._buy_button_outline, fill="", outline="")

    def buy_button_press(self):
        """ Logic to be called when the buy button is pressed. """
        logic = self._hub.get_logic()
        logic.buy_space()

    def modify_space_color(self, cur_player):
        """ Modifies the color of a space to match the player who purchased it. """
        spaces = get_spaces(self._reg)
        players = get_players(self._reg)
        player_obj = players[cur_player]
        player_pos = player_obj.get_position()
        player_space = spaces[player_pos]
        space_owner_obj = player_space.get_owner()
        if space_owner_obj is not None and space_owner_obj.get_name() == cur_player:
            player_gui = player_obj.get_gui_element()
            color = self._canvas.itemcget(player_gui, "fill")
            space_gui = player_space.get_gui_element()
            self._canvas.itemconfig(space_gui, fill=color)


class GuiPlayerMovement:
    """ Contains some logic for manipulating the location of the player GUI elements. """

    def __init__(self, dice, canvas, real_estate_game):
        self._dice_button = dice
        self._canvas = canvas
        self._reg = real_estate_game
        self._space_size = 101.25
        self._indicators = []

    def move_player(self, player_name, num_spaces):
        """ Moves the location of the player's GUI element."""
        player_obj = self._reg.get_player_object(player_name)
        player_gui = player_obj.get_gui_element()
        old_location = player_obj.get_position()
        new_location = player_obj.get_position() + num_spaces

        if new_location <= 25:
            self.move_player_loop(player_gui, new_location, old_location)
        else:
            adjusted_location = new_location - 25
            self.move_player_loop(player_gui, 25, old_location)
            self.move_player_loop(player_gui, 1, 25)
            if adjusted_location != 1:
                self.move_player_loop(player_gui, adjusted_location, 1)

        self.remove_indicators()

    def move_player_loop(self, player, new_location, old_location):
        """ Moves the location of the player's GUI element by looping
        through locations until the player reaches the goal location. """

        if old_location == 25 and new_location == 1:
            self.move_obj(player, self._space_size, 0)

        while old_location < new_location:
            if old_location <= 5:
                self.move_obj(player, self._space_size, 0)
            elif old_location == 6:
                self.move_obj(player, self._space_size, self._space_size)
            elif 7 <= old_location <= 11:
                self.move_obj(player, 0, self._space_size)
            elif old_location == 12:
                self.move_obj(player, -self._space_size, self._space_size)
            elif 13 <= old_location <= 17:
                self.move_obj(player, -self._space_size, 0)
            elif old_location == 18:
                self.move_obj(player, -self._space_size, -self._space_size)
            elif 19 <= old_location <= 25:
                self.move_obj(player, 0, -self._space_size)
            old_location += 1
            self.indicate_old_pos(player, old_location)

    def move_obj(self, obj, x_axis, y_axis):
        """ Moves a GUI object. """
        self._canvas.move(obj, x_axis, y_axis)

    def indicate_old_pos(self, player, pos):
        """ Leaves a tail of GUI objects to indicate where player has moved from.  (Creates a pseudo-animation) """
        pos -= 1
        color = self._canvas.itemcget(player, "fill")
        spaces = get_spaces(self._reg)
        space = spaces[pos]
        space_gui = space.get_gui_element()
        pos = self._canvas.coords(space_gui)
        self.create_oval(pos, color)

    def create_oval(self, pos, color):
        """ Creates an oval GUI object at the given position. """
        oval = self._canvas.create_oval(pos[0] + 25, pos[1] + 25, pos[2] - 25, pos[3] - 25, fill=color)
        self._indicators.append(oval)

    def remove_indicators(self):
        """ Removes the tail GUI objects one at a time. """
        self._dice_button.hide_dice()
        self._canvas.update()
        for oval in self._indicators:
            #  Sets the animation speed:
            self._canvas.after(100, self.delete_oval(oval))  # 100 is the ideal animation speed determined by tests.
            self._canvas.update()
        self._indicators = []
        self._dice_button.show_dice()

    def delete_oval(self, oval):
        """ Deletes the given GUI oval object. """
        self._canvas.delete(oval)


class GuiGameLogic:
    """ GuiGameLogic manages the core game logic whenever the game is played using the GUI.
    Including the AI player logic. """

    def __init__(self, canvas, real_estate_game, hub):
        self._canvas = canvas
        self._reg = real_estate_game
        self._hub = hub
        self._stats = hub.get_stats()
        self._movement = hub.get_player_movement()
        self._add_button = hub.get_add_button()
        self._dice_button = hub.get_dice_button()
        self._buy_button = hub.get_buy_button()
        self._cur_player_name = ""
        self._game_over = False
        self._victory_lap = 0
        self._lap_max = 20

    def next_player_turn(self, cur_player):
        """ Indexes through the players list and sets the current player = next player."""
        player_list = get_players_as_list(self._reg)
        cur_index = player_list.index(cur_player)
        if cur_index < len(player_list) - 1:
            next_player = player_list[player_list.index(cur_player) + 1]
        else:
            next_player = player_list[0]
        self._cur_player_name = next_player
        self.check_if_bankrupt(next_player)

    def check_if_bankrupt(self, name):
        """ Checks if a player is bankrupt, if they are it skips their turn. """
        players = get_players(self._reg)
        next_player = players[name]
        money = next_player.get_balance()
        if money <= 0:
            self.next_player_turn(name)
        else:
            self.set_cur_player(name)

    def move_player(self, num_spaces):
        """ If there is a player, moves the player.  Otherwise, it creates a player."""
        if self._cur_player_name != '':
            self._movement.move_player(self._cur_player_name, num_spaces)
            self._reg.move_player(self._cur_player_name, num_spaces)
            self.next_player_turn(self._cur_player_name)
            self.check_for_ai_logic()
        else:
            self._add_button.add_player_button_press()
            self.set_cur_player()

    def set_cur_player(self, name=None):
        """ Sets the current player, then updates the current player display in the GUI. """
        if name is None:
            players_list = get_players_as_list(self._reg)
            self._cur_player_name = players_list[0]
        else:
            self._cur_player_name = name
        player = self._cur_player_name
        self._stats.show_cur_player_stats(player)
        self._buy_button.set_buy_button_color(player)

    def check_for_ai_logic(self):
        """ Checks to see if player needs to use AI logic. """
        players = get_players(self._reg)
        player = players[self._cur_player_name]
        ai_logic = player.get_ai()
        if ai_logic:
            self._dice_button.hide_dice()
            self.do_ai_logic()
        else:
            self._dice_button.show_dice()

    def do_ai_logic(self):
        """ A very simple AI. """
        try:
            if self.should_ai_buy_space():
                self._canvas.after(100, self.buy_space())
            if self.ai_victory_lap():
                self._canvas.after(100, self._dice_button.roll_dice())
        except:
            # Prevents error when closing a game made up entirely of AI players.
            pass

    def ai_victory_lap(self):
        """ Some logic to determine what to do when only AI players remain.  (Prevents recursion depth errors)
        First if the game lasts for 20 rounds, it picks an arbitrary winner (it awards that player 10k).
        Then after an AI has won the game the AI circles the map a few times then the game closes. """
        if self._victory_lap == 20:
            self.pick_arbitrary_winner()
        if not self.humans_active():
            self._victory_lap += 1
        if self._game_over:
            self._victory_lap += 2
        if self._victory_lap > self._lap_max:
            self._reg.quit_game()
            return False
        return True

    def humans_active(self):
        """ Checks to see if any human players are active. """
        players = get_players(self._reg)
        for player in players:
            if not players[player].get_ai():
                bal = players[player].get_balance()
                if bal > 0:
                    return True
        self._lap_max = 100
        return False

    def pick_arbitrary_winner(self):
        """ Gives an arbitrary AI player 100,000$ so that the AI only game will end soon. """
        players = get_players(self._reg)
        cur_player = players[self._cur_player_name]
        cur_player.set_balance(100000)
        for player in players:
            if player != self._cur_player_name:
                bal = players[player].get_balance()
                if bal > 0:
                    bal = bal - 25
                    players[player].set_balance(-bal)

    def should_ai_buy_space(self):
        """ A few simple conditions to determine weather or not the AI should buy a space. """
        bal = self._reg.get_player_account_balance(self._cur_player_name)
        pos = self._reg.get_player_current_position(self._cur_player_name)
        if pos > 0:
            spaces = get_spaces(self._reg)
            space = spaces[pos]
            price = space.get_purchase_amt()
            if self.ai_should_keep_saving(bal, price):
                return False
            if random.randint(1, 10) > 8:
                # 20% chance AI will try to buy any space they land on.
                return True
            if self.is_space_prime_real_estate(bal, price):
                return True
        return False

    def ai_should_keep_saving(self, bal, price):
        """ Simple AI logic to determine if the AI should save up. """
        if price * 1.4 <= bal and 500 < bal < 1500:
            if random.randint(1, 10) <= 9:
                # It's a pretty good idea to save but 10% chance they won't (simulate impulsive decision-making)
                return True
        return False

    def is_space_prime_real_estate(self, bal, price):
        """ Simple AI logic to simulate human player behaviour.
        If the space is prime real estate or the AI has plenty of money, they will try to buy the space they are on. """
        if bal >= 2600:
            # If AI has a very large amount of money, buy any space the AI lands on.
            return True
        if bal >= price + 100 and price >= 750:
            return True
        if price >= 1000 and 1000 < bal < 1500:
            return True
        if price >= 1500 and bal >= 1500:
            return True
        return False

    def buy_space(self):
        """ If the current player can buy the space they are on, they buy it, and it changes color. """
        player = self._cur_player_name
        if self._reg.buy_space(player):
            self._buy_button.modify_space_color(player)
            self._buy_button.set_buy_button_color(player)
            self._stats.show_cur_player_stats(player)

    def player_bankrupt(self, name):
        """ Removes the fill color from a bankrupt players GUI element. """
        players = get_players(self._reg)
        player = players[name]
        player_gui = player.get_gui_element()
        player_color = self._canvas.itemcget(player_gui, "fill")
        if player_color != "":
            self._canvas.itemconfig(player_gui, fill="", outline=player_color)

    def empty_bankrupt_space(self, space):
        """ Removes the fill color from a bankrupt players previously owned space. """
        space = space.get_gui_element()
        color = self._canvas.itemcget(space, "fill")
        self._canvas.itemconfig(space, fill="", outline=color)

    def check_for_winner(self):
        """ Checks to see if the game is over. """
        winner = self._reg.check_game_over()
        if winner != "":
            self.game_is_over(winner)

    def game_is_over(self, winner):
        """ The game is over, sets all spaces on the board to match the winning players fill color. """
        players = get_players(self._reg)
        player = players[winner]
        player_gui = player.get_gui_element()
        color = self._canvas.itemcget(player_gui, "fill")
        spaces = get_spaces(self._reg)
        for space in spaces:
            gui = space.get_gui_element()
            self._canvas.itemconfig(gui, fill=color)
        self._game_over = True


class GuiPlayer:
    """ Creates the GUI representation of the player object. """

    def __init__(self, canvas, color="red", shape_key="d"):
        self._canvas = canvas
        self._color = color
        self._shape_key = shape_key

    def create_player(self):
        """ Creates the GUI representation of the player object. """
        points = [0, 0, 100, 0, 100, 100, 0, 100]
        if self._shape_key == "d":
            points = draw_a_dragon()
        if self._shape_key == "m":
            points = draw_a_mage()
        if self._shape_key == "u":
            points = draw_a_unicorn()
        if self._shape_key == "k":
            points = draw_a_knight()
        new_player = self._canvas.create_polygon(points, outline="black", fill=self._color, width=2)
        return new_player


def get_players(real_estate_game):
    """ Gets the player dictionary as it currently is in the real estate game. """
    players = real_estate_game.get_all_players()
    return players


def get_spaces(real_estate_game):
    """ Gets the spaces list as it currently is in the real estate game. """
    spaces = real_estate_game.get_all_spaces()
    return spaces


def get_players_as_list(real_estate_game):
    """ Returns a list of all player names. """
    players = get_players(real_estate_game)
    players_list = list(players.keys())
    return players_list


def get_cur_player_color(canvas, real_estate_game, cur_player):
    """ Returns the color of the current player. """
    player = real_estate_game.get_player_object(cur_player)
    player_gui = player.get_gui_element()
    player_color = canvas.itemcget(player_gui, "fill")
    return player_color


def draw_a_dragon():
    """ Draws a dragon using a large set of grid points. """
    points = [(5, 5), (20, 10), (25, 15), (25, 30), (40, 35), (45, 27.5), (35, 10), (80, 15), (85, 30),
              (80, 40), (90, 30), (95, 25), (95, 20), (97.5, 27.5), (102.5, 25), (105, 30), (112.5, 31.5),
              (110, 40), (103, 40), (97.5, 40), (85, 51.5), (85, 52.5), (94, 57), (101.5, 57), (101.5, 60.5),
              (94, 60.5), (80, 55), (75, 50), (55, 55), (56, 60), (45, 60), (45, 65), (51, 65), (51, 70), (40, 70),
              (40, 51), (47.4, 51), (15, 35), (17.5, 17.5)]
    return points


def draw_a_mage():
    """ Draws a wizard using a large set of grid points. """
    points = [(60, -15), (60, 25), (65, 25), (65, 28), (60, 28), (55, 40), (65, 50), (65, 65),
              (60, 65), (60, 50), (50, 45), (55, 55), (60, 80), (45, 80), (47, 55), (45, 45), (40, 55),
              (30, 60), (33, 80), (30, 80), (20, 30), (15, 30), (15, 25), (23, 20), (27, 22), (25, 25), (23, 29),
              (28, 55), (37, 53), (45, 40), (42, 40), (40, 28), (35, 28), (35, 25), (40, 25)]
    return points


def draw_a_unicorn():
    """ Draws a unicorn using a large set of grid points. """
    points = [(100, 0), (75, 25), (85, 35), (80, 45), (70, 40), (65, 35), (60, 40), (60, 45), (85, 65),
              (85, 70), (80, 70), (75, 65), (60, 55), (60, 65), (40, 70), (40, 65), (50, 60), (45, 55),
              (30, 55), (25, 65), (25, 70), (35, 80), (25, 80), (20, 70), (20, 67), (18,57), (5, 70),
              (0, 55), (8, 55), (8, 60), (18, 50), (5, 45), (3, 40), (5, 13), (17, 28), (19, 32), (19, 35),
              (35, 30), (50, 30), (60, 20), (60, 15), (65, 20), (70, 20)]
    return points


def draw_a_knight():
    """ Draws a knight using a large set of grid points. """
    points = [(45, 10), (55, 10), (60, 15), (60, 25), (55, 30), (62, 30), (70, 45), (80, 45), (80, 43), (75, 43),
              (75, 40), (80, 40), (80, 0), (85, 40), (90, 40), (90, 43), (85, 43), (85, 55), (80, 55), (80, 50),
              (70, 50), (60, 38), (65, 75), (38, 75), (40, 60), (25, 75), (15, 55), (15, 35), (30, 30), (37, 33),
              (40, 30), (45, 30), (40, 25), (40, 15)]
    return points
