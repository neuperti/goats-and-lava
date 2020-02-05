"""A german game called 'Schiffe Versenken', but this command line based."""

import random
import logic.main as main
import logic.cmd_parser as cmd_module
cmd_parser = cmd_module.cmd_parser


__author__ = "7157367, Seiffert"
__credits__ = "To my loving mother, sister, and for the sake of humanity."
__email__ = "philipp-seiffert@gmx.de"


class Board(main.Board):
    def __init__(self, queue, *args):
        main.Board.__init__(self, *args)
        self.queue = queue

    def change_size(self, new_size):
        """Changes the size of the board."""
        self.size = new_size
        self.clear()
        for x in range(1, new_size+1):
            for y in range(1, new_size+1):
                self.add((x, y))

    def main_loop(self):
        """The main loop, in which all actions are performed."""
        player_names = list(self.player_fleets.keys())
        actual_player = random.randint(0, len(player_names) - 1)
        print("The lucky first player is... " + player_names[actual_player] + "!")
        while len(self.player_fleets) > 1:
            player_name = player_names[actual_player]
            if player_name not in self.player_fleets:
                print(player_name, "is already on the bottom of the sea, thus skipped!")
            else:
                print(player_name + " will now do their turn!")
            self.bombard_fleet(player_name)
            actual_player = (actual_player + 1) % len(player_names)
        print(list(self.player_fleets.keys())[0], "won by staying alive for the longest!")

    def initialize_fleets(self):
        """Lets users create new fleets:"""
        print("You are now within the process of setting up all fleets for the battle.")
        active_player = None
        while True:
            order = None
            try:
                order, arguments = cmd_parser(
                    self,
                    initialisation_mode=True,
                    player_whose_turn_it_is=active_player
                )
            except RuntimeError:
                pass
            if order is None:
                pass
            elif order == "switched to":
                active_player = arguments
            elif order == "deleted":
                if active_player not in self.player_fleets:
                    active_player = None
            elif order == "finished setup":
                break
            elif order == "make ship":
                try:
                    fleet = self.player_fleets[active_player]
                    fleet.add_ship(Ship(fleet, *arguments))
                except:
                    # We'll try an other time ;)
                    continue
            else:
                raise ValueError(
                    "This should not be like this: "
                    + str(order) + ", " + str(arguments)
                )

    def bombard_fleet(self, own_name):
        """allows user to bomb his enemies."""
        while True:
            # Try to get a valid order and try again if you don't
            order = None
            try:
                order, arguments = cmd_parser(
                    self,
                    initialisation_mode=False,
                    player_whose_turn_it_is=own_name
                )

            except RuntimeError:
                pass
            if order is None:
                pass
            elif order is "shoot":
                successful_hit = self.shoot_at_given_positions(arguments, own_name)
                if successful_hit:
                    print("Successfully hit " + str(successful_hit) + " targets!")
                else:
                    print("Awww naaah, you missed...")
                    break
            else:
                raise Exception("This shouldn't happen:", order, arguments)


class Ship(main.Ship):
    pass


def start_game(queue, board):
    print(board.intro)
    board.initialize_fleets()
    board.main_loop()