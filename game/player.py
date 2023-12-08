import random
import time
import numpy as np
import copy
from loguru import logger
from game.othello import GameState


class Player:
    MAX_DEPTH = 20

    def __init__(self, name, symbol, is_ai=False):
        self.name = name
        self.symbol = symbol
        self.opponent_symbol = "W" if symbol == "B" else "B"
        self.is_ai = is_ai

    def place_piece(self, x, y, game):
        logger.info(f"{self.name} is playing")
        if self.is_ai and game.state == GameState.PLAYING:
            time.sleep(1)
            move = self.best_move(game)
            game.place_piece(move[0], move[1])
            logger.info(
                f"{self.name} is placing a piece at ({move[0]}, {move[1]})")
        else:
            game.place_piece(x, y)
            logger.info(f"{self.name} is placing a piece at ({x}, {y})")

    def best_move(self, game):
        best_move = None
        best_score = -np.inf

        # Make a copy of the game for simulation
        simulated_game = copy.deepcopy(game)

        # Get all playable positions
        playable_positions = simulated_game.get_playable_positions()

        # Iterate through all playable positions
        for x, y in playable_positions:
            # Simulate placing a piece
            simulated_game.place_piece(x, y)

            # Get the score of the simulated game
            score = self.minimax(simulated_game, 0, False)

            # Undo the simulated move
            simulated_game.undo_last_move()

            # If the score is better than the best score, update the best score and best move
            if score > best_score:
                best_score = score
                best_move = (x, y)

        return best_move

    def minimax(self, game, depth, isMaximizing, alpha=-np.inf, beta=np.inf):
        # If the game is over, return the score
        if depth == Player.MAX_DEPTH or game.is_game_over():
            ai_score = game.get_player_score(self.symbol)
            opponent_score = game.get_player_score(self.opponent_symbol)

            return ai_score - opponent_score

        possible_moves = game.get_playable_positions()

        if isMaximizing:
            best_score = -np.inf
            for x, y in possible_moves:
                game.place_piece(x, y)
                score = self.minimax(game, depth + 1, False)
                game.undo_last_move()
                best_score = max(score, best_score)
                if best_score >= beta:
                    break
                alpha = max(alpha, best_score)
            return best_score
        else:
            best_score = np.inf
            for x, y in possible_moves:
                game.place_piece(x, y)
                score = self.minimax(game, depth + 1, True)
                game.undo_last_move()
                best_score = min(score, best_score)
                if best_score <= alpha:
                    break
                beta = min(beta, best_score)
            return best_score
