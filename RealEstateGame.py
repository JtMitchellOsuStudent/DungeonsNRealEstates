# Author: JT Mitchell
# GitHub username: JtMitchellOsuStudent
# Date: 6/1/22
# Description: Week 9 - Portfolio Project - BORING VERSION - final draft.
# Description: RealEstateGame.py contains a number of classes and methods for creating and playing a monopoly-esque
# game called Real Estate Game (THIS VERSION IS BORING BECAUSE IT DOES NOT ALLOW FOR GUI - SEE FUN VERSION)

# Code Outline:
# 4 classes 'RealEstateGame', 'GameSpace', 'GoSpace', 'Player'
# RealEstateGame:  Contains methods and variables to simulate playing a monopoly-esque game.
# GameSpace:  Contains methods and variables that pertain to each space on the board.
# GoSpace:  A child class of GameSpace that represents the first space on the board.
# Player:  Contains methods and variables that pertain to a player game object.


class RealEstateGame:
    """ Represents the Real Estate Game, played with the standard rules specified by the assignment readme file. """

    def __init__(self):
        self._spaces = []
        self._players = {}

    def create_spaces(self, go_amt, rent_amounts):
        """ Creates all spaces for the game board. """
        self.create_go_space(go_amt)
        self.create_real_estate_spaces(rent_amounts)

    def create_go_space(self, go_amt):
        """ Creates the GO space for the game board. """
        go_space = GoSpace(go_amt, "GO", None)
        self._spaces.append(go_space)

    def create_real_estate_spaces(self, rent_amounts):
        """ Creates the real estate spaces for the game board. """
        theme = fantasy_theme()  # sets the naming convention for the spaces.
        for index in range(0, 24):
            new_space = GameSpace(theme[index], rent_amounts[index])
            self._spaces.append(new_space)

    def create_player(self, name, money):
        """ Creates a new player object and adds it to the players list. """
        name = self.repeated_name_check(name)
        new_player = Player(name, money, 0)
        self._players[name] = new_player

    def repeated_name_check(self, name):
        """ If the given name exists in the players list, modifies the name.  Otherwise, returns the given name. """
        if name in self._players.keys():
            return self.modify_repeat_names(name, 1)
        else:
            return name

    def modify_repeat_names(self, name, count):
        """ Recursively counts how many copies of the name there are in the players list
        and returns a modified version of the name concatenated with the number of copies. """
        mod_name = f"{name} ({count})"
        if mod_name in self._players.keys():
            return self.modify_repeat_names(name, count + 1)
        else:
            return mod_name

    def buy_space(self, name):
        """ If the player can buy the space, they buy the space and returns True, otherwise returns False."""
        pos = self.get_player_current_position(name)
        space = self.get_game_space_object(pos)
        player = self.get_player_object(name)
        return space.try_to_buy(player)

    def move_player(self, name, num_spaces):
        """ Moves the player, if they are not bankrupt. """
        if self.get_player_account_balance(name) == 0:
            return

        new_pos = self.determine_new_pos(name, num_spaces)
        self.set_player_current_position(name, new_pos)
        self.does_player_owe_rent(name, new_pos)

    def determine_new_pos(self, name, num_spaces):
        """ Determines the new position the player will move to. """
        new_pos = num_spaces + self.get_player_current_position(name)
        if new_pos > 24:
            new_pos = new_pos - 25
            self.pass_go(name)
        return new_pos

    def pass_go(self, name):
        """ Increase the player objects account balance by the GO space payout amount. """
        go = self._spaces[0]
        go_payout = go.get_payout()
        player = self.get_player_object(name)
        player.set_balance(go_payout)

    def does_player_owe_rent(self, name, pos):
        """ Checks to see if the space is free.  If the space is not free, then player pays rent. """
        space = self.get_game_space_object(pos)
        owner = space.get_owner()
        if owner is None or pos == 0:
            return
        elif owner.get_name() == name:
            return
        else:
            self.pay_rent(name, space.get_rent(), owner)

    def pay_rent(self, name, rent, owner):
        """ Transfers rent money from the player to the players current space owner. """
        player = self.get_player_object(name)
        player_bal = self.get_player_account_balance(name)

        if player_bal > rent:
            self.transfer_money(player, owner, rent)
        else:
            self.transfer_money(player, owner, player_bal)
            self.player_is_bankrupt(name)

    @staticmethod
    def transfer_money(sender, receiver, amount):
        """ Transfers money from the sender to the receiver. """
        sender.set_balance(-amount)
        receiver.set_balance(amount)

    def player_is_bankrupt(self, name):
        """ For all spaces the bankrupt player owns, sets those spaces to be owned by None.
        If GUI is active, handles the bankrupt player in the GUI. (Managed here to prevent repeat iterations)."""
        for space in self._spaces:
            owner = space.get_owner()
            if owner and owner.get_name() == name:
                space.set_owner(None)

    def check_game_over(self):
        """ Checks to see if there is more than 1 active player.
        If only one remains returns the winners name, otherwise returns an empty string. """
        active_players = self.get_active_players()
        if len(active_players) > 1:
            return ""
        else:
            return active_players[0]

    def get_active_players(self):
        """ Returns a list of the names of all players whose account balance is greater than zero. """
        active_players = []
        for player in self._players:
            player_obj = self._players[player]
            if player_obj.get_balance() > 0:
                active_players.append(player_obj.get_name())
        return active_players

    def get_player_account_balance(self, name):
        """ Returns player account balance. """
        player = self.get_player_object(name)
        return player.get_balance()

    def get_player_current_position(self, name):
        """ Returns players current position int. """
        player = self.get_player_object(name)
        return player.get_position()

    def set_player_current_position(self, name, pos):
        """ Sets the players current position int. """
        player = self.get_player_object(name)
        player.set_position(pos)

    def get_game_space_object(self, pos):
        return self._spaces[pos]

    def get_player_object(self, name):
        return self._players[name]

    def get_all_players(self):
        return self._players

    def get_all_spaces(self):
        return self._spaces


