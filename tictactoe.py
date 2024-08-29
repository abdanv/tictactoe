"""
Tic Tac Toe Player
"""

import math
import copy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Initialize counters
    count_X = 0
    count_O = 0

    # Iterate through the matrix
    for row in board:
        for element in row:
            if element == 'X':
                count_X += 1
            elif element == 'O':
                count_O += 1
    
    # Check who has more moves 
    if count_X > count_O:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    l = len(board)
    moves = set()
    for i in range(l):
        for j in range(l):
            if board[i][j] is None:
                moves.add((i, j))
    
    return moves
    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    l = len(board)
    
    # Raising exception on negative out-of-bounds move
    if action[0] < 0 or action[0] > l - 1 or action[1] < 0 or action[1] > l - 1:
        raise ValueError
    
    # Raising exception on taken move
    if board[action[0]][action[1]]:
        raise ValueError
          
    # Making a deep copy of the board before making any changes.
    new_board = copy.deepcopy(board)
    player_input = player(board)
    new_board[action[0]][action[1]] = player_input
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    l = len(board)
    countX_diag1 = 0
    countO_diag1 = 0
    countX_diag2 = 0
    countO_diag2 = 0
    
    for i in range(l):
        countX_hor = 0
        countO_hor = 0
        countX_ver = 0
        countO_ver = 0
        
        # Check diagonal 1 (top-left to bottom-right)
        if board[i][i] == "X":
            countX_diag1 += 1
        if board[i][i] == "O":
            countO_diag1 += 1
            
        # Check diagonal 2 (top-right to bottom-left)
        if board[i][l - 1 - i] == "X":
            countX_diag2 += 1
        if board[i][l - 1 - i] == "O":
            countO_diag2 += 1
            
        # Check rows and columns
        for j in range(l):
            if board[i][j] == "X":
                countX_hor += 1
            elif board[i][j] == "O":
                countO_hor += 1
                
            if board[j][i] == "X":
                countX_ver += 1
            elif board[j][i] == "O":
                countO_ver += 1
        
        # Check for a win in the current row or column
        if countX_hor == l or countX_ver == l:
            return "X"
        if countO_hor == l or countO_ver == l:
            return "O"
    
    # Check for a win in either diagonal    
    if countX_diag1 == l or countX_diag2 == l:
        return "X"
    if countO_diag1 == l or countO_diag2 == l:
        return "O"

    # If no winner is found, return None    
    return None        


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    l = len(board)
    # Game is over because someone has won the game
    if winner(board):
        return True
    
    # Check if all cells have been filled
    for i in range(l):
        for j in range(l):
            if board[i][j] is None:
                return False
            
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    
    if result == "X":
        return 1
    elif result == "O":
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is a terminal board, the minimax function should return None.
    if terminal(board):
        return None
    
    if player(board) == "X":
        min = -2
        for action in actions(board):
            currX_value = min_value(result(board, action))
            if currX_value > min:
                min = currX_value
                picked_action = action
        return picked_action
    
    if player(board) == "O":
        max = 2
        for action in actions(board):
            currO_value = max_value(result(board, action))
            if currO_value < max:
                max = currO_value
                picked_action = action
        return picked_action


def max_value(board):
    
    if terminal(board):
        return utility(board)
    
    value = -2
    
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
        
    return value


def min_value(board):
    
    if terminal(board):
        return utility(board)
    
    value = 2
    
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
        
    return value