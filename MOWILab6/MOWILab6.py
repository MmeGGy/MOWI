import pygame
import sys
import json

WIDTH = 300
HEIGHT = 300

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CELL_SIZE = WIDTH // 3

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

game_board = [[None, None, None], [None, None, None], [None, None, None]]
current_player = "X"
game_over = False

# Statistics
stats = {"games_played": 0, "wins": 0, "losses": 0, "draws": 0}

def update_screen():
    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), 2)
    pygame.draw.line(screen, BLACK, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, HEIGHT), 2)
    pygame.draw.line(screen, BLACK, (0, CELL_SIZE), (WIDTH, CELL_SIZE), 2)
    pygame.draw.line(screen, BLACK, (0, 2 * CELL_SIZE), (WIDTH, 2 * CELL_SIZE), 2)

    for row in range(3):
        for col in range (3):
            if game_board[row][col] == "X":
                pygame.draw.line(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE),
                                 ((col +1)*CELL_SIZE, (row + 1)*CELL_SIZE), 2)
                pygame.draw.line(screen, BLACK, (col * CELL_SIZE, (row + 1) * CELL_SIZE),
                                 ((col + 1) * CELL_SIZE, row * CELL_SIZE), 2)
            elif game_board[row][col] == "0":
                pygame.draw.circle(screen, BLACK, ((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE),
                                   CELL_SIZE // 2, 2)
    pygame.display.flip()

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != None:
            if board[i][0] == "X":
                return "X"
            else:
                return "0"
        if board[0][i] == board[1][i] == board[2][i] != None:
            if board[0][i] == "X":
                return "X"
            else:
                return "0"
    if board[0][0] == board[1][1] == board[2][2] != None:
        if board[1][1] == "X":
            return "X"
        else:
            return "0"
    if board[0][2] == board[1][1] == board[2][0] != None:
        if board[1][1] == "X":
            return "X"
        else:
            return "0"
    if all(board[row][col] is not None for row in range(3) for col in range(3)):
        return "Draw"
    return None

def update_game(row, col):
    if game_board[row][col] is None and not game_over:
        game_board[row][col] = current_player

        winner = check_winner(game_board)
        if winner is not None:
            end_game(winner)
        else:
            change_turn()

def change_turn():
    global current_player
    current_player = "0" if current_player == "X" else "X"

def end_game(winner):
    global game_over
    game_over = True

    if winner == "Draw":
        message = "It's a draw"
        stats["draws"] += 1
    else:
        message = f"{winner} wins"
        if winner == "X":
            stats["wins"] += 1
        else:
            stats["losses"] += 1

    pygame.display.set_caption(message)
    save_statistics()
    show_statistics()
    show_new_game_prompt()

def show_new_game_prompt():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_statistics()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                reset_game()
                return

def reset_game():
    global game_board, current_player, game_over
    game_board = [[None, None, None], [None, None, None], [None, None, None]]
    current_player = "X"
    game_over = False
    pygame.display.set_caption("Tic-Tac-Toe")
    stats["games_played"] += 1
    update_screen()

def choose_computer_move():
    best_score = -float("inf")
    best_move = None

    for row in range(3):
        for col in range(3):
            if game_board[row][col] is None:
                game_board[row][col] = "0"
                score = minimax(game_board, 0, False)
                game_board[row][col] = None

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move

def minimax(board, depth, is_maximizing):
    result = check_winner(board)
    if result is not None:
        if result == "X":
            return -1
        elif result == "0":
            return 1
        else:
            return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "0"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score

def save_statistics():
    with open("statistics.json", "w") as file:
        json.dump(stats, file)

def load_statistics():
    try:
        with open("statistics.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def show_statistics():
    print("--- Statistics ---")
    print(f"Games played: {stats['games_played']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print(f"Draws: {stats['draws']}")
    print("------------------")

def run_game():
    global stats

    # Load statistics
    loaded_stats = load_statistics()
    if loaded_stats:
        stats = loaded_stats

    stats["games_played"] += 1
    show_statistics()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_statistics()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // CELL_SIZE
                row = mouse_pos[1] // CELL_SIZE
                update_game(row, col)
                if game_over:
                    show_new_game_prompt()
                elif not game_over and current_player == "0":
                    computer_move = choose_computer_move()
                    if computer_move:
                        update_game(computer_move[0], computer_move[1])
        update_screen()

run_game()
