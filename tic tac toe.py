HUMAN = "X"
AI = "O"
EMPTY = " "

WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),  # rows
    (0,3,6), (1,4,7), (2,5,8),  # cols
    (0,4,8), (2,4,6)            # diagonals
]

def print_board(board):
    cells = [board[i] if board[i] != EMPTY else str(i+1) for i in range(9)]
    print(f"\n {cells[0]} | {cells[1]} | {cells[2]} ")
    print("---+---+---")
    print(f" {cells[3]} | {cells[4]} | {cells[5]} ")
    print("---+---+---")
    print(f" {cells[6]} | {cells[7]} | {cells[8]} \n")

def winner(board):
    for a,b,c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    if EMPTY not in board:
        return "draw"
    return None

def available_moves(board):
    return [i for i, v in enumerate(board) if v == EMPTY]

def order_moves(moves):
    # Small speed-up: center > corners > edges
    center = [4] if 4 in moves else []
    corners = [m for m in [0,2,6,8] if m in moves]
    edges = [m for m in [1,3,5,7] if m in moves]
    return center + corners + edges

def minimax(board, maximizing, alpha, beta):
    w = winner(board)
    if w == AI:
        return 10, None
    if w == HUMAN:
        return -10, None
    if w == "draw":
        return 0, None

    if maximizing:
        best_score = -10**9
        best_move = None
        for move in order_moves(available_moves(board)):
            board[move] = AI
            score, _ = minimax(board, False, alpha, beta)
            board[move] = EMPTY
            if score > best_score:
                best_score, best_move = score, move
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = 10**9
        best_move = None
        for move in order_moves(available_moves(board)):
            board[move] = HUMAN
            score, _ = minimax(board, True, alpha, beta)
            board[move] = EMPTY
            if score < best_score:
                best_score, best_move = score, move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score, best_move

def human_turn(board):
    while True:
        try:
            choice = input("Choose your move (1-9): ").strip()
            if choice.lower() == "q":
                return "quit"
            pos = int(choice) - 1
            if pos not in range(9):
                print("Enter a number from 1 to 9.")
                continue
            if board[pos] != EMPTY:
                print("That spot is taken. Try another.")
                continue
            board[pos] = HUMAN
            return None
        except ValueError:
            print("Invalid input. Type a number 1-9, or 'q' to quit.")

def ai_turn(board):
    _, move = minimax(board, True, -10**9, 10**9)
    board[move] = AI

def play_game():
    print("\n=== Tic-Tac-Toe — Unbeatable AI ===")
    print("You are X. Type numbers 1-9 to place your mark. Type 'q' to quit.")
    while True:
        # choose who starts
        first = input("Start first? (y/n): ").strip().lower()
        if first in ("y","n"):
            human_starts = (first == "y")
            break
        print("Please enter 'y' or 'n'.")

    board = [EMPTY] * 9
    current = HUMAN if human_starts else AI

    while True:
        print_board(board)
        if current == HUMAN:
            q = human_turn(board)
            if q == "quit":
                print("Goodbye!")
                return
        else:
            print("AI is thinking...")
            ai_turn(board)

        w = winner(board)
        if w:
            print_board(board)
            if w == "draw":
                print("It's a draw!")
            else:
                print(f"{w} wins!")
            break

        current = AI if current == HUMAN else HUMAN

    # replay option
    again = input("\nPlay again? (y/n): ").strip().lower()
    if again == "y":
        play_game()
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    play_game()
