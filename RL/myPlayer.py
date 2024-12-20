import Goban
from playerInterface import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from random import choice

class myPlayer(PlayerInterface):
    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self.turns = 0
        self._last_move = None

    def getPlayerName(self):
        return "Minimax Player"

    # def evaluate_using_final_score(self, board):
    #     print(board.compute_score())
    #     score_str = board.final_go_score()
    #     if score_str.startswith("W+"):
    #         margin = int(score_str[2:])
    #         return margin if self._mycolor == Goban.Board._WHITE else -margin
    #     elif score_str.startswith("B+"):
    #         margin = int(score_str[2:])
    #         return margin if self._mycolor == Goban.Board._BLACK else -margin
    #     else:
    #         return 0  

    def evaluate(self, board):
        black_score, white_score = board.compute_score()
        return black_score - white_score

    def minimax(self, board, depth, maximizingPlayer, alpha, beta):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board)
            # return self.evaluate_using_final_score(board)

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in board.legal_moves():
                if move != -1:  
                    board.push(move)
                    eval = self.minimax(board, depth-1, False, alpha, beta)
                    board.pop()
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return maxEval
        else:
            minEval = float('inf')
            for move in board.legal_moves():
                if move != -1:  
                    board.push(move)
                    eval = self.minimax(board, depth-1, True, alpha, beta)
                    board.pop()
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return minEval
        
    def minimax_root(self, board, depth, maximizingPlayer):
        legal_moves = board.legal_moves()  
        scores = {}
        with ThreadPoolExecutor(max_workers=len(legal_moves)) as executor:
            future_to_move = {}
            for move in legal_moves:
                if move == -1:  
                    continue  
                board_copy = deepcopy(board)
                board_copy.push(move)  
                future = executor.submit(self.minimax, board_copy, depth - 1, not maximizingPlayer, float('-inf'), float('inf'))
                future_to_move[future] = move
            for future in as_completed(future_to_move):
                move = future_to_move[future]
                score = future.result()
                scores[move] = score

        best_move = max(scores, key=scores.get, default=-1)  
        return "PASS" if best_move == -1 else board.move_to_str(best_move)

    def getPlayerMove(self):
        if self._board.is_game_over():
            return "PASS"
        if self._last_move == "PASS":
            black_score, white_score = self._board.compute_score()
            my_color = self._mycolor
            opponent_color = Goban.Board._BLACK if my_color == Goban.Board._WHITE else Goban.Board._WHITE
            if (my_color == Goban.Board._BLACK and black_score > white_score + 1) or \
                (my_color == Goban.Board._WHITE and white_score > black_score + 1):
                return "PASS"
            
        if self.turns < 10:
            moves = self._board.legal_moves()  
            move = choice(moves)
            self._board.push(move)  
            self.turns += 1
            return "PASS" if move == -1 else self._board.move_to_str(move)
        elif self.turns < 20:
            move = self.minimax_root(self._board, 2, True)  
            self._board.push(Goban.Board.name_to_flat(move))  
            self.turns += 1
            return move
        
        elif self.turns < 40:
            move = self.minimax_root(self._board, 3, True)  
            self._board.push(Goban.Board.name_to_flat(move))  
            self.turns += 1
            return move
        else:
            move = self.minimax_root(self._board, 5, True)  
            self._board.push(Goban.Board.name_to_flat(move))  
            self.turns += 1
            return move

    def playOpponentMove(self, move):
        if move in [self._board.move_to_str(m) for m in self._board.legal_moves()]:
            self._board.push(Goban.Board.name_to_flat(move))
            self._last_move = move

    def newGame(self, color):
        self._mycolor = color

    def endGame(self, winner):
        pass
