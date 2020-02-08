"""A german game called 'Schiffe Versenken'"""

import random
from tkinter.messagebox import askyesno
from gui.show_defeat import die_from_being_killed

__author__ = "6666888, Neuperti, 7157367, Seiffert"
__credit__ = "immense time pressure"
__email__ = "s8978466@stud.uni-frankfurt.de"


class Board(set):
    """A board representing the visual boundaries of the ship."""

    intro = open("logic/intro.txt", "r").read()

    def __init__(self, size=10):
        """Initializes the board."""
        set.__init__(self)
        self.size = size
        for x in range(1, size+1):
            for y in range(1, size+1):
                self.add((x, y))
        self.player_fleets = dict()  # a dict which contains a fleet for every player name.

    def main_loop(self):
        """The main loop, in which all actions are performed."""
        player_names = list(self.player_fleets.keys())
        actual_player = random.randint(0, len(player_names) - 1)
        print("The lucky first player is... " + player_names[actual_player] + "!")
        while len(self.player_fleets) > 1:
            # let all players do their job until only one of them is left...
            player_name = player_names[actual_player]
            if player_name not in self.player_fleets:
                print(player_name, "is already on the bottom of the sea, thus skipped!")
            else:
                input(player_name + " will now do their turn; look away, guys, and press enter! ")
                print("\n" * 100)
                self.bombard_fleet(player_name)
                print("\n" * 100)
            actual_player = (actual_player + 1) % len(player_names)
        print(list(self.player_fleets.keys())[0], "won by staying alive for the longest!")

    def initialize_fleets(self):
        """Lets users create new fleets:"""
        print("We will now go through the process of setting up all fleets for the battle.")
        while True:
            # check if new fleet should be added:
            if len(self.player_fleets) >= 2:
                print("(Enter f to finish)", end=" ")
            new_fleet_name = input("Enter a new players name: ")
            if len(self.player_fleets) >= 2 and new_fleet_name == "f":
                # finished board setup!
                break
            self.player_fleets[new_fleet_name] = Fleet(self, new_fleet_name)
            self.player_fleets[new_fleet_name].initialize_fleet()
            print("\n" * 100)

    def shoot_at_given_positions(self, pos, own_name):
        """Lets the player shoot at a location and try to get as many other ships as possible."""
        successes = 0
        for player_name in list(self.player_fleets.keys()):
            if player_name != own_name:
                if pos in (
                    self.player_fleets[own_name].positions_missed
                    | self.player_fleets[own_name].positions_hit
                ):
                    if askyesno("Rock + Rock = Rock", "Do you really want to shoot at rocks?"):
                        self.queue.print_queue.append("Okay, then.")
                    else:
                        self.queue.print_queue.append(
                            "That's wiser. I'll count this wisdom as hitting 0.1 boats, take it\
as a cookie!")
                        return 0.1
                fleet = self.player_fleets[player_name]
                hit = fleet.shoot_at_given_position(pos)
                if hit:
                    self.player_fleets[own_name].positions_hit.add(pos)
                    successes += 1
                else:
                    self.player_fleets[own_name].positions_missed.add(pos)
        return successes

    def bombard_fleet(self, own_name):
        """Manages the bombardment of the opposing fleet"""
        # draw our own fleet:
        self.player_fleets[own_name].draw_defensive()
        # start the shooting!:
        while True:
            # draw the board:
            self.player_fleets[own_name].draw_offensive()
            # get an input:
            while True:
                # Try to get a valid order and try again if you don't
                try:
                    target_position = tuple(int(i) for i in input("Where to shoot? : ").split())
                    if len(target_position) != 2:
                        raise ValueError("Must be two ints separated by a single whitespace.")
                    if target_position not in self:
                        print("Your target is not within the board.")
                        continue
                    if target_position in self.player_fleets[own_name].positions_missed:
                        confirm = input("You already missed here. Enter Y to try a second time: ")
                        if confirm != "Y":
                            continue
                    if target_position in self.player_fleets[own_name].positions_hit:
                        confirm = input("You already hit here. Enter Y to try a second time: ")
                        if confirm != "Y":
                            continue
                    break
                except:
                    print("""You MUST enter two ints separated by a single whitespace, the first
one being the row, the second one being the column.""")
                    continue
            # test if we hit:
            successful_hit = self.shoot_at_given_positions(target_position, own_name)
            if successful_hit:
                print("Successfully hit " + str(successful_hit) + " targets!")
            else:
                print("Awww naaah, you missed...")
                break
        # exit turn!
        input("Press enter to finish turn!")
        print("\n" * 100)


