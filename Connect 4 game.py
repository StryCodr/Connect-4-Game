import random
import math

#loops through code below to see if player has won
def winning_board(board, player):
    return row_winner(board, player) or column_winner(board, player) or diagonal_winner(board, player)

#check for row winners
def row_winner(board, player):
    for row in board:
        count = 0
        for cell in row:
            if cell == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

#check for column winners
def column_winner(board, player):
    for i in range(len(board[0])):
        column_num = i
        column = []
        for i in range(len(board)):
            column.append(board[i][column_num])
        count = 0
        for cell in column:
            if cell == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False


#check for diagonal winners
# row = r, column = c
def diagonal_winner(board, player):
    #Check for positive sloped diagonals
    for r in range(len(board) - 3):
        for c in range(len(board[0]) - 3):
            if board[r][c] == player and board[r+1][c+1] == player and \
                board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True
    #Check for negative sloped diagonals
    for r in range(3, len(board)):
        for c in range(len(board[0]) - 3):
            if board[r][c] == player and board[r-1][c+1] == player and \
                board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True
    return False
def diagonal_equal(diagonal, player):
    count = 0
    for cell in diagonal:
        if cell == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False


    
#board that is shown
def format_board(board):
    formatted_grid = []
    for i in board:
        formatted_row = []
        col_div = []
        col_div.append('|'.join(i))
        formatted_row += [']'] + col_div + ['[']
        formatted_grid.append(''.join(formatted_row))
    num_labels = ''
    nums = []
    for i in range(7):
        nums.append(' ' + str(i+1) + '  ')
    num_labels = [' '] + nums + [' ']
    formatted_grid.append(''.join(num_labels))
    formatted_grid =  '\n'.join(formatted_grid)
    return(formatted_grid)



#player inputs and placing move in proper place
#also input errors and fixes
def play_move(board, player):
    column = []
    if player == ' X ':
        player_num = "Player 1"
    else:
        player_num = "Player 2"
    col_pick = input(f"{player_num}'s move: ")
    if col_pick.isdigit():
        col_pick = int(col_pick) - 1
        if not 0 <= col_pick <= 6:
            #out of range error
            print("Error: Column outside of board. Try again.\n")
            play_move(board, player)
        else:
            for i in range(len(board)):
                column.append(board[i][col_pick])
            if '   ' not in column:
                #column full
                print("Error: Selected column is full. Try again.\n")
                play_move(board, player)
            else:
                row_num = -1
                for i in range(len(board)):
                    if board[i][col_pick] == '   ':
                        row_num += 1
                    else:
                        break
                board[row_num][col_pick] = player
                print(format_board(board))
    else:
        #input was not a number
        print("Error: Invalid input. Try again.\n")
        play_move(board, player)





#AI's algorithm for its move (minimax algorithm w/ alpha-beta pruning)
def minimax(board, depth, alpha, beta, maximizingPlayer, player):
    opponent = ' O ' if player == ' X ' else ' X '
    valid_locations = [col for col in range(7) if board[0][col] == '   ']
    is_terminal = winning_board(board, player) or winning_board(board, opponent) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_board(board, player):
                return 100000000000000
            elif winning_board(board, opponent):
                return -10000000000000
            else:  #Game is over, no more valid moves
                return 0
        else:  #Depth is zero
            return score_position(board, player)
    if maximizingPlayer:
        value = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            temp_board[row][col] = player
            new_score = minimax(temp_board, depth-1, alpha, beta, False, player)
            value = max(value, new_score)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:  #Minimizing player
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            temp_board[row][col] = opponent
            new_score = minimax(temp_board, depth-1, alpha, beta, True, player)
            value = min(value, new_score)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

def score_position(board, player):
    score = 0
    opponent = ' O ' if player == ' X ' else ' X '

    #Score center column
    center_array = [board[i][3] for i in range(len(board))]
    center_count = center_array.count(player)
    score += center_count * 3

    #Score Horizontal
    for r in range(len(board)):
        row_array = [board[r][i] for i in range(7)]
        for c in range(4):
            window = row_array[c:c+4]
            score += evaluate_window(window, player)

    #Score Vertical
    for c in range(7):
        col_array = [board[r][c] for r in range(len(board))]
        for r in range(3):
            window = col_array[r:r+4]
            score += evaluate_window(window, player)

    #Score positive sloped diagonal
    for r in range(3):
        for c in range(4):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    #Score negative sloped diagonal
    for r in range(3):
        for c in range(4):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, player)
    return score

def evaluate_window(window, player):
    score = 0
    opponent = ' O ' if player == ' X ' else ' X '

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count('   ') == 1:
        score += 5
    elif window.count(player) == 2 and window.count('   ') == 2:
        score += 2

    if window.count(opponent) == 3 and window.count('   ') == 1:
        score -= 4
    return score

def get_next_open_row(board, col):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == '   ':
            return r
        
