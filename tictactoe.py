#!/usr/bin/env python3

# Import modules
from game import Game
import players
import argparse

# List of possible players
player_list = (
    "human", "random", "minimax"
)

# Setup argparse
parser = argparse.ArgumentParser(
    prog='Super Tic Tac Toe',
    description=
        """Super Tic Tac Toe is just like regular Tic Tac Toe, 
            except the board is 9x9. This game can be played with humans,
            random AI players, and intelligent minimax AI players."""
)
parser.add_argument(
    "player-1",
    help="Type of first player",
    choices=player_list,
    type=str
)
parser.add_argument(
    "--depth-1",
    help="Maximum depth of minimax player",
    nargs='?',
    action='store',
    type=int,
    default=2
)
parser.add_argument(
    "--delay-1",
    help="Delay time (s) of random player",
    nargs='?',
    action='store',
    type=float,
    default=0.5
)
parser.add_argument(
    "--name-1",
    help="Name of first player",
    nargs='?',
    action='store',
    type=str,
    default='Player 1'
)
parser.add_argument(
    "player-2",
    help="Type of second player",
    choices=player_list,
    type=str
)
parser.add_argument(
    "--depth-2",
    help="Maximum depth of minimax player",
    nargs='?',
    action='store',
    type=int,
    default=2
)
parser.add_argument(
    "--delay-2",
    help="Delay time (s) of random player",
    nargs='?',
    action='store',
    type=float,
    default=0.5
)
parser.add_argument(
    "--name-2",
    help="Name of second player",
    nargs='?',
    action='store',
    type=str,
    default='Player 2'
)

if __name__ == "__main__":
    # Parse arguments
    args = parser.parse_args()
    print(args)
    # Set players accordingly
    player1, player2 = None, None
    # Set player 1
    p1 = getattr(args,'player-1')
    if p1 == "human":
        player1 = players.HumanPlayer(args.name_1)
    elif p1 == "random":
        player1 = players.RandomAIPlayer(args.name_1, delay=args.delay_1)
    elif p1 == "minimax":
        player1 = players.MinimaxAIPlayerV1(args.name_1,max_depth=args.depth_1)
    # Set player 2
    p2 = getattr(args,'player-2')
    if p2 == "human":
        player2 = players.HumanPlayer(args.name_2)
    elif p2 == "random":
        player2 = players.RandomAIPlayer(args.name_2, delay=args.delay_2)
    elif p2 == "minimax":
        player2 = players.MinimaxAIPlayerV1(args.name_2,max_depth=args.depth_2)
    # Run game
    game = Game(player1,player2)
    game.run()