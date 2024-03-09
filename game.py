from board import Board
import pygame

class Game:
    def __init__(self,player1,player2):
        # Game variables
        self.player1 = player1
        self.player2 = player2
        self.currplayer = player1
        self.isplaying = 1
        self.board = Board()
        # Initialize pygame
        pygame.init()
        # GUI constant variables
        self.DISPLAY_SIZE = (500,550)
        self.DEFAULT_BG_COLOR = (0,0,0)
        self.DEFAULT_LINE_COLOR = (255,255,255)
        self.DEFAULT_FONT_COLOR = (255,255,255)
        self.PADDING = 25
        self.FONT = pygame.font.Font('freesansbold.ttf', 20)
        self.PIECE_FONT = pygame.font.Font('freesansbold.ttf', 40)
    def run(self):
        # GUI intialization
        self.screen = pygame.display.set_mode(self.DISPLAY_SIZE)
        pygame.display.set_caption("Super Tic Tac Toe")
        self.screen.fill(self.DEFAULT_BG_COLOR)
        pygame.display.flip()
        # Game loop
        running = True
        is_done = False
        win_text = ""
        while running:
            # Check for quit event
            for event in pygame.event.get():   
                if event.type == pygame.QUIT: 
                    running = False
            # Clear screen
            self.screen.fill(self.DEFAULT_BG_COLOR)
            # Draw board lines
            disp_x, disp_y = self.DISPLAY_SIZE
            disp_x -= self.PADDING
            disp_y -= 50 + self.PADDING
            for x in range(self.PADDING + ((disp_x - self.PADDING) // 9), disp_x, (disp_x - self.PADDING) // 9):
                pygame.draw.line(self.screen, self.DEFAULT_LINE_COLOR, [x, self.PADDING], [x, disp_y], width=1)
            for y in range(self.PADDING + ((disp_y - self.PADDING) // 9), disp_y, (disp_y - self.PADDING) // 9):
                pygame.draw.line(self.screen, self.DEFAULT_LINE_COLOR, [self.PADDING, y], [disp_x, y], width=1)
            # Draw player text
            text = self.FONT.render(f'{self.currplayer.name}\'s Turn ({"X" if self.isplaying == 1 else "O"})', False, self.DEFAULT_FONT_COLOR)
            if is_done:
                text = self.FONT.render(win_text, False, self.DEFAULT_FONT_COLOR)
            text_rect = text.get_rect()
            text_rect.center = (self.DISPLAY_SIZE[0] // 2, self.DISPLAY_SIZE[1] - 30)
            self.screen.blit(text, text_rect)
            # Draw pieces
            for i in range(9):
                for j in range(9):
                    if self.board.at(i,j) == 1:
                        text = self.PIECE_FONT.render('X', False, self.DEFAULT_FONT_COLOR)
                        text_rect = text.get_rect() 
                        text_rect.center = (
                            int(self.PADDING + (i * 50) + 25),
                            int(self.PADDING + (j * 50) + 25),
                        )
                        self.screen.blit(text, text_rect)
                    elif self.board.at(i,j) == 2:
                        text = self.PIECE_FONT.render('O', False, self.DEFAULT_FONT_COLOR)
                        text_rect = text.get_rect() 
                        text_rect.center = (
                            int(self.PADDING + (i * 50) + 25),
                            int(self.PADDING + (j * 50) + 25),
                        )
                        self.screen.blit(text, text_rect)
            # Flip screen buffer
            pygame.display.flip()
            if not is_done:
                # Player makes move
                play_x,play_y = self.currplayer.move(
                    self.board,
                    self.isplaying,
                    ((disp_x - self.PADDING) // 9),
                    ((disp_y - self.PADDING) // 9),
                    self.PADDING,
                    pygame
                )
                # Check move and play
                if self.isplaying == 1:
                    self.board.set(play_x,play_y,1)
                elif self.isplaying == 2:
                    self.board.set(play_x,play_y,2)
                # Check win conditions
                if self.board.is_win(self.isplaying):
                    win_text = f"{self.currplayer.name} ({'X' if self.isplaying == 1 else 'O'}) wins!"
                    is_done = True
                # Check draw conditions
                if self.board.is_full():
                    win_text = "Draw!"
                    is_done = True
                self.switch_players()
    # Switch current player
    def switch_players(self):
        if self.isplaying == 1:
            self.isplaying = 2
            self.currplayer = self.player2
        else:
            self.isplaying = 1
            self.currplayer = self.player1