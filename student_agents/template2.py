import random
import ChessEngine
import math
import copy
import sys
import time

## Sebastian Volz
## Timo Luebbing

class Agent:
    def __init__(self):
        self.move_queue = None

    def get_move(self):
        move = None
        while not self.move_queue.empty():
            move = self.move_queue.get()
        return move

    def update_move(self, move, score, depth):
        """
        :param move: Object of class Move, like a list element of gamestate.getValidMoves()
        :param score: Integer; not really necessary, just for informative printing
        :param depth: Integer; not really necessary, just for informative printing
        :return:
        """
        self.move_queue.put([move, score, depth])

    def clear_queue(self, outer_queue):
        self.move_queue = outer_queue

    def findBestMove(self, gs: ChessEngine.GameState):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        validMoves : list
            list of valid moves
        returnQueue : Queue
            multithreading queue

        Returns
        -------
        none

        """
        ### player white: true, player black: false
        player_turn = gs.whiteToMove
        depth = 2

        score, move = alpha_beta(gs, player_turn, -math.inf, math.inf, depth)
        self.update_move(move, score, depth)
        


### METRICS TO ANALYZE HOW GOOD THE POSITION IS
def howManyPiecesLost(gs: ChessEngine.GameState, is_white_turn):
    # given a gameState and player: return how many pieces the opponent has lost
    white = 0
    black = 0
    for piece in gs.board:
        if piece == 'wp':
            white += 1
        elif (piece == 'wB') | (piece == 'wN'):
            white += 3
        elif piece == 'wR':
            white += 5
        elif piece == 'wK':
            white += 100
        elif piece == 'bp':
            black += 1
        elif (piece == 'bB') | (piece == 'bN'):
            black += 3
        elif piece == 'bR':
            black += 5
        elif piece == 'bK':
            black += 100
    if is_white_turn:
        return white - black
    else:
        return black - white

def isChecked(gs: ChessEngine.GameState, is_white_turn):
    checkExists = gs.checkForPinsAndChecks()[0]
    if checkExists:
        # we are in the position to check
        if gs.whiteToMove == is_white_turn:
            return 1
        # our opponent is in the position to check
        else:
            return -1
    else:
        return 0


def is_start_game(gs):
    board = gs.board
    return board.count("wp") == 6 or board.count("bp") == 6

def is_end_game(gs):
    board = gs.board
    white_pieces = [piece for piece in board if piece[0] == "w"]
    black_pieces = [piece for piece in board if piece[0] == "b"]
    if len(white_pieces) + len(black_pieces) <= 8:
        return True
    pawns = white_pieces.count("wp") + black_pieces.count("bp")
    if pawns <= 4:
        return True
    special_pieces = ["wN", "bN", "wB", "bB", "wR", "bR"]
    return len([piece in special_pieces for piece in white_pieces]) <= 2 or len(
       [piece in special_pieces for piece in black_pieces]) <= 2

def utility(gs, is_max_turn, move_to_current_gs):
    if is_start_game(gs):
        # print("is startgame")
        pass
    if is_end_game(gs):
        # print("is endgame!!!!")
        pass
    
    return howManyPiecesLost(gs, is_max_turn) + isChecked(gs, is_max_turn)


### Implement Alpha-Beta-Search
def alpha_beta_search(gs, is_max_turn, depth):
    pass


def max_value(gs, is_max_turn, alpha, beta, depth):
    if depth == 0:
        return utility(gs, is_max_turn)

    v_max = -math.inf
    moves = gs.getValidMoves()

    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        v_max = max(v_max, min_value(nextGameState, is_max_turn, alpha, beta, depth - 1))
        if v_max >= beta:
            return v_max
        alpha = max(alpha, v_max)
    return v_max


def min_value(gs, is_max_turn, alpha, beta, depth):
    if depth == 0:
        return utility(gs, is_max_turn)

    v_min = math.inf
    moves = gs.getValidMoves()

    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        v_min = min(v_min, max_value(nextGameState, is_max_turn, alpha, beta, depth - 1))
        if v_min <= alpha:
            return v_min
        beta = min(beta, v_min)
    return v_min


### Alpha beta pruning minimax 2. try:
def alpha_beta(gs, is_max_turn, alpha, beta, depth, last_move = None):

    # time_limit, start_time = times
    # diff = time.time() - start_time
    # if time_limit - diff < 5:
    #     depth -= 2 if depth >= 2 else 0
    
    if depth == 0:
        return utility(gs, is_max_turn, last_move), None
    
    moves = gs.getValidMoves()
    best_value = -math.inf if is_max_turn else math.inf
    best_move = None

    for move in moves:
        childGameState = copy.deepcopy(gs)
        childGameState.makeMove(move)
        utility_child = alpha_beta(childGameState, not is_max_turn, alpha, beta, depth - 1, move)[0]

        if is_max_turn and best_value < utility_child:
            best_value = utility_child
            best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        
        elif (not is_max_turn) and best_value > utility_child:
            best_value = utility_child
            best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
    
    return best_value, best_move


### Implement MiniMax algorithm.
### Utility for starters: how many pieces the opponent looses.
### Depth at first: two

# given gamestate, return move
def minimax(gs, is_max_turn, depth):
    moves = gs.getValidMoves()
    max = -math.inf
    maxMove = moves[0]
    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        nextGameStateUtility = minValue(nextGameState, is_max_turn, depth - 1)
        if nextGameStateUtility > max:
            max = nextGameStateUtility
            maxMove = move
    return maxMove


def minValue(gs, is_max_turn, depth):
    if depth == 0:
        return utility(gs, is_max_turn)

    moves = gs.getValidMoves()
    min = math.inf

    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        nextGameStateUtility = maxValue(nextGameState, is_max_turn, depth - 1)
        if nextGameStateUtility < min:
            min = nextGameStateUtility
    return min


def maxValue(gs, is_max_turn, depth):
    if depth == 0:
        return utility(gs, is_max_turn)

    moves = gs.getValidMoves()
    max = -math.inf
    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        nextGameStateUtility = minValue(nextGameState, is_max_turn, depth - 1)
        if nextGameStateUtility > max:
            max = nextGameStateUtility
    return max