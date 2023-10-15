import pygame
from view.screen import MainMenu

pygame.init()

running = True

main_menu = MainMenu(1280, 720, "Othello")
current_screen = main_menu

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for visual_component in current_screen.visual_components:
        visual_component.process()

    current_screen.draw()

pygame.quit()
