import random
import time


class Player:
    def __init__(self, name, symbol, is_ai=False):
        self.name = name
        self.symbol = symbol
        self.opponent_symbol = "W" if symbol == "B" else "B"
        self.is_ai = is_ai

    def place_piece(self, x, y, game):
        if self.is_ai:
            time.sleep(1)
            available_moves = game.get_playable_positions()
            move = random.choice(available_moves)
            game.place_piece(move[0], move[1])
        else:
            game.place_piece(x, y)
