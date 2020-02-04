"""A german game called 'Schiffe Versenken', but this command line based."""

import random
import main
import cmd_parser as cmd_module
cmd_parser = cmd_module.cmd_parser


__author__ = "7157367, Seiffert"
__credits__ = """To my loving mother, sister, and for the sake of humanity."""
__email__ = "philipp-seiffert@gmx.de"


class Board(main.Board):
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


def start_game():
    """Start a game and run it!

    Doctest:

    >>> start_game()
       Ship Destroying
       + ----------- +
    A game about destroying enemy fleets and leaving traumatised wifes, husbands and children grieve
    for the people you killed.
    <BLANKLINE>
    The game consists of the following phases:
    <BLANKLINE>
    (1) Setting the boards width (default is 10).
    (2) Registering the players (at least 2). Each player must have multiple ships, each of whom is a
        row or a column and between 3 and 6 (both ends inclusive) fields long. Each player must plaster
        10-25% of the entire field with its boats. It ships of one player may not overlap with each
        each other, but with ships of other players.
    (3) A starting player is randomly determined.
    (4) The players take turns one after an other, until only one player is left. This player is the
        winner. Players get "destroyed" by having all their shots destroyed.
    (5) In each turn, the player can shoot at random positions until they miss. As there may be more
        than one player and each shot is fired against all players but the one who shot it, a player
        may hit more than one ship with each shot. You will be told the number of ships and the names
        of the players you hit with each shot, and you can view a map showing where you hit and where
        you missed. You can also view a map showing where you where hit and where your ships are
        positioned. Players will be told if they destroy a ship.
    <BLANKLINE>
    The game may be started by running main.py or by running main_cmd.py, the later of whom imports
    the former and runs it with a command line interface instead of the default heavily guided one.
    As ship destroying is a game build open the underlying theme of trust in the original paper
    version (one can always just lie), the cmd-version is trust-based as well. As the order in which
    actions are performed is more free than in the guided version, one can switch more often and one
    manually decides when to flush the screen for privacy reasons and when not to and so on.
    <BLANKLINE>
    If you are running said command-line version, use the command ?c to view a list of all commands.
    <BLANKLINE>
    (Made by Philipp Seiffert)
    <BLANKLINE>
    You are now within the process of setting up all fleets for the battle.
    --> ?i
       Ship Destroying
       + ----------- +
    A game about destroying enemy fleets and leaving traumatised wifes, husbands and children grieve
    for the people you killed.
    <BLANKLINE>
    The game consists of the following phases:
    <BLANKLINE>
    (1) Setting the boards width (default is 10).
    (2) Registering the players (at least 2). Each player must have multiple ships, each of whom is a
        row or a column and between 3 and 6 (both ends inclusive) fields long. Each player must plaster
        10-25% of the entire field with its boats. It ships of one player may not overlap with each
        each other, but with ships of other players.
    (3) A starting player is randomly determined.
    (4) The players take turns one after an other, until only one player is left. This player is the
        winner. Players get "destroyed" by having all their shots destroyed.
    (5) In each turn, the player can shoot at random positions until they miss. As there may be more
        than one player and each shot is fired against all players but the one who shot it, a player
        may hit more than one ship with each shot. You will be told the number of ships and the names
        of the players you hit with each shot, and you can view a map showing where you hit and where
        you missed. You can also view a map showing where you where hit and where your ships are
        positioned. Players will be told if they destroy a ship.
    <BLANKLINE>
    The game may be started by running main.py or by running main_cmd.py, the later of whom imports
    the former and runs it with a command line interface instead of the default heavily guided one.
    As ship destroying is a game build open the underlying theme of trust in the original paper
    version (one can always just lie), the cmd-version is trust-based as well. As the order in which
    actions are performed is more free than in the guided version, one can switch more often and one
    manually decides when to flush the screen for privacy reasons and when not to and so on.
    <BLANKLINE>
    If you are running said command-line version, use the command ?c to view a list of all commands.
    <BLANKLINE>
    (Made by Philipp Seiffert)
    <BLANKLINE>
    --> ?c
       Ship Destroying
       + ----------- +
    Commands:
    <BLANKLINE>
    Question-Options (?):
      ?i: Show info.txt
      ?c: Show commands.txt
    <BLANKLINE>
    Display-functions (d):
      df: Display flush (prints lots of whitespace to hide your input from the next player)
      dd: Shows the defensive board for the current player (the board showing their ships and the hits
          they took)
      do: Shows the offensive board of the current player (where they hit and where they missed)
    <BLANKLINE>
    Player-functions (p):
      Only usable in initialization mode:
      p+ [player_name]: Register player of the given name.
      p- [player_name]: Delete player of the given name.
      ps [player_name]: Switch to the player of the given name.
    <BLANKLINE>
    Ship functions (s):
      Only usable in initialization mode:
      s+ [position as "row column"] [length as int] [direction as n, s, o or w]: Add a ship of the given
         length going from the given position into the given direction
    <BLANKLINE>
    Initialisation functions:
      Only available during setup,  whilst everyone places their boats:
      if: Finish initialisation. This will fail if some players fleets don't fulfill the requirements.
    <BLANKLINE>
    Board functions:
      bs [size]: Sets the boards size (Only available before any players are registered)
      bb [position]: Bomb the given position of the Board.
    <BLANKLINE>
    Game functions:
      gq: Quits the game.
      gr: Restarts the game.
    <BLANKLINE>
    (Made by Philipp Seiffert)
    <BLANKLINE>
    --> bs 10
    Set board size to 10
    --> dd
    There aren't any players in the game yet, so we can't show their current state.
    --> p+ Player_1
    Created & switched to Player_1.
    --> bs 10
    You can't change the boards size after you registered any players!
    --> if
    You can't play with less than 2 players xD.
    --> p- Player_1
    Deleted player Player_1.
    --> bs 10
    Set board size to 10
    --> p+ Player1
    Created & switched to Player1.
    --> s+ 1 1 6 s
    --> dd
    your fleet (# is your boat, x shows sunk boats):
    +----------+
    |#         |
    |#         |
    |#         |
    |#         |
    |#         |
    |#         |
    |          |
    |          |
    |          |
    |          |
    +----------+
    --> s+ 5 1 3 o
    Couldn't add this ship because it intersects with other ships in (5, 1)
    --> s+ 10 10 4 o
    couldn't add this ship because its off the board in (10, 13) and (10, 11) and (10, 12)
    --> s+ 1 2 6 s
    --> s+ 1 3 6 s
    --> s+ 1 4 6 s
    --> s+ 1 5 6 s
    Your fleet may maximally cover 25% of the field.
    --> dd
    your fleet (# is your boat, x shows sunk boats):
    +----------+
    |####      |
    |####      |
    |####      |
    |####      |
    |####      |
    |####      |
    |          |
    |          |
    |          |
    |          |
    +----------+
    --> p+ Player2
    Created & switched to Player2.
    --> if
    The players Player2 are not ready to finish their setup, as they don't have 10% of their area covered with their fleet or don't have 2 ship yet.
    --> ps Player1
    Switched to Player1.
    --> ps Player2
    Switched to Player2.
    --> s+ 10 10 2 n
    Ships must be at least 3 fields long.
    --> s+ 10 10 7 n
    Ships may not be longer than 6 fields.
    --> s+ 10 10 6 n
    --> s+ 10 9 6 n
    --> s+ 10 8 6 n
    --> if
    Finished setting up the board!
    The lucky first player is... Player1!
    Player1 will now do their turn!
    --> df
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    --> p+ Player3
    The board is already set up, you can't do this right now xD
    --> if
    The board is already set up, you can't do this right now xD
    --> s+ 1 1 3 s
    The board is already set up, you can't do this right now xD
    --> bb 1 1
    Awww naaah, you missed...
    Player2 will now do their turn!
    --> bb 1 1
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |x         |
    |          |
    |          |
    |          |
    |          |
    |          |
    |          |
    |          |
    |          |
    |          |
    +----------+
    --> bb 2 1
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 3 1
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 4 1
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 5 1
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 6 1
    you hit a boat! ...of player Player1
    Yay! You sank the ship! ...of player Player1
    Successfully hit 1 targets!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |x         |
    |x         |
    |x         |
    |x         |
    |x         |
    |x         |
    |          |
    |          |
    |          |
    |          |
    +----------+
    --> bb 7 1
    Awww naaah, you missed...
    Player1 will now do their turn!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |~         |
    |          |
    |          |
    |          |
    |          |
    |          |
    |          |
    |          |
    |          |
    |          |
    +----------+
    --> bb 10 10
    you hit a boat! ...of player Player2
    Successfully hit 1 targets!
    --> bb 9 10
    you hit a boat! ...of player Player2
    Successfully hit 1 targets!
    --> bb 9 10
    Awww naaah, you missed...
    Player2 will now do their turn!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |x         |
    |x         |
    |x         |
    |x         |
    |x         |
    |x         |
    |~         |
    |          |
    |          |
    |          |
    +----------+
    --> bb 1 2
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 2 2
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 2 3
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 2 4
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 2 5
    Awww naaah, you missed...
    Player1 will now do their turn!
    --> dd
    your fleet (# is your boat, x shows sunk boats):
    +----------+
    |xx##      |
    |xxxx      |
    |x###      |
    |x###      |
    |x###      |
    |x###      |
    |          |
    |          |
    |          |
    |          |
    +----------+
    --> bb 8 8
    you hit a boat! ...of player Player2
    Successfully hit 1 targets!
    --> bb 8 9
    you hit a boat! ...of player Player2
    Successfully hit 1 targets!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |~         |
    |          |
    |          |
    |          |
    |          |
    |          |
    |          |
    |       xx |
    |         x|
    |         x|
    +----------+
    --> bb 8 10
    you hit a boat! ...of player Player2
    Successfully hit 1 targets!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |~         |
    |          |
    |          |
    |          |
    |          |
    |          |
    |          |
    |       xxx|
    |         x|
    |         x|
    +----------+
    --> bb 8 7
    Awww naaah, you missed...
    Player2 will now do their turn!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |xx        |
    |xxxx~     |
    |x         |
    |x         |
    |x         |
    |x         |
    |~         |
    |          |
    |          |
    |          |
    +----------+
    --> bb 1 3
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> o
    Command o does not exist!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |xxx       |
    |xxxx~     |
    |x         |
    |x         |
    |x         |
    |x         |
    |~         |
    |          |
    |          |
    |          |
    +----------+
    --> bb 1 4
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 3 2
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 3 3
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 3 4
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |xxxx      |
    |xxxx~     |
    |xxxx      |
    |x         |
    |x         |
    |x         |
    |~         |
    |          |
    |          |
    |          |
    +----------+
    --> bb 4 2
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 5 2
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 6 2
    you hit a boat! ...of player Player1
    Yay! You sank the ship! ...of player Player1
    Successfully hit 1 targets!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |xxxx      |
    |xxxx~     |
    |xxxx      |
    |xx        |
    |xx        |
    |xx        |
    |~         |
    |          |
    |          |
    |          |
    +----------+
    --> bb 4 3
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 5 3
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 6 3
    you hit a boat! ...of player Player1
    Yay! You sank the ship! ...of player Player1
    Successfully hit 1 targets!
    --> do
    the board (~ means you missed, x you hit):
    +----------+
    |xxxx      |
    |xxxx~     |
    |xxxx      |
    |xxx       |
    |xxx       |
    |xxx       |
    |~         |
    |          |
    |          |
    |          |
    +----------+
    --> bb 4 4
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 5 4
    you hit a boat! ...of player Player1
    Successfully hit 1 targets!
    --> bb 6 4
    you hit a boat! ...of player Player1
    Yay! You sank the ship! ...of player Player1
    You destroyed an entire fleet! ...of player Player1
    Successfully hit 1 targets!
    --> bb 1 1
    Awww naaah, you missed...
    Player2 won by staying alive for the longest!
    """
    board = Board()
    print(board.intro)
    board.initialize_fleets()
    board.main_loop()


def _test():
    cmd_module.running_a_test.append(1)
    old_randint_function = random.randint
    random.randint = lambda *args: 0
    import doctest
    doctest.testmod()
    cmd_module.running_a_test.clear()
    random.randint = old_randint_function


def main():
    """The loop to start and restart games:"""
    print("[Running test..]", end=" ")
    _test()
    print("[If test printed nothing, that means it was successful!]")
    start_game()


if __name__ == "__main__":
    main()
