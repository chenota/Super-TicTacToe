class Board:
    # Set board to all zeros
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
    # Get board at row, column
    def at(self,r,c):
        if 0 <= r <= 9 and 0 <= c <= 9:
            return self.board[r][c]
        return None
    # Set board at row, column to specified player's piece
    def set(self,r,c,v):
        if 0 <= r <= 9 and 0 <= c <= 9 and self.board[r][c] == 0:
            self.board[r][c] = v 
    # Make a deep copy of self
    def copy(self):
        new_board = Board()
        for i in range(9):
            for j in range(9):
                new_board.set(i,j,self.at(i,j))
        return new_board
    # Check if board is a winning state
    def is_win(self,player):
        # Rows
        for row in self.board:
            if len(list(filter(lambda x: x == player, row))) == 9:
                return True
        # Columns
        for col in zip(*self.board):
            if len(list(filter(lambda x: x == player, col))) == 9:
                return True
        # Diagonals
        diag_left = [self.board[i][i] for i in range(9)]
        if len(list(filter(lambda x: x == player, diag_left))) == 9:
            return True
        diag_right = [self.board[i][8 - i] for i in range(9)]
        if len(list(filter(lambda x: x == player, diag_right))) == 9:
            return True
        return False
    # Check if more moves can be made
    def is_full(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False 
        return True
    # Get list of valid moves (empty board cells)
    def get_valid_moves(self):
        valid_moves = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    valid_moves.append((i,j))
        return valid_moves