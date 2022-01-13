import random
import ChessEngine
import copy
import math

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

    def findBestMove(self, gs):
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
        ## player white: true, player black: false
        player_turn = gs.whiteToMove
        max_depth = 4
       
        ## Iterative deepening with alpha beta ##
        for depth in range(2, max_depth + 1, 2):
            print('Current depth = ', depth)
            score, move = alpha_beta(gs, True, -math.inf, math.inf, depth, player_turn)
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

    return white - black if is_white_turn else black - white

def isChecked(gs: ChessEngine.GameState, is_white_turn):
    checkExists = gs.checkForPinsAndChecks()[0]
    if checkExists:
        return 1 if gs.whiteToMove == is_white_turn else -1
    else:
        return 0

def central_pieces(gs: ChessEngine.GameState, is_white_turn):
    white = 0
    black = 0
    board = gs.board

    central_squares       = [board[i] for i in [14, 15, 20, 21]]
    outer_central_squares = [board[i] for i in [13, 16, 19, 22]]

    for piece in central_squares:
        if piece[0] == 'w':
            white += 0.1
        elif piece[0] == 'b':
            black += 0.1
    for piece in outer_central_squares:
        if piece[0] == 'w':
            white += 0.05
        elif piece[0] == 'b':
            black += 0.05
    
    return white - black if is_white_turn else black - white



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


def utility(gs, is_white_turn, move_to_current_gs = None):
    if is_start_game(gs):
        #print('CentralPieces Util:', central_pieces(gs, is_white_turn))
        return howManyPiecesLost(gs,is_white_turn) + central_pieces(gs, is_white_turn)
    if is_end_game(gs):
        # print("is endgame!!!!")
        pass
    
    return howManyPiecesLost(gs, is_white_turn) + isChecked(gs, is_white_turn)



### Alpha beta pruning minimax 2. try:
def alpha_beta(gs, is_max_turn, alpha, beta, depth, isWhiteTurn, last_move = None):

    # time_limit, start_time = times
    # diff = time.time() - start_time
    # if time_limit - diff < 5:
    #     depth -= 2 if depth >= 2 else 0
    
    if depth == 0:
        return utility(gs, isWhiteTurn, last_move), None
    
    moves = gs.getValidMoves()
    best_value = -math.inf if is_max_turn else math.inf
    best_move = None

    for move in moves:
        childGameState = copy.deepcopy(gs)
        childGameState.makeMove(move)
        utility_child = alpha_beta(childGameState, not is_max_turn, alpha, beta, depth - 1, not isWhiteTurn, move)[0]

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

