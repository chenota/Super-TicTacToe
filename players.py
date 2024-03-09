import random
import time

class HumanPlayer:
    def __init__(self,name):
        self.name = name
    # Human player clicks board to move
    def move(self,board,player,cell_size_x,cell_size_y,padding,pygame):
        # Get list of valid moves
        valid_moves = board.get_valid_moves()
        # Wait for click...
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return None
            # If player clicked...
            elif event.type == pygame.MOUSEBUTTONUP:
                # Get mouse position
                pos_x,pos_y = pygame.mouse.get_pos()
                # Get cell player clicked
                cells = ((pos_x - padding) // cell_size_x, (pos_y - padding) // cell_size_y)
                # If cell is a valid move, return, otherwise wait
                if cells in valid_moves:
                    return cells
            
class RandomAIPlayer:
    def __init__(self,name,delay=0.5):
        self.name = name
        self.delay = delay
    def move(self,board,player,cell_size_x,cell_size_y,padding,pygame):
        # Wait to play
        time.sleep(self.delay)
        # Get list of valid moves
        valid_moves = board.get_valid_moves()
        # Return random choice from list
        return random.choice(valid_moves)
    
class MinimaxAIPlayerV1:
    def __init__(self,name,max_depth=2):
        self.name = name
        self.max_depth = max_depth
        # Pieces towards center of board are more valuable
        self.POSITION_SCORE = [
            [4,  0,  0,  0,  0,  0,  0,  0,  4],
            [0, 10,  7,  7,  7,  7,  7, 10,  0],
            [0,  7, 15, 12, 12, 12, 15,  7,  0],
            [0,  7, 12, 19, 18, 19, 12,  7,  0],
            [0,  7, 12, 18, 23, 18, 15,  7,  0],
            [0,  7, 12, 19, 20, 19, 12,  7,  0],
            [0,  7, 15, 12, 12, 12, 15,  7,  0],
            [0, 10,  7,  7,  7,  7,  7, 10,  0],
            [4,  0,  0,  0,  0,  0,  0,  0,  4],
        ]
        self.nodes = 0
    # Return the other player
    def __other_player(self,player):
        return 2 if player == 1 else 1
    # Score pieces in a line
    def line_score(self,row,player):
        score = 0
        for data in row:
            # Add to score if player is in this row
            if data == player:
                score += 1
            # If you can't win from this row, don't give a score
            elif data == self.__other_player(player):
                return 0
        return score
    # Score of current game state
    def __score(self,board,min_player,max_player):
        # Initialize scores
        max_player_score = 0
        min_player_score = 0
        # Reward players for pieces closest to the middle
        for i in range(9):
            for j in range(9):
                if board.at(i,j) == min_player:
                    min_player_score += 0.5 * self.POSITION_SCORE[i][j]
                elif board.at(i,j) == max_player:
                    max_player_score += 0.5 * self.POSITION_SCORE[i][j]
        # Reward players for having pieces in a line that the enemy hasn't played in yet
        max_line_score = 0
        min_line_score = 0
        # Rows
        for row in board.board:
            max_line_score += self.line_score(row,max_player)
            min_line_score += self.line_score(row,min_player)
        # Columns
        for col in zip(*board.board):
            max_line_score += self.line_score(col,max_player)
            min_line_score += self.line_score(col,min_player)
        # Diagonal left
        diag_left = [board.board[i][i] for i in range(9)]
        max_line_score += self.line_score(diag_left,max_player)
        min_line_score += self.line_score(diag_left,min_player)
        # Diagonal right
        diag_right = [board.board[i][8 - i] for i in range(9)]
        max_line_score += self.line_score(diag_right,max_player)
        min_line_score += self.line_score(diag_right,min_player)
        # Total line score
        max_player_score += 3 * max_line_score
        min_player_score += 3 * min_line_score
        # Reward players for winning
        if board.is_win(min_player):
            min_player_score += 200
        elif board.is_win(max_player):
            max_player_score += 200
        # Player cares more about winning than preventing other player from winning
        return (3 * max_player_score) - (2 * min_player_score)
    # Minimax game state search
    def __minimax(self,board,player,min_player,max_player,depth,alpha,beta,arg=False):
        # Base cases: If reach end game or max depth, return state
        if board.is_win(max_player) or board.is_win(min_player) or board.is_full() or depth <= 0:
            return self.__score(board,min_player,max_player)
        # Search next set of states for max player
        elif player == max_player:
            # Store maximum score and move index that gives it
            max_eval = -float('inf')
            max_idx = None
            # Search each possible move...
            for i,(move_x,move_y) in enumerate(board.get_valid_moves()):
                # Track how many nodes searched
                self.nodes += 1
                # Make a copy of the board
                new_board = board.copy()
                # Max player plays move on board copy
                new_board.set(move_x,move_y,player)
                # Recursively evaluate new game state
                eval = self.__minimax(new_board,
                                min_player,
                                min_player,
                                max_player,
                                depth - 1,
                                alpha,
                                beta)
                # (Possibly) update maximum score
                max_eval = max(max_eval,eval)
                # If new score is max, set max index to index of current move
                if eval == max_eval: 
                    max_idx = i
                # Alpha-beta pruning
                alpha = max(alpha,max_eval)
                if beta < alpha:
                   break
            # Return maximum score, otherwise return idx of max score if specified
            return max_eval if not arg else max_idx
        # Search next set of states for min player
        elif player == min_player:
            # Store minimum score and move index that gives it
            min_eval = float('inf')
            min_idx = None
            # Search each possible move...
            for i,(move_x,move_y) in enumerate(board.get_valid_moves()):
                # Track how many nodes searched
                self.nodes += 1
                # Make a copy of the board
                new_board = board.copy()
                # Min player plays move on board copy
                new_board.set(move_x,move_y,player)
                # Recursively evaluate new game state
                eval = self.__minimax(new_board,
                                max_player,
                                min_player,
                                max_player,
                                depth - 1,
                                alpha,
                                beta)
                # Check if new score is minimum score
                min_eval = min(min_eval,eval)
                # If new score is minimum, update minimum move index
                if eval == min_eval: 
                    min_idx = i
                # Alpha-beta pruning
                beta = min(beta,min_eval)
                if beta < alpha:
                    break
            # If specified, return minimum score index, otherwise return minimum score
            return min_eval if not arg else min_idx
    # Move piece according to minimax search
    def move(self,board,player,cell_size_x,cell_size_y,padding,pygame):
        # Track number of nodes used
        self.nodes = 0
        # Get first list of valid moves
        valid_moves = board.get_valid_moves()
        # Perform minimax search of move list, get idx of best move
        argmax = self.__minimax(
            board,player,
            self.__other_player(player),
            player,
            self.max_depth,
            -float('inf'),
            float('inf'),
            arg=True
        )
        # Make that move
        return valid_moves[argmax]