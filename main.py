import pygame
import random
from math import inf



WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TRANS = (1, 2, 3)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

WIDTH = 800
HEIGHT = 800
MARK_SIZE = 50

SIDE_BUTTON_POS = (WIDTH // 2 - 100, HEIGHT - 70)
SIDE_BUTTON_SIZE = (200, 50)
RESET_BUTTON_COLOR = (255, 255, 255)
X_BUTTON_POS = (WIDTH // 2 - 155, HEIGHT - 70)
O_BUTTON_POS = (WIDTH // 2 + 50, HEIGHT - 70)
BUTTON_SIZE = (50, 50)

def draw_reset_button(screen):
    reset_button_rect = pygame.Rect(WIDTH / 2 - 50, HEIGHT + 10, 100, 40)
    pygame.draw.rect(screen, BROWN, reset_button_rect)
    pygame.draw.rect(screen, WHITE, reset_button_rect, 5)
    font = pygame.font.SysFont('Calibri', 20, True)
    reset_text = font.render('RESET', True, WHITE)
    screen.blit(reset_text, [WIDTH / 2 - reset_text.get_width() / 2, HEIGHT + 20])



def draw_side_button(screen):
    font = pygame.font.SysFont('Calibri', 24, True, False)
    x_button = font.render("X", True, WHITE)
    o_button = font.render("O", True, WHITE)
    screen.blit(x_button, (WIDTH + 50, 50))
    screen.blit(o_button, (WIDTH + 150, 50))


def draw_buttons(screen):
    font = pygame.font.SysFont('Calibri', 24, False, False)

    reset_button_rect = pygame.Rect(WIDTH - 220, 10, 200, 20)
    pygame.draw.rect(screen, RESET_BUTTON_COLOR, reset_button_rect,50)
    reset_text = font.render('Reset', True, BLACK)
    reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
    screen.blit(reset_text, reset_text_rect)

    x_button_rect = pygame.Rect(X_BUTTON_POS, BUTTON_SIZE)
    pygame.draw.rect(screen, GREEN, x_button_rect)
    x_text = font.render("X", True, BLACK)
    x_text_rect = x_text.get_rect(center=x_button_rect.center)
    screen.blit(x_text, x_text_rect)

    o_button_rect = pygame.Rect(O_BUTTON_POS, BUTTON_SIZE)
    pygame.draw.rect(screen, GREEN, o_button_rect)
    o_text = font.render("O", True, BLACK)
    o_text_rect = o_text.get_rect(center=o_button_rect.center)
    screen.blit(o_text, o_text_rect)



class Game:

    def minimax(self, depth, maximizing_player, alpha, beta):
        if depth == 0 or self.check_winner() is not None:
            return self.heuristic()

        if maximizing_player:
            max_eval = -inf
            for row in range(8):
                for col in range(8):
                    if self.game_board[row][col].lower() == self.players[self.turn % 2]:
                        for move in self.get_valid_moves(row, col):
                            self.make_move(row, col, move[0], move[1], move[2])
                            eval = self.minimax(depth - 1, False, alpha, beta)
                            self.undo_move(row, col, move[0], move[1], move[2])
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
            return max_eval
        else:
            min_eval = inf
            for row in range(8):
                for col in range(8):
                    if self.game_board[row][col].lower() == self.players[(self.turn + 1) % 2]:
                        for move in self.get_valid_moves(row, col):
                            self.make_move(row, col, move[0], move[1], move[2])
                            eval = self.minimax(depth - 1, True, alpha, beta)
                            self.undo_move(row, col, move[0], move[1], move[2])
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
            return min_eval

    def ai_make_move(self, depth=3):
        best_eval = -inf
        best_move = None
        for row in range(8):
            for col in range(8):
                if self.game_board[row][col].lower() == self.players[self.turn % 2]:
                    for move in self.get_valid_moves(row, col):
                        self.make_move(row, col, move[0], move[1], move[2])
                        eval = self.minimax(depth - 1, False, -inf, inf)
                        self.undo_move(row, col, move[0], move[1], move[2])
                        if eval > best_eval:
                            best_eval = eval
                            best_move = (row, col, move[0], move[1], move[2])

        if best_move:
            self.play(self.players[self.turn % 2], (best_move[0], best_move[1]), best_move[2], best_move[3], best_move[4])

    def heuristic(self):

        ai_pieces = sum(
            [row.count(self.players[self.turn % 2]) + row.count(self.players[self.turn % 2].upper()) for row in
             self.game_board])
        opp_pieces = sum(
            [row.count(self.players[(self.turn + 1) % 2]) + row.count(self.players[(self.turn + 1) % 2].upper()) for row
             in self.game_board])
        return ai_pieces - opp_pieces

    def get_valid_moves(self, from_row, from_col):
        moves = []
        for dr in [-2, -1, 1, 2]:
            for dc in [-2, -1, 1, 2]:
                to_row, to_col = from_row + dr, from_col + dc
                if 0 <= to_row < 8 and 0 <= to_col < 8:
                    move = self.is_valid_move(self.game_board[from_row][from_col].lower(), [from_row, from_col], to_row,
                                              to_col)
                    if move[0]:
                        moves.append((to_row, to_col, move[1]))
        return moves

    def make_move(self, from_row, from_col, to_row, to_col, jumped_piece):
        self.game_board[to_row][to_col] = self.game_board[from_row][from_col]
        self.game_board[from_row][from_col] = '-'
        if jumped_piece is not None:
            self.game_board[jumped_piece[0]][jumped_piece[1]] = '-'

    def undo_move(self, from_row, from_col, to_row, to_col, jumped_piece):
        self.game_board[from_row][from_col] = self.game_board[to_row][to_col]
        self.game_board[to_row][to_col] = '-'
        if jumped_piece is not None:
            if self.game_board[from_row][from_col].lower() == 'x':
                self.game_board[jumped_piece[0]][jumped_piece[1]] = 'o'
            else:
                self.game_board[jumped_piece[0]][jumped_piece[1]] = 'x'

    def reset_board(self):
        self.game_board = [['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                           ['-', 'x', '-', 'x', '-', 'x', '-', 'x'],
                           ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                           ['-', '-', '-', '-', '-', '-', '-', '-'],
                           ['-', '-', '-', '-', '-', '-', '-', '-'],
                           ['-', 'o', '-', 'o', '-', 'o', '-', 'o'],
                           ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
                           ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]

    def __init__(self):

        self.status = 'playing'
        self.turn = random.randrange(2)
        self.players = ['x', 'o']
        self.selected_token = None
        self.jumping = False
        pygame.display.set_caption("%s's turn" % self.players[self.turn % 2])
        self.game_board = [['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                           ['-', 'x', '-', 'x', '-', 'x', '-', 'x'],
                           ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                           ['-', '-', '-', '-', '-', '-', '-', '-'],
                           ['-', '-', '-', '-', '-', '-', '-', '-'],
                           ['-', 'o', '-', 'o', '-', 'o', '-', 'o'],
                           ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
                           ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]

    def evaluate_click(self, mouse_pos):
        if WIDTH - 220 < mouse_pos[0] < WIDTH - 20 and 10 < mouse_pos[1] < 60:
            self.reset_board()
            return
        if self.status == 'playing':
            row, column = get_clicked_row(mouse_pos), get_clicked_column(mouse_pos)
            if self.selected_token:
                move = self.is_valid_move(self.players[self.turn % 2], self.selected_token, row, column)
                if move[0]:
                    self.play(self.players[self.turn % 2], self.selected_token, row, column, move[1])
                elif row == self.selected_token[0] and column == self.selected_token[1]:
                    self.selected_token = None
                    if self.jumping:
                        self.jumping = False
                        self.next_turn()
                else:
                    print()
                    'invalid move'
            else:
                if self.game_board[row][column].lower() == self.players[self.turn % 2]:
                    self.selected_token = [row, column]
            if pygame.mouse.get_pressed()[0]:
                if WIDTH - 50 < mouse_pos[0] < WIDTH - 10 and 0 < mouse_pos[1] < 40:
                    self.__init__()
                elif WIDTH - 150 < mouse_pos[0] < WIDTH - 10 and 0 < mouse_pos[1] < 40:
                    self.players = ['x', 'o'] if self.players == ['o', 'x'] else ['o', 'x']
                    self.turn += 1
                    pygame.display.set_caption("%s's turn" % self.players[self.turn % 2])
        elif self.status == 'game over':
            self.__init__()

    def is_valid_move(self, player, token_location, to_row, to_col):

        from_row = token_location[0]
        from_col = token_location[1]
        token_char = self.game_board[from_row][from_col]
        if self.game_board[to_row][to_col] != '-':
            return False, None
        if (((token_char.isupper() and abs(from_row - to_row) == 1) or (player == 'x' and to_row - from_row == 1) or
             (player == 'o' and from_row - to_row == 1)) and abs(from_col - to_col) == 1) and not self.jumping:
            return True, None
        if (((token_char.isupper() and abs(from_row - to_row) == 2) or (player == 'x' and to_row - from_row == 2) or
             (player == 'o' and from_row - to_row == 2)) and abs(from_col - to_col) == 2):
            jump_row = int((to_row - from_row) / 2 + from_row)
            jump_col = int((to_col - from_col) / 2 + from_col)

            if self.game_board[jump_row][jump_col].lower() not in [player, '-']:
                return True, [jump_row, jump_col]
        return False, None

    def play(self, player, token_location, to_row, to_col, jump):

        from_row = token_location[0]
        from_col = token_location[1]
        token_char = self.game_board[from_row][from_col]
        self.game_board[to_row][to_col] = token_char
        self.game_board[from_row][from_col] = '-'
        if (player == 'x' and to_row == 7) or (player == 'o' and to_row == 0):
            self.game_board[to_row][to_col] = token_char.upper()
        if jump:
            self.game_board[jump[0]][jump[1]] = '-'
            self.selected_token = [to_row, to_col]
            self.jumping = True
        else:
            self.selected_token = None
            self.next_turn()
        winner = self.check_winner()
        if winner is None:
            pygame.display.set_caption("%s's turn" % self.players[self.turn % 2])
        elif winner == 'draw':
            pygame.display.set_caption("It's a stalemate! Click to start again")
            self.status = 'game over'
        else:
            pygame.display.set_caption("%s wins! Click to start again" % winner)
            self.status = 'game over'

    def next_turn(self):
        self.turn += 1
        pygame.display.set_caption("%s's turn" % self.players[self.turn % 2])

    def check_winner(self):

        x = sum([row.count('x') + row.count('X') for row in self.game_board])
        if x == 0:
            return 'o'
        o = sum([row.count('o') + row.count('O') for row in self.game_board])
        if o == 0:
            return 'x'
        if x == 1 and o == 1:
            return 'draw'
        return None

    def draw(self, screen):
        for r in range(len(self.game_board)):
            for c in range(len(self.game_board[r])):
                x = c * WIDTH / 8
                y = r * HEIGHT / 8
                if (r + c) % 2 == 0:
                    color = BROWN
                else:
                    color = WHITE
                pygame.draw.rect(screen, color, [x, y, WIDTH / 8, HEIGHT / 8])
                mark = self.game_board[r][c]
                if self.players[self.turn % 2] == mark.lower():
                    color = YELLOW
                else:
                    color = WHITE
                if self.selected_token:
                    if self.selected_token[0] == r and self.selected_token[1] == c:
                        color = RED
                if mark != '-':
                    font = pygame.font.SysFont('Calibri', MARK_SIZE, False, False)
                    mark_text = font.render(self.game_board[r][c], True, color)
                    x = c * WIDTH / 8 + WIDTH / 16
                    y = r * HEIGHT / 8 + HEIGHT / 16
                    screen.blit(mark_text, [x - mark_text.get_width() / 2, y - mark_text.get_height() / 2])

        draw_side_button(screen)
        draw_buttons(screen)


def get_clicked_column(mouse_pos):
    x = mouse_pos[0]
    for i in range(1, 8):
        if x < i * WIDTH / 8:
            return i - 1
    return 7


def get_clicked_row(mouse_pos):
    y = mouse_pos[1]
    for i in range(1, 8):
        if y < i * HEIGHT / 8:
            return i - 1
    return 7



pygame.init()
pygame.display.init()

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)


game = Game()


done = False


clock = pygame.time.Clock()


# game loop:
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()


            if (X_BUTTON_POS[0] <= mouse_x <= X_BUTTON_POS[0] + BUTTON_SIZE[0] and
                    X_BUTTON_POS[1] <= mouse_y <= X_BUTTON_POS[1] + BUTTON_SIZE[1]):
                game.players = ['x', 'o']
                game.turn = 0
                game.reset_board()
                pygame.display.set_caption("%s's turn" % game.players[game.turn % 2])


            elif (O_BUTTON_POS[0] <= mouse_x <= O_BUTTON_POS[0] + BUTTON_SIZE[0] and
                  O_BUTTON_POS[1] <= mouse_y <= O_BUTTON_POS[1] + BUTTON_SIZE[1]):
                game.players = ['o', 'x']
                game.turn = 0
                game.reset_board()
                pygame.display.set_caption("%s's turn" % game.players[game.turn % 2])

            else:
                game.evaluate_click((mouse_x, mouse_y))
            if game.players[game.turn % 2] == 'x':
                game.ai_make_move()
    screen.fill(BLACK)
    game.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
