import random
import ChessEngine
import math
import copy


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
        player = gs.whiteToMove
        depth = 2
        move, score = minimax(gs, player, depth)
        self.update_move(move, score, depth)


### METRICS TO ANALYZE HOW GOOD THE POSITION IS
def howManyPiecesLost(gs: ChessEngine.GameState, pov):
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
            white += 1
        elif piece == 'bp':
            black += 1
        elif (piece == 'bB') | (piece == 'bN'):
            black += 3
        elif piece == 'bR':
            black += 5
        elif piece == 'bK':
            black += 1
    if pov:
        return white - black
    else:
        return black - white


def utility(gs, pov):
    return howManyPiecesLost(gs, pov)


### Implement MiniMax algorithm.
### Utility for starters: how many pieces the opponent looses.
### Depth at first: two

# given gamestate, return move
def minimax(gs, pov, depth):
    moves = gs.getValidMoves()
    max = -math.inf
    maxMove = moves[0]
    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        nextGameStateUtility = minValue(nextGameState, pov, depth - 1)
        if nextGameStateUtility > max:
            max = nextGameStateUtility
            maxMove = move
    return maxMove, max


def minValue(gs, pov, depth):
    if depth == 0:
        return utility(gs, pov)

    moves = gs.getValidMoves()
    min = math.inf

    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        nextGameStateUtility = maxValue(nextGameState, pov, depth - 1)
        if nextGameStateUtility < min:
            min = nextGameStateUtility
    return min


def maxValue(gs, pov, depth):
    if depth == 0:
        return utility(gs, pov)

    moves = gs.getValidMoves()
    max = -math.inf
    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        nextGameStateUtility = minValue(nextGameState, pov, depth - 1)
        if nextGameStateUtility > max:
            max = nextGameStateUtility
    return max