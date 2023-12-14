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
    DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 1),
                  (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def __init__(self):
        """
        Initialize the game
        Create an empty board and place the initial pieces
        """
        self.state = GameState.INITIAL

        self.players = None
        self.current_player = None
        self.is_playing_against_ai = False

        self.last_move = None
        self.is_simulated = False

        # Set the initial board
        self.board = np.empty((8, 8), dtype=str)
        for (x, y), player in [((3, 3), "W"), ((3, 4), "B"), ((4, 3), "B"), ((4, 4), "W")]:
            self.board[x][y] = player

        # Set the empty cells
        self.empty_cells = set([(i, j) for i in range(8)
                               for j in range(8) if self.board[i][j] == ""])

        self.state = GameState.PLAYING

    def set_players(self, players):
        """
        Set the players of the game
        Define the starting player
        """
        self.players = players
        self.current_player = np.random.choice(self.players)

    def is_playable_position(self, position):
        """
        Check if the position is playable
        A playable position is an empty cell that is adjacent to an opponent piece
        and that can be flipped in at least one direction
        """
        x, y = position
        if self.board[x][y] != "" or not self.is_cell_on_board(x, y):
            return False
        return any(self.can_flip_in_direction(x, y, direction) for direction in self.DIRECTIONS)

    def get_playable_positions(self):
        """
        Return the playable positions
        """
        return [position for position in self.empty_cells if self.is_playable_position(position)]

    def is_any_direction_playable(self, position):
        return any(self.can_flip_in_direction(position[0], position[1], direction) for direction in self.DIRECTIONS)

    def is_cell_on_board(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def place_piece(self, x, y):
        # Check if the game state is playing and if the position is on the board
        if self.state != GameState.PLAYING or not self.is_cell_on_board(x, y):
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
        for direction in self.DIRECTIONS:
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
                if not self.is_simulated:
                    self.state = GameState.GAME_OVER
                    pygame.event.post(pygame.event.Event(GAME_IS_OVER_EVENT))
                return True

    def is_game_over(self):
        if not self.can_play(self.current_player) and not self.can_play(self.other_player(self.current_player)):
            return True
        return False

    def can_play(self, player):
        return any(self.is_any_direction_playable(position) for position in self.empty_cells)

    def other_player(self, player):
        """
        Return the opponent player for a given player
        """
        return self.players[1] if player == self.players[0] else self.players[0]

    def can_flip_in_direction(self, x, y, direction):
        """
        Check if pieces can be flipped in a direction
        """
        if direction is None:
            return False

        # Checking position
        actual_position = np.array([x, y]) + direction
        # Check if an opponent piece is found
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
        """
        Return the score of a player
        """
        return np.count_nonzero(self.board == player_symbol)

    def undo_last_move(self) -> None:
        """
        Undo the last move
        """
        if self.last_move is None:
            return
        x, y = self.last_move
        self.board[x][y] = ""
        self.empty_cells.add((x, y))
        self.current_player = self.other_player(self.current_player)
        self.last_move = None

    def get_hash(self):
        """
        Return the hash of the board
        """
        return hashlib.md5(self.board.tobytes()).hexdigest()

    def get_winner(self) -> str:
        """
        Return the winner of the game or "Tie" if the game is a tie
        """
        p1 = self.get_player_score(self.players[0].symbol)
        p2 = self.get_player_score(self.players[1].symbol)
        if p1 > p2:
            return f"{self.players[0].name} won!"
        elif p1 < p2:
            return f"{self.players[1].name} won!"
        else:
            return "Tie"