def ai_move(board, player):
    best_score = -math.inf
    best_col = random.choice([col for col in range(7) if board[0][col] == '   '])
    for col in range(7):
        if board[0][col] == '   ':
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            temp_board[row][col] = player
            score = minimax(temp_board, 5, -math.inf, math.inf, False, player)
            # Add a small random factor to the score
            score += random.uniform(-0.5, 0.5)
            if score > best_score:
                best_score = score
                best_col = col
    row = get_next_open_row(board, best_col)
    board[row][best_col] = player
    print(f"Computer's move: {best_col + 1}")
    print(format_board(board))

#AI developement (testing) mode
def AI_dev_mode(player1, player2, board):
    print("Entering dev mode: \n\n")
    #Ai for X
    Comp1_wins = 0
    #Ai for O
    Comp2_wins = 0
    #if AI ties
    Comp_tie = 0
    new_board = board
    game_board = board
    for _ in range(5):
        #makes fresh board for new game
        game_board = [row[:] for row in new_board]
        print("\n\nNew Game:\n" + format_board(game_board) + '\n')
        tot_moves = 42
        moves = 0
        for _ in range(tot_moves):
            print("Computer1 is thinking...")
            ai_move(game_board, player1)
            moves += 1
            if winning_board(game_board, player1):
                print("Computer1 won.")
                Comp1_wins += 1
                print(f"Computer 1: {Comp1_wins}\nComputer 2: {Comp2_wins}\nTies: {Comp_tie}\n")
                break
            if tot_moves == moves:
                print("Neither Computer has won, restarting.\n")
                Comp_tie += 1
                break
            print('\n')
            print("Computer2 is thinking...")
            ai_move(game_board, player2)
            moves += 1
            if winning_board(game_board, player2):
                print("Computer2 won.")
                Comp2_wins += 1
                print(f"Computer 1: {Comp1_wins}\nComputer 2: {Comp2_wins}\nTies: {Comp_tie}\n")
                break
            if tot_moves == moves:
                print("Neither Computer has won, restarting.\n")
                Comp_tie += 1
                print(f"Computer 1: {Comp1_wins}\nComputer 2: {Comp2_wins}\nTies: {Comp_tie}\n")
                break
            print('\n\n')
    print(f"Final Results:\nComputer 1: {Comp1_wins}\nComputer 2: {Comp2_wins}\nTies: {Comp_tie}")



#actual game and turn-based code for 1/2 players
def play_game(player1, player2, board, one_player):
    print("Enter column number to take turn.\n(Player 1 = X, Player 2 = O) \n\n")
    print(format_board(board) + '\n')
    tot_moves = 42
    moves = 0
    for _ in range(tot_moves):
        play_move(board, player1)
        moves += 1
        if winning_board(board, player1):
            return print_winner(player1, one_player)
        if tot_moves == moves:
            return print_draw()
        print('\n')
        
        if one_player:
            print("Computer is thinking...")
            ai_move(board, player2)
        else:
            play_move(board, player2)
            
        moves += 1
        if winning_board(board, player2):
            return print_winner(player2, one_player)
        if tot_moves == moves:
            return print_draw()
        print('\n')



#outcomes
def print_winner(player, one_player = False):
    if one_player == True:
        if player == ' X ':
            print(f"You win!\n")
        else:
            print(f"Computer wins!\n")
    else:
        print(f'\n{player}wins!\n')
def print_draw():
    print("It's a draw!")
    
    
    
#game mechanics
def start_game(player1, player2, board):
    board = board
    print("Enter column number to take turn.\n(Player 1 = X, Player 2 = O) \n\n")
    num_players = input("How many players are playing (1 or 2)?: ")
    print("\n")
    if num_players.isdigit():
        if num_players == '1':
            return play_game(player1, player2, board, one_player = True)
        elif num_players == '2':
            return play_game(player1, player2, board, one_player = False)
        else:
            #if input is not 1 or 2
            if int(num_players) > 2:
                print("Error: Too many players. Try again.\n\n")
                start_game(player1, player2, board)
            elif int(num_players) < 1:
                print("Error: Not enough players. Try again.\n\n")
                start_game(player1, player2, board)
            else:
                print("Error: Invalid number of players. Try again.\n\n")
                start_game(player1, player2, board)
    elif num_players == 'DEVmode_0':
        #ai developement
        return AI_dev_mode(player1, player2, board)
    else:
        #if input is not a number
        print("Error: Invalid input. Try again.\n\n")
        start_game(player1, player2, board)
    
    
#empty board format
board = ([
['   ', '   ', '   ', '   ', '   ', '   ', '   '], 
['   ', '   ', '   ', '   ', '   ', '   ', '   '], 
['   ', '   ', '   ', '   ', '   ', '   ', '   '], 
['   ', '   ', '   ', '   ', '   ', '   ', '   '], 
['   ', '   ', '   ', '   ', '   ', '   ', '   '], 
['   ', '   ', '   ', '   ', '   ', '   ', '   ']
    ])




start_game(' X ', ' O ', board)
