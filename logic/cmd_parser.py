"""Some helper functions for our command line interface."""


__author__ = "6666888, Neuperti, 7157367, Seiffert"
__credit__ = "immense time pressure"
__email__ = "s8978466@stud.uni-frankfurt.de"


import sys
import subprocess
import time
import threading
import logic.main as main
from gui.show_defeat import die_from_being_a_coward
from gui.show_defeat import finish_game


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
    "bb",  # [position]: Bomb the given position of the Board.

    # Quitting/Restarting:
    "gq",  # Quits the game
    "gr",   # Restarts the game

    # Options:
    "one_shoot_per_ship",
    "rock_scattering",
    "thinking_time"
}


NO_ARG_COMMANDS = {
    "?i", "?c",
    "df", "dd", "do",
    "if",
    "gq", "gr"
}

ONE_ARG_COMMANDS = {
    "p+", "p-", "ps",
    "bs",
    "one_shoot_per_ship", "rock_scattering", "thinking_time"
}

TWO_ARG_COMMANDS = {
    "bb"
}

FOUR_ARG_COMMANDS = {
    "s+"
}


class Fleet(main.Fleet):
    """Inherits from the fleet class of main.py"""
    def is_ready(self):
        """Checks if the conditions for a legal fleet are met"""
        if len(self) > len(self.board) * .1 and len(self.ships) >= 2:
            return True
        else:
            return False


def cmd_parser(board, initialisation_mode=False, player_whose_turn_it_is=None):
    """Lets player enter a command and process it."""
    # Take input, which may be predefined:
    command = board.queue.get(remaining_thinking_time=board.thinking_time).split()
    if command[0] == "failed!":
        board.queue.response_queue.append(False)
        return_value = "died from timer!", None
    else:
        return_value = None, None
    order, *arguments = command
    error = None

    # error checking for amount of arguments and situation:
    if order in {
        "one_shoot_per_ship", "rock_scattering", "thinking_time"
    } and not initialisation_mode:
        error = "Command " + order + " only works in initialisation mode!"
    if order not in COMMANDS | {"failed!"}:
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
        error = "You can't just bomb around whilst gardening, that's a war crime!"
    if board.quit:
        error = "You already exited the game, so you can't do this anymore!"

    if not error:
        # doing commands that can always be done:
        if order == "?i":
            with open("logic/intro.txt", "r") as intro:
                board.queue.print_queue.append(intro.read())
                return_value = None, None
        if order == "?c":
            with open("logic/commands.txt", "r") as commands:
                board.queue.print_queue.append(commands.read())
                return_value = None, None
        if order == "thinking_time":
            if not arguments[0].isdigit():
                error = "Thinking time must be a digit!"
            else:
                board.thinking_time = int(arguments[0])
                board.queue.print_queue.append("Thinking time set to", arguments[0])
        if order == "one_shoot_per_ship":
            if arguments[0] == "True":
                board.one_shoot_per_ship = True
                board.queue.print_queue.append(order, " is activated.")
            else:
                board.one_shoot_per_ship = False
                board.queue.print_queue.append(order, " is deactivated.")
        if order == "rock_scattering":
            if arguments[0] == "True":
                board.rock_scattering = True
                board.queue.print_queue.append(order, " is activated.")
            else:
                board.rock_scattering = False
                board.queue.print_queue.append(order, " is deactivated.")
        if order == "df":
            board.queue.print_queue.append("\n" * 100)
            return_value = None, None
        if order == "dd":
            board.player_fleets[player_whose_turn_it_is].draw_defensive()
            return_value = None, None
        if order == "do":
            board.player_fleets[player_whose_turn_it_is].draw_offensive()
            return_value = None, None
        if order == "bs":
            try:
                new_size = int(arguments[0])
                board.queue.print_queue.append("Set board size to", new_size)
                board.change_size(new_size)
                board.queue.draw_queue.append(int(arguments[0]))
                return_value = None, None
            except:
                error = "The new size of the board must be an int!"
        if order in {"p+", "p-", "ps"}:
            player_name = arguments[0]
            if order == "p+" and player_name in board.player_fleets:
                error = "There already is a player of this name!"
            elif order == "p+":
                board.player_fleets[player_name] = Fleet(board, player_name)
                board.queue.print_queue.append("Created & switched to", player_name + ".")
                return_value = "switched to", player_name
            elif order == "p-" and player_name not in board.player_fleets:
                error = "Player " + player_name + " does not exist and thus can't be deleted!"
            elif order == "p-":
                del board.player_fleets[player_name]
                board.queue.print_queue.append("Deleted player", player_name + ".")
                return_value = "deleted", player_name
            elif order == "ps" and player_name not in board.player_fleets:
                error = "Player " + player_name + " does not exist."
            elif order == "ps":
                board.queue.print_queue.append("Switched to", player_name + ".")
                time.sleep(5)
                return_value = "switched to", player_name
        if order == "if":
            board.queue.print_queue.append("Finished setting up the board!")
            return_value = "finished setup", True
        if order == "bb":
            try:
                position = tuple(int(i) for i in arguments)
                return_value = "shoot", position
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
                    return_value = "make ship", (position, length, direction)
            except:
                pass
        # Quit or restart the game:
        if order == "gq":
            board.queue.response_queue.append(True)
            die_from_being_a_coward("someone", board)
            board.quit = True  # meaning we can't enter any commands anymore.
            return_value = None, None
            return None, None
        if order == "gr":
            subprocess.Popen(
                [sys.executable, "main.py"],
                creationflags=subprocess.DETACHED_PROCESS, cwd=".",
            )
            finish_game(board.window)
    if error:
        board.queue.print_queue.append(error)
        board.queue.response_queue.append(False)
        raise RuntimeError("Something happened: " + str(error))
    else:
        board.queue.response_queue.append(True)
    return return_value
