import random
from colorama import init, Fore, Style
init(autoreset=True)
def display_board(board):
    print()
    def colored(cell):
        if cell == 'X':
            return Fore.RED + cell + Style.RESET_ALL
        elif cell == 'O':
            return Fore.BLUE + cell + Style.RESET_ALL
        else:
            return Fore.YELLOW + cell + Style.RESET_ALL
    print(' ' + colored(board[0]) + ' | ' + colored(board[1]) + ' | ' + colored(board[2]))
    print(Fore.CYAN + '-----------' + Style.RESET_ALL)
    print(' ' + colored(board[3]) + ' | ' + colored(board[4]) + ' | ' + colored(board[5]))
    print(Fore.CYAN + '-----------' + Style.RESET_ALL)
    print(' ' + colored(board[6]) + ' | ' + colored(board[7]) + ' | ' + colored(board[8]))
    print()
def player_choice():
    symbol = ''
    while symbol not in ['X', 'O']:
        symbol = input(Fore.GREEN + "Do you want to be X or O? " + Style.RESET_ALL).upper()
    if symbol == 'X':
        return ('X', 'O')
    else:
        return ('O', 'X')
def player_move(board, symbol):
    move = -1
    while move not in range(1, 10) or not board[move - 1].isdigit():
        try:
            move = int(input("Enter your move (1-9): "))
            if move not in range(1, 10) or not board[move - 1].isdigit():
                print("Invalid move. Please try again.")
        except ValueError:
            print("Please enter a number between 1 and 9.")
    board[move - 1] = symbol
def ai_move(board, ai_symbol, player_symbol):
    for i in range(9):
        if board[i].isdigit():
            board_copy = board.copy()
            board_copy[i] = ai_symbol
            if check_win(board_copy, ai_symbol):
                board[i] = ai_symbol
                return
    for i in range(9):
        if board[i].isdigit():
            board_copy = board.copy()
            board_copy[i] = player_symbol
            if check_win(board_copy, player_symbol):
                board[i] = ai_symbol
                return
    possible_moves = [i for i in range(9) if board[i].isdigit()]
    move = random.choice(possible_moves)
    board[move] = ai_symbol
def tictactoe():
    print("welcome to tic tac toe")
    playername=input(Fore.GREEN + "Enter Your Name: " + Style.RESET_ALL)
    while True:
        board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        player_symbol, ai_symbol = player_choice()
        turn = 'Player'
        game_on = True
def check_win(board, symbol):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),    # Horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),    # Vertical
        (0, 4, 8), (2, 4, 6)                # Diagonal
    ]
    for cond in win_conditions:
        if board[cond[0]] == board[cond[1]] == board[cond[2]] == symbol:
            return True
    return False