class Fleet(set):
    """Represents a players fleet of ships."""
    def __init__(self, board, player_name):
        """Initializes a ship with the fleet."""
        set.__init__(self)
        self.board = board
        self.ships = list()
        self.positions_hit = set()
        self.positions_missed = set()
        self.player_name = player_name
        self.taken_hits = set()

    def initialize_fleet(self):
        """Initializes the fleet by adding boats."""
        print("You will now initialize your fleet.")
        print(
"You have at least 2 ships and 10% of the field covered, and you may not cover more than 25%."
        )
        while True:
            # We can finish once we have a board coverage of at least 10% and at least 2 ships:
            if len(self) > len(self.board) * .1 and len(self.ships) >= 2:
                finish = input("Enter f to finish: ")
                if finish == "f":
                    break
            # Ask for the ships position:
            while True:
                try:
                    ship_position = tuple(int(i) for i in input("Ship position: ").split())
                    if len(ship_position) != 2:
                        raise ValueError("Must be two ints separated by a single whitespace.")
                    break
                except:
                    print("Must be two ints separated by a single whitespace.")
            # ask for ship length:
            while True:
                try:
                    length = int(input("Ship length: "))
                    break
                except:
                    print("Must be an int.")
            # ask for ship direction:
            while True:
                try:
                    direction = input("Expansion direction of the ship: (n/s/o/w): ")
                    if direction not in {"n", "s", "o", "w"}:
                        raise ValueError("Direction must be one of n, s, o and w.")
                    direction = {
                        "n": [-1, 0],
                        "s": [1, 0],
                        "o": [0, 1],
                        "w": [0, -1]
                    }[direction]
                    break
                except:
                    print("Direction must be one of n, s, o and w.")
            # try to add the ship:
            try:
                self.add_ship(Ship(self, ship_position, length, direction))
                self.draw_defensive()
            except:
                # We'll try an other time ;)
                continue

    def is_defeated(self):
        """Handles own defeat by deleting self from board."""
        del self.board.player_fleets[self.player_name]
        die_from_being_killed(self.player_name)

    def add_ship(self, ship: set):
        """Adds a ship to the board, where the ship is a set of positions tuples."""
        self.update(ship)
        self.ships.append(ship)
        self.draw_defensive()

    def draw_defensive(self):
        """Draws the state of the fleet."""
        # optional To Do: adding stone on grass
        self.board.queue.draw_queue.append((
            "grass",
            ("lava", self),
            ("stone_lava", self.taken_hits),
        ))

    def draw_offensive(self):
        """Draws the board for a specific player to shoot."""
        self.board.queue.draw_queue.append((
            "blank",
            ("stone_lava", self.positions_hit),
            ("stone_grass", self.positions_missed)
        ))

    def shoot_at_given_position(self, pos):
        """Shoots at the given position and triggers all the consequences.
        Returns if the player is allowed an other shot."""
        if pos in self:
            self.board.queue.print_queue.append("you hit a boat! ...of player " + self.player_name)
            self.remove(pos)
            self.taken_hits.add(pos)
            for ship in list(self.ships):
                if pos in ship:
                    ship.remove(pos)
                    if not ship:
                        self.board.queue.print_queue.append("Yay! You sank the ship! ...of player "
                                                            + self.player_name)
            if not self:
                self.board.queue.print_queue.append("You destroyed an entire fleet! ...of player "
                                                    + self.player_name)
                self.is_defeated()
            return True
        else:
            return False


class Ship(set):
    """Represents a ship."""
    def __init__(self, fleet, pos, length, direction):
        """Initializes the ship:"""
        set.__init__(self)
        positions = {
            (
                pos[0] + direction[0] * i,
                pos[1] + direction[1] * i
            ) for i in range(length)
        }
        if length > 6:
            fleet.board.queue.print_queue.append("Ships may not be longer than 6 fields.")
            raise ValueError("Ships may not be longer than 6 fields.")
        if length < 3:
            fleet.board.queue.print_queue.append("Ships must be at least 3 fields long.")
            raise ValueError("Ships must be longer than 3 fields long..")
        if positions & fleet != set():
            fleet.board.queue.print_queue.append(
                "Couldn't add this ship because it intersects with other ships in",
                " and ".join(list(str(i) for i in (positions & fleet)))
            )
            raise ValueError(
                "Couldn't add this ship because it intersects with other ships in",
                " and ".join(list(str(i) for i in (positions & fleet)))
            )
        if positions & fleet.board != positions:
            fleet.board.queue.print_queue.append(
                "couldn't add this ship because it's off the board in",
                " and ".join(list(str(i) for i in (positions - fleet.board)))
            )
            raise ValueError(
                "couldn't add this ship because it's off the board in",
                " and ".join(list(str(i) for i in (positions - fleet.board)))
            )
        if len(positions) + len(fleet) > len(fleet.board) * .25:
            fleet.board.queue.print_queue.append("Your fleet may maximally cover 25% of the field.")
            raise ValueError("Your fleet may maximally cover 25% of the field.")

        self.update(positions)


def start_game():
    """Start a game and run it!"""
    print(Board.intro)
    try:
        board_size = int(input("Enter your board size or nothing to keep the default (10): "))
    except:
        print("Kept the defaults.")
        board_size = 10
    board = Board(size=board_size)
    board.initialize_fleets()
    board.main_loop()


def main():
    """The loop to start and restart games:"""
    start_game()


if __name__ == "__main__":
    main()