class GameSpace:
    """ Represents a real estate game space object. """

    def __init__(self, name, rent_amt):
        self._name = name
        self._rent = rent_amt
        self._owner = None

    def try_to_buy(self, player):
        """ Takes a player object as an argument.  If that player can afford this game space object, then they buy it
        and the method returns True, otherwise returns False. """
        purchase_amount = self.get_purchase_amt()
        player_balance = player.get_balance()
        if player_balance > purchase_amount and self._owner is None:
            self._owner = player
            player.set_balance(-purchase_amount)
            return True
        else:
            return False

    def get_name(self):
        return self._name

    def get_rent(self):
        return self._rent

    def get_purchase_amt(self):
        return self._rent * 5

    def get_owner(self):
        return self._owner

    def set_owner(self, new_owner):
        self._owner = new_owner


class GoSpace(GameSpace):
    """ A child object of the GameSpace class that represents the 'GO' space game object. """

    def __init__(self, payout, name, rent_amt):
        super().__init__(name, rent_amt)
        self._payout = payout
        self._rent = None

    def get_payout(self):
        return self._payout

    def try_to_buy(self, player):
        return False

    def set_owner(self, new_owner):
        return None

    def get_purchase_amt(self):
        return None


class Player:
    """ Represents a player object. """

    def __init__(self, name, money, position):
        self._name = name
        self._money = money
        self._pos = position

    def set_balance(self, amount):
        """ A positive amount increases balance and a negative one decreases it. """
        self._money += amount

    def get_name(self):
        return self._name

    def get_balance(self):
        return self._money

    def get_position(self):
        return self._pos

    def set_position(self, new_position):
        self._pos = new_position


def fantasy_theme():
    """ Returns a list with fantasy themed names. """
    theme = ["Druids Camp", "Dragons Lair", "Elves Keep", "Fairy Meadow",
             "Ghouls Gate", "Gnomes Guild", "Goblin Cave", "Giants Hill",
             "Hydras Hideout", "Kobolds Stronghold", "Lichs Domain",
             "Mimics Mouth", "Ogres Pit", "Skeletons Grave",
             "Dwarves Mine", "Trolls Tower", "Unicorn Falls",
             "Vampires Crypt", "Wyvern Woods", "Zombie Inn",
             "Werewolf Ridge", "Mages Fire", "Warlocks Cove",
             "Halfling Holm"
             ]
    return theme

