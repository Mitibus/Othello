import numpy as np
import pygame
from constants.events import GAME_IS_OVER_EVENT


class OthelloGame:
    def __init__(self):
        self.board = np.empty((8, 8), dtype=str)
        self.empty_cells = set([(i, j) for i in range(8)
                               for j in range(8) if self.board[i][j] == ""])
        self.players = None
        self.current_player = None
        self.is_playing_against_ai = False

        # Set the initial board
        self.board[3][3] = "W"
        self.empty_cells.discard((3, 3))
        self.board[3][4] = "B"
        self.empty_cells.discard((3, 4))
        self.board[4][3] = "B"
        self.empty_cells.discard((4, 3))
        self.board[4][4] = "W"
        self.empty_cells.discard((4, 4))

    def set_players(self, players):
        self.players = players
        self.current_player = players[0]

    def get_playable_positions(self):
        # Return a list of playable positions for the current player around the opponent pieces where cells are empty
        playable_positions = []

        for empty_cell in self.empty_cells:
            directions = [(1, 0), (1, 1), (0, 1), (-1, 1),
                          (-1, 0), (-1, -1), (0, -1), (1, -1)]
            for direction in directions:
                if self.is_playable_position(empty_cell, direction):
                    playable_positions.append(tuple(empty_cell))
                    break

        return playable_positions

    def is_playable_position(self, position, direction=None):
        around_position = np.array(position) + direction

        # Check if the position is on the board
        if not self.is_cell_on_board(around_position[0], around_position[1]):
            return False

        # Check if the cell contains the opponent piece
        if self.board[around_position[0]][around_position[1]] != self.current_player.opponent_symbol:
            return False

        while self.is_cell_on_board(around_position[0], around_position[1]):
            around_position += direction

            # CHeck if the position is on the board
            if not self.is_cell_on_board(around_position[0], around_position[1]):
                return False

            # Check if the cell is empty
            if self.board[around_position[0]][around_position[1]] == "":
                return False

            # Check if the cell contains the current player piece
            if self.board[around_position[0]][around_position[1]] == self.current_player.symbol:
                return True

        return False

    def is_cell_on_board(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def place_piece(self, x, y):
        # Check if cell is on the board
        if not self.is_cell_on_board(x, y):
            return False

        # Check if the position is playable
        playable_positions = self.get_playable_positions()
        if (x, y) not in playable_positions:
            return False

        # Place the piece
        self.board[x][y] = self.current_player.symbol
        self.empty_cells.discard((x, y))

        # Flip the opponent pieces
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1),
                      (-1, 0), (-1, -1), (0, -1), (1, -1)]

        for direction in directions:
            print(np.array([x, y]), np.array([x, y]) + direction,
                  self.can_flip_in_direction(x, y, direction))
            if self.can_flip_in_direction(x, y, direction):
                self.flip_in_direction(x, y, direction)

        # Change the current player
        self.current_player = self.players[(
            self.players.index(self.current_player) + 1) % 2]

        # Check if the game is over
        if len(self.get_playable_positions()) == 0:
            self.current_player = self.players[(
                self.players.index(self.current_player) + 1) % 2]

            if len(self.get_playable_positions()) == 0:
                return True

    def is_game_over(self):
        if not self.can_play(self.current_player) and not self.can_play(self.other_player(self.current_player)):
            # Raise a pygame event to display the winner
            pygame.event.post(pygame.event.Event(GAME_IS_OVER_EVENT))
            return True
        return False

    def can_play(self, player):
        return any(self.is_playable_position(position) for position in self.empty_cells)

    def other_player(self, player):
        return self.players[1] if player == self.players[0] else self.players[0]

    def can_flip_in_direction(self, x, y, direction):
        return self.check_direction(x, y, direction, lambda symbol: symbol == self.current_player.symbol)

    def check_direction(self, x, y, direction, condition):
        actual_position = np.array([x, y]) + direction
        while self.is_cell_on_board(actual_position[0], actual_position[1]):
            if condition(self.board[actual_position[0]][actual_position[1]]):
                return True
            actual_position += direction
        return False

    def flip_in_direction(self, x, y, direction):
        actual_position = np.array([x, y]) + direction

        while self.board[actual_position[0]][actual_position[1]] != self.current_player.symbol:
            self.board[actual_position[0]][actual_position[1]
                                           ] = self.current_player.symbol
            actual_position += direction

    def get_player_score(self, player_symbol):
        return np.count_nonzero(self.board == player_symbol)
