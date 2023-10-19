import pygame
from view.color import BACKGROUND_COLOR, WHITE, BLACK
from view.components import Button
from constants.events import START_HUMAN_VS_HUMAN_EVENT, START_HUMAN_VS_AI_EVENT
from game.othello import OthelloGame


class Screen:
    def __init__(self, width=1280, height=720, title="Othello", background=BACKGROUND_COLOR):
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.background = background
        self.screen.fill(background)
        self.visual_components = pygame.sprite.Group()

        icon = pygame.image.load("assets/icon/icon.jpg")
        pygame.display.set_icon(icon)

    def get_font(self, size):
        return pygame.font.SysFont("assets/font/TechnoRaceItalic.otf", size)

    def draw(self):
        pygame.display.update()


class MainMenu(Screen):
    def __init__(self, width, height, title, background=BACKGROUND_COLOR):
        super().__init__(width, height, title, background=background)

    def draw(self):
        # Add the title
        title = self.get_font(100).render("Othello", True, WHITE)
        title_rect = title.get_rect()
        title_rect.center = (self.width / 2, 100)
        self.screen.blit(title, title_rect)

        # Add the buttons
        human_vs_human_button = Button(
            self.screen,
            position=(640 - 150, 250),
            size=(300, 100),
            text="Human vs Human",
            background_color=BACKGROUND_COLOR,
            text_color=WHITE,
            hovered_color="#2EAE52",
            border_color=WHITE,
            font_size=50,
            on_click_function=self.start_human_vs_human,
        )

        human_vs_ai_button = Button(
            self.screen,
            position=(640 - 150, 400),
            size=(300, 100),
            text="Human vs AI",
            background_color=BACKGROUND_COLOR,
            text_color=WHITE,
            hovered_color="#2EAE52",
            border_color=WHITE,
            font_size=50,
            on_click_function=self.start_human_vs_ai,
        )

        quit_button = Button(
            self.screen,
            position=(640 - 150, 550),
            size=(300, 100),
            text="Quit",
            background_color=BACKGROUND_COLOR,
            text_color=WHITE,
            hovered_color="#2EAE52",
            border_color=WHITE,
            font_size=50,
            on_click_function=self.quit,
        )

        self.visual_components.add(
            human_vs_human_button, human_vs_ai_button, quit_button)

        # Call the parent draw method
        super().draw()

    def start_human_vs_human(self):
        pygame.event.post(pygame.event.Event(START_HUMAN_VS_HUMAN_EVENT))

    def start_human_vs_ai(self):
        pygame.event.post(pygame.event.Event(START_HUMAN_VS_AI_EVENT))

    def quit(self):
        # Raise pygame quit event
        pygame.event.post(pygame.event.Event(pygame.QUIT))


class PlayScreen(Screen):
    def __init__(self, width, height, title, background=BACKGROUND_COLOR):
        super().__init__(width, height, title, background=background)
        self.game = OthelloGame()

    def draw(self):
        # Divide the screen in two parts
        # First part on the left is the board 720x720, 8x8 grid
        # Second part on the right is the information panel 560x720

        # Draw the board
        self.draw_game_board()

        # Draw the information panel
        self.draw_information_panel()

        # Call the parent draw method
        super().draw()

        # If playing against AI, let the AI play
        if self.game.is_playing_against_ai and self.game.current_player.is_ai:
            self.game.current_player.place_piece(
                None, None, self.game)

    def draw_game_board(self):
        # Draw the board
        board = pygame.Surface((720, 720))
        board.fill(BACKGROUND_COLOR)

        # Draw the grid
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(board, WHITE, (i * 90, j * 90, 90, 90), 1)

        # Draw the pieces
        for i in range(8):
            for j in range(8):
                if self.game.board[i][j] == "W":
                    pygame.draw.circle(
                        board, WHITE, (i * 90 + 45, j * 90 + 45), 40)
                elif self.game.board[i][j] == "B":
                    pygame.draw.circle(
                        board, BLACK, (i * 90 + 45, j * 90 + 45), 40)

        # Get the playable positions
        playable_positions = self.game.get_playable_positions()

        # Draw the playable positions with a gray empty circle
        for playable_position in playable_positions:
            pygame.draw.circle(
                board, (128, 128, 128), (playable_position[0] * 90 + 45, playable_position[1] * 90 + 45), 40)

        # Add the board to the screen
        self.screen.blit(board, (0, 0))

    def draw_information_panel(self):
        # Draw the information panel
        information_panel = pygame.Surface((560, 720))
        information_panel.fill(BACKGROUND_COLOR)

        # Add a title to the information panel
        title = self.get_font(50).render("Othello", True, WHITE)
        title_rect = title.get_rect()
        title_rect.center = (280, 50)
        information_panel.blit(title, title_rect)

        # Add a subtitle to the information panel
        subtitle = self.get_font(30).render("Informations", True, WHITE)
        subtitle_rect = subtitle.get_rect()
        subtitle_rect.center = (280, 90)
        information_panel.blit(subtitle, subtitle_rect)

        # Add the current player and under the text a circle with the color of the current player
        current_player_text = self.get_font(
            30).render("Current Player", True, WHITE)
        current_player_text_rect = current_player_text.get_rect()
        current_player_text_rect.center = (280, 250)
        information_panel.blit(current_player_text, current_player_text_rect)

        # Add the current player circle
        if self.game.current_player.symbol == "W":
            pygame.draw.circle(information_panel, WHITE, (280, 350), 40)
        else:
            pygame.draw.circle(information_panel, BLACK, (280, 350), 40)

        # Add the score
        score_text = self.get_font(30).render("Score", True, WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (280, 450)
        information_panel.blit(score_text, score_text_rect)

        # Draw a circle for the white player and right the score next to it
        pygame.draw.circle(information_panel, WHITE, (245, 550), 40)
        white_score = self.get_font(30).render(
            str(self.game.get_player_score("W")), True, WHITE)
        white_score_rect = white_score.get_rect()
        white_score_rect.center = (245, 650)
        information_panel.blit(white_score, white_score_rect)

        # Draw a circle for the black player and right the score next to it
        pygame.draw.circle(information_panel, BLACK, (345, 550), 40)
        black_score = self.get_font(30).render(
            str(self.game.get_player_score("B")), True, WHITE)
        black_score_rect = black_score.get_rect()
        black_score_rect.center = (345, 650)
        information_panel.blit(black_score, black_score_rect)

        self.screen.blit(information_panel, (720, 0))

    def process_mouse_click(self):
        # Get the position of the mouse
        mouse_position = pygame.mouse.get_pos()

        # Check if the mouse is on the board
        if mouse_position[0] < 720:
            # Get the position of the mouse on the grid
            grid_position = (mouse_position[0] // 90, mouse_position[1] // 90)

        if not self.game.current_player.is_ai:
            self.game.current_player.place_piece(
                grid_position[0], grid_position[1], self.game)
