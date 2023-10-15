import pygame
from view.color import BACKGROUND_COLOR, WHITE
from view.components import Button


class Screen:
    def __init__(self, width=1280, height=720, title="Othello"):
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.visual_components = pygame.sprite.Group()

        icon = pygame.image.load("assets/icon/icon.jpg")
        pygame.display.set_icon(icon)

    def get_font(self, size):
        return pygame.font.SysFont("assets/font/TechnoRaceItalic.otf", size)

    def draw(self):
        pygame.display.update()


class MainMenu(Screen):
    def __init__(self, width, height, title, background=BACKGROUND_COLOR):
        super().__init__(width, height, title)
        self.background = background
        self.screen.fill(background)

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
        print("Starting human vs human game")
        pass

    def start_human_vs_ai(self):
        print("Starting human vs ai game")
        pass

    def quit(self):
        # Raise pygame quit event
        pygame.event.post(pygame.event.Event(pygame.QUIT))
