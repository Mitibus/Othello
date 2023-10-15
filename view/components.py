import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, screen=None, position=(0, 0), size=(10, 10), text="Button", background_color=(0, 0, 0), text_color=(0, 0, 0), hovered_color=(0, 0, 0), border_color=None, font_size=30, on_click_function=None, one_press=False):
        super().__init__()
        self.x, self.y = position
        self.width, self.height = size
        self.on_click_function = on_click_function
        self.one_press = one_press
        self.already_pressed = False
        self.text = text
        self.screen = screen
        self.background_color = background_color
        self.hovered_color = hovered_color
        self.text_color = text_color
        self.font_size = font_size
        self.border_color = border_color

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_surface.fill(self.background_color)
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.button_surf = pygame.font.SysFont(
            'assets/TechnoRaceItalic.otf', self.font_size).render(self.text, True, self.text_color)

    def process(self):
        # Reset button color
        self.button_surface.fill(self.background_color)

        mouse_position = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_position):
            # Button is hovered
            self.button_surface.fill(self.hovered_color)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                # Button is pressed
                if self.one_press:
                    self.on_click_function()
                elif not self.already_pressed:
                    self.on_click_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False

        self.button_surface.blit(self.button_surf, [
            self.button_rect.width / 2 - self.button_surf.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_surf.get_rect().height / 2
        ])

        self.screen.blit(self.button_surface, self.button_rect)

    def delete(self):
        self.screen.fill((0, 0, 0), self.button_rect)
