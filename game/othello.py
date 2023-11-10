import numpy as np
import pygame
import hashlib
from constants.events import GAME_IS_OVER_EVENT
from enum import Enum


class GameState(Enum):
    INITIAL = 0
    PLAYING = 1
    GAME_OVER = 2


class OthelloGame:
    def __init__(self):
        self.state = GameState.INITIAL

        self.board = np.empty((8, 8), dtype=str)
        self.empty_cells = set([(i, j) for i in range(8)
                               for j in range(8) if self.board[i][j] == ""])
        self.players = None
        self.current_player = None
        self.is_playing_against_ai = False

        self.last_move = None

        # Set the initial board
        self.board[3][3] = "W"
        self.empty_cells.discard((3, 3))
        self.board[3][4] = "B"
        self.empty_cells.discard((3, 4))
        self.board[4][3] = "B"
        self.empty_cells.discard((4, 3))
        self.board[4][4] = "W"
        self.empty_cells.discard((4, 4))

        self.state = GameState.PLAYING

    def set_players(self, players):
        self.players = players
        self.current_player = players[0]

    def get_playable_positions(self):
        # Return a list of playable positions for the current player around the opponent pieces where cells are empty
        playable_positions = []

        for empty_cell in self.empty_cells:
            if self.is_adjacent_to_opponent(empty_cell) and self.is_any_direction_playable(empty_cell):
                playable_positions.append(tuple(empty_cell))

        return playable_positions

    def is_playable_position(self, position, direction):
        if not self.is_cell_on_board(position[0], position[1]):
            return False
        if self.board[position[0]][position[1]] != "":
            return False
        return self.check_direction(position[0], position[1], direction)

    def is_any_direction_playable(self, position):
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1),
                      (-1, 0), (-1, -1), (0, -1), (1, -1)]
        return any(self.check_direction(position[0], position[1], direction) for direction in directions)

    def is_cell_on_board(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def place_piece(self, x, y):
        # Check if the game state is playing
        if self.state != GameState.PLAYING:
            return False

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
        self.last_move = (x, y)

        # Flip the opponent pieces
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1),
                      (-1, 0), (-1, -1), (0, -1), (1, -1)]

        for direction in directions:
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
            self.state = GameState.GAME_OVER
            pygame.event.post(pygame.event.Event(GAME_IS_OVER_EVENT))
            return True
        return False

    def can_play(self, player):
        return any(self.is_any_direction_playable(position) for position in self.empty_cells)

    def other_player(self, player):
        return self.players[1] if player == self.players[0] else self.players[0]

    def can_flip_in_direction(self, x, y, direction):
        return self.check_direction(x, y, direction)

    def check_direction(self, x, y, direction):
        if direction is None:
            return False

        actual_position = np.array([x, y]) + direction
        found_opponent_piece = False

        while self.is_cell_on_board(actual_position[0], actual_position[1]):
            cell = self.board[actual_position[0]][actual_position[1]]
            if cell == "":
                return False
            elif cell == self.current_player.opponent_symbol:
                found_opponent_piece = True
            elif cell == self.current_player.symbol:
                return found_opponent_piece
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

    def is_adjacent_to_opponent(self, cell):
        x, y = cell
        adjacent_cells = [(x + dx, y + dy) for dx in [-1, 0, 1]
                          for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]

        for adj_cell in adjacent_cells:
            if self.is_cell_on_board(adj_cell[0], adj_cell[1]) and self.board[adj_cell[0]][adj_cell[1]] == self.current_player.opponent_symbol:
                return True
        return False

    def undo_last_move(self) -> None:
        if self.last_move is None:
            return
        x, y = self.last_move
        self.board[x][y] = ""
        self.empty_cells.add((x, y))
        self.current_player = self.other_player(self.current_player)
        self.last_move = None

    def get_hash(self):
        # Convert board to a byte array
        board_bytes = self.board.tobytes()

        # Create a md5 hash of the board
        hash_md5 = hashlib.md5()
        hash_md5.update(board_bytes)

        return hash_md5.hexdigest()

    def __str__(self):
        return self.get_hash()
