import pygame
from view.screen import MainMenu, PlayScreen
from constants.events import START_HUMAN_VS_HUMAN_EVENT, START_HUMAN_VS_AI_EVENT, GAME_IS_OVER_EVENT
from game.player import Player
import random

pygame.init()

running = True

main_menu = MainMenu(1280, 720, "Othello")
play_screen = PlayScreen(1280, 720, "Othello - Play")
current_screen = main_menu

clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == START_HUMAN_VS_HUMAN_EVENT:
            players = (Player("Player 1", "B"), Player("Player 2", "W"))
            current_screen = play_screen
            current_screen.game.set_players(players)
        elif event.type == START_HUMAN_VS_AI_EVENT:
            players = (Player("Player 1", "B"),
                       Player("AI", "W", is_ai=True))
            current_screen = play_screen
            current_screen.game.set_players(players)
            current_screen.game.is_playing_against_ai = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == play_screen:
                current_screen.process_mouse_click()
        elif event.type == GAME_IS_OVER_EVENT:
            # Open alert box
            pass

    for visual_component in current_screen.visual_components:
        visual_component.process()

    current_screen.draw()
    clock.tick(60)

pygame.quit()
