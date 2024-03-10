# Super-TicTacToe
Super Tic Tac Toe is just like regular Tic Tac Toe, except the board is 9x9. This game can be played with humans, random AI players, and intelligent minimax AI players.

## How to Play
Super Tic Tac Toe is started via command line, using the tictactoe.py file. The general structure of the command line arguments is as follows:
```
python3 tictactoe.py {human,random,minimax} [options] {human,random,minimax} [options]
```
You can run
```
python3 tictactoe.py --help
```
for more info on how the command line arguments work.

## Minimax AI
The included AI player employs minimax search with $\alpha-\beta$ pruning to boost search performance. While the current performance strategy noticeably cuts down run time, the search process is still very slow beyond a search depth of 3. To further improve performance I can implement additional strategies, like pre-sorting moves according to a heuristic so better moves are searched first.

## Development Information
Super Tic Tac Toe was developed on MacOS Sonoma (14.2.1) using Python version 3.9.6. 

## Credits
The GUI was created with PyGame, argument parsing with ArgParse, and the rest was done completely by me!