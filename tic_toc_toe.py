import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
    print("\n")

def check_winner(board):
    for row in board:
        if row.count(row[0]) == 3 and row[0] != " ":
            return True

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return True

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return True

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return True

    return False

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def ai_move(board):
    empty_cells = get_empty_cells(board)
    return random.choice(empty_cells)

def play():
    board = [[" "]*3 for _ in range(3)]
    while True:
        print_board(board)

        # Player move
        row, col = map(int, input("Enter row and col (0-2): ").split())
        if board[row][col] != " ":
            print("Cell already taken! Try again.")
            continue
        board[row][col] = "X"

        if check_winner(board):
            print_board(board)
            print("You win! 🎉")
            break

        if not get_empty_cells(board):
            print_board(board)
            print("It's a tie!")
            break

        # AI move
        ai_row, ai_col = ai_move(board)
        board[ai_row][ai_col] = "O"
        print(f"AI chose: {ai_row}, {ai_col}")

        if check_winner(board):
            print_board(board)
            print("AI wins! 🤖")
            break

play()
