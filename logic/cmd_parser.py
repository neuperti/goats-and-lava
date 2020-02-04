"""Some helper functions for our command line interface."""


__author__ = "7157367, Seiffert"
__credits__ = """To my loving mother, sister, and for the sake of humanity."""
__email__ = "philipp-seiffert@gmx.de"


import sys
import subprocess
import main

running_a_test = list()


def test_input(start_inputs=[
    line.split(">>> ")[1] for line in open("example_game.txt", "r").read().split("\n")
    if ">>> " in line
][1:]):
    new_input = start_inputs.pop(0)
    print("--> " + new_input)
    return new_input


COMMANDS = {
    # Question-Options (?):
    "?i",  # Show info.txt
    "?c",  # Show commands.txt

    # Display-functions (d):
    "df",  # Display flush (prints lots of whitespace to hide your input from the next player)
    "dd",  # Shows the defensive board for the current player (the board showing their ships and the
           # hits they took)
    "do",  # Shows the offensive board of the current player (where they hit and where they missed)

    # Player-functions (p):
    "p+",  # [player_name]: Register player of the given name.
    "p-",  # [player_name]: Delete player of the given name.
    "ps",  # [player_name]: Switch to the player of the given name.

    # Ship functions (s):
    "s+",  # [position as two ints] [length as int] [direction as n, s, o or w]: Add a ship of the
           # given length going from the given position into the given direction

    # Initialisation functions:
    "if",  # Finish initialisation. This will fail if some players fleets don't fulfill the
           # requirements.

    # Board functions:
    "bs",  # [size]: Sets the boards size (Only available before any players are registered)
    "bb"   # [position]: Bomb the given position of the Board.
}


NO_ARG_COMMANDS = {
    "?i", "?c",
    "df", "dd", "do",
    "if"
}

ONE_ARG_COMMANDS = {
    "p+", "p-", "ps",
    "bs"
}

TWO_ARG_COMMANDS = {
    "bb"
}

FOUR_ARG_COMMANDS = {
    "s+"
}


class Fleet(main.Fleet):
    def is_ready(self):
        if len(self) > len(self.board) * .1 and len(self.ships) >= 2:
            return True
        else:
            return False


def cmd_parser(board, initialisation_mode=False, player_whose_turn_it_is=None, predefined_input=None):
    """Lets player enter a command and process it."""
    # Take input, which may be predefined:
    if predefined_input is not None:
        command = predefined_input
    else:
        command = ""
        while command == "":
            if running_a_test:
                command = test_input()
            else:
                command = input(">>> ")
        command = command.split()
    order, *arguments = command
    error = None
    # Quit or restart the game:
    if order == "gq":
        sys.exit()
    if order == "gr":
        subprocess.Popen(
            [sys.executable, "main_cmd.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=".",
        )
        sys.exit()

    # error checking for amount of arguments and situation:
    if order not in COMMANDS:
        error = "Command " + order + " does not exist!"
    if order in NO_ARG_COMMANDS and len(arguments) != 0:
        error = "Command " + order + " takes exactly one argument!"
    if order in ONE_ARG_COMMANDS and len(arguments) != 1:
        error = "Command " + order + " takes exactly one argument!"
    if order in TWO_ARG_COMMANDS and len(arguments) != 2:
        error = "Command " + order + " takes only one argument!"
    if order in FOUR_ARG_COMMANDS and len(arguments) != 4:
        error = "Command " + order + " takes exactly 3 arguments!"
    if order in {"dd", "do"} and player_whose_turn_it_is is None:
        error = "There aren't any players in the game yet, so we can't show their current state."
    if order in {"if", "p+", "p-", "ps", "bs", "s+"} and not initialisation_mode:
        error = "The board is already set up, you can't do this right now xD"
    if order == "s+" and not player_whose_turn_it_is:
        error = "You can't add a ship without an active player!"
    elif order == "if":
        player_who_are_not_ready_to_finish_setup = {
            player_name for player_name in board.player_fleets
            if not board.player_fleets[player_name].is_ready()
        }
        if player_who_are_not_ready_to_finish_setup:
            error = (
                "The players "
                + " and ".join(list(player_who_are_not_ready_to_finish_setup))
                + " are not ready to finish their setup, as they don't have 10% of their area"
                + " covered with their fleet or don't have 2 ship yet."
            )
    if order == "if" and len(board.player_fleets) < 2:
        error = "You can't play with less than 2 players xD."
    if order == "bs" and len(board.player_fleets) > 0:
        error = "You can't change the boards size after you registered any players!"
    if order == "bb" and initialisation_mode:
        error = "You can't just bomb around whilst setting up the board, that's a war crime!"

    if not error:
        # doing commands that can always be done:
        if order == "?i":
            with open("intro.txt", "r") as intro:
                print(intro.read())
                return None, None
        if order == "?c":
            with open("commands.txt", "r") as commands:
                print(commands.read())
                return None, None
        if order == "df":
            print("\n" * 100)
            return None, None
        if order == "dd":
            board.player_fleets[player_whose_turn_it_is].draw_defensive()
            return None, None
        if order == "do":
            board.player_fleets[player_whose_turn_it_is].draw_offensive()
            return None, None
        if order == "bs":
            try:
                new_size = int(arguments[0])
                print("Set board size to", new_size)
                board.change_size(new_size)
                return None, None
            except:
                error = "The new size of the board must be an int!"
        if order in {"p+", "p-", "ps"}:
            player_name = arguments[0]
            if order == "p+" and player_name in board.player_fleets:
                error = "There already is a player of this name!"
            elif order == "p+":
                board.player_fleets[player_name] = Fleet(board, player_name)
                print("Created & switched to", player_name + ".")
                return "switched to", player_name
            elif order == "p-" and player_name not in board.player_fleets:
                error = "Player " + player_name + " does not exist and thus can't be deleted!"
            elif order == "p-":
                del board.player_fleets[player_name]
                print("Deleted player", player_name + ".")
                return "deleted", player_name
            elif order == "ps" and player_name not in board.player_fleets:
                error = "Player " + player_name + " does not exist."
            elif order == "ps":
                print("Switched to", player_name + ".")
                return "switched to", player_name
        if order == "if":
            print("Finished setting up the board!")
            return "finished setup", True
        if order == "bb":
            try:
                position = tuple(int(i) for i in arguments)
                return "shoot", position
            except ValueError:
                error = (
                    "Position argument for bombing must be two ints, one for the row and one\n"
                    + "for the column."
                )
        if order == "s+":
            try:
                try:
                    position = (int(arguments[0]), int(arguments[1]))
                except ValueError:
                    error = (
                        "Position must be two ints, one for the row and one for the column, not\n"
                        + " and ".join([str(i) for i in arguments[:2]])
                    )
                    raise ValueError("")
                try:
                    length = int(arguments[2])
                except ValueError:
                    error = "Length of the ship must be an int, not " + arguments[2]
                    raise ValueError("")
                direction = arguments[3]
                if direction not in {"n", "s", "o", "w"}:
                    error = "Direction must be  one of n, s, o and w!"
                else:
                    direction = {
                        "n": [-1, 0],
                        "s": [1, 0],
                        "o": [0, 1],
                        "w": [0, -1]
                    }[direction]
                    return "make ship", (position, length, direction)
            finally:
                pass
    if error:
        print(error)
        raise RuntimeError("Something happened: " + str(error))
    return None, None
