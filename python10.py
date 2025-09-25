import pygame, sys, math, random

# Setup
pygame.init()
WIDTH, HEIGHT = 300, 300
ROWS, COLS = 3, 3
SQ = WIDTH // COLS
WHITE, BG, LINE, CIRCLE, CROSS = (255,255,255), (28,170,156), (23,145,135), (239,231,200), (66,66,66)
LINE_W, CIRCLE_R, CIRCLE_W, CROSS_W = 5, SQ//4, 15, 20
AI, HUMAN, EMPTY = 1, -1, 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")

# Game data
board = [[EMPTY]*COLS for _ in range(ROWS)]
player_turn = True
game_over = False

# Draw board lines
def draw_board():
    screen.fill(BG)
    for i in range(1, ROWS):
        pygame.draw.line(screen, LINE, (0, i*SQ), (WIDTH, i*SQ), LINE_W)
        pygame.draw.line(screen, LINE, (i*SQ, 0), (i*SQ, HEIGHT), LINE_W)

# Draw X and O
def draw_figures():
    for r in range(ROWS):
        for c in range(COLS):
            x = c*SQ + SQ//2
            y = r*SQ + SQ//2
            if board[r][c] == HUMAN:
                pygame.draw.circle(screen, CIRCLE, (x, y), CIRCLE_R, CIRCLE_W)
            elif board[r][c] == AI:
                pygame.draw.line(screen, CROSS, (c*SQ+20, r*SQ+20), (c*SQ+SQ-20, r*SQ+SQ-20), CROSS_W)
                pygame.draw.line(screen, CROSS, (c*SQ+20, r*SQ+SQ-20), (c*SQ+SQ-20, r*SQ+20), CROSS_W)

# Check win
def check_win(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): return True
        if all(board[j][i] == player for j in range(3)): return True
    if all(board[i][i] == player for i in range(3)): return True
    if all(board[i][2-i] == player for i in range(3)): return True
    return False

# Check draw
def is_draw():
    return all(board[r][c] != EMPTY for r in range(ROWS) for c in range(COLS))

# Minimax AI
def minimax(is_max):
    if check_win(AI): return 1
    if check_win(HUMAN): return -1
    if is_draw(): return 0
    best = -math.inf if is_max else math.inf
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == EMPTY:
                board[r][c] = AI if is_max else HUMAN
                score = minimax(not is_max)
                board[r][c] = EMPTY
                best = max(best, score) if is_max else min(best, score)
    return best

# AI best move
def best_move():
    best_score, move = -math.inf, None
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == EMPTY:
                board[r][c] = AI
                score = minimax(False)
                board[r][c] = EMPTY
                if score > best_score:
                    best_score, move = score, (r, c)
    if move: board[move[0]][move[1]] = AI

# Restart game
def restart():
    global board, player_turn, game_over
    board = [[EMPTY]*COLS for _ in range(ROWS)]
    player_turn, game_over = True, False
    draw_board()

# Main loop
draw_board()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r: restart()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player_turn:
            r, c = event.pos[1] // SQ, event.pos[0] // SQ
            if board[r][c] == EMPTY:
                board[r][c] = HUMAN
                player_turn = False

    if not player_turn and not game_over:
        best_move()
        player_turn = True

    draw_figures()
    pygame.display.update()

    if not game_over:
        if check_win(HUMAN): print("Human Wins!"); game_over = True
        elif check_win(AI): print("AI Wins!"); game_over = True
        elif is_draw(): print("Draw!"); game_over = True
