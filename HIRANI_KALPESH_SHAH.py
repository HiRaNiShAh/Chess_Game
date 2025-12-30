import sys
import copy
import time
from config import *
from board import Board

# DISCLAIMER:
# This submission does NOT use reinforcement learning, supervised learning,
# neural networks, trained heuristics, adaptive policies, or any learning-based
# methods. The agent relies purely on deterministic game-tree search and
# handcrafted heuristic evaluation.
class HIRANI_KALPESH_SHAH:
    def __init__(self, board):
        self.board = board
        self.depth = 2  


    def get_best_move(self):
        legal_moves = self.board.get_legal_moves()
        if not legal_moves:
            return None

        best_move = None

        if self.board.white_to_move:
            best_score = -10**9
            for move in legal_moves:
                self.board.make_move(move)
                score = self._minimax(self.depth - 1, False, -10**9, 10**9)
                self.board.undo_move()
                if score > best_score:
                    best_score = score
                    best_move = move
        else:
            best_score = 10**9
            for move in legal_moves:
                self.board.make_move(move)
                score = self._minimax(self.depth - 1, True, -10**9, 10**9)
                self.board.undo_move()
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move


    def evaluate_board(self):
        score = 0
        board = self.board.board

        for r in range(8):
            for c in range(4):
                piece = board[r][c]
                if piece == '--':
                    continue

                value = PIECE_VALUES[piece]

                if piece[1] == 'P':
                    pst = PAWN_PST[r][c]
                elif piece[1] == 'N':
                    pst = KNIGHT_PST[r][c]
                elif piece[1] == 'B':
                    pst = BISHOP_PST[r][c]
                elif piece[1] == 'K':
                    pst = KING_PST_LATE_GAME[r][c]
                else:
                    pst = 0

                if piece[0] == 'w':
                    score += value + pst
                else:
                    score += value - pst

        return score


    def _minimax(self, depth, maximizing, alpha, beta):
        state = self.board.get_game_state()

        if state == "checkmate":
            return -600 if maximizing else 600
        if state == "stalemate" or depth == 0:
            return self.evaluate_board()

        moves = self.board.get_legal_moves()
        if not moves:
            return self.evaluate_board()

        if maximizing:
            max_eval = -10**9
            for move in moves:
                self.board.make_move(move)
                eval = self._minimax(depth - 1, False, alpha, beta)
                self.board.undo_move()
                if eval > max_eval:
                    max_eval = eval
                if eval > alpha:
                    alpha = eval
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = 10**9
            for move in moves:
                self.board.make_move(move)
                eval = self._minimax(depth - 1, True, alpha, beta)
                self.board.undo_move()
                if eval < min_eval:
                    min_eval = eval
                if eval < beta:
                    beta = eval
                if beta <= alpha:
                    break
            return min_eval


################################################################################################################
