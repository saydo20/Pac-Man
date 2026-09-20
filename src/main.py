import pygame
from UI.main_menu import MainMenu
from UI.game_play import GamePlay
from gamedata import GameData
from parse_config import Config

pygame.init()
screen = pygame.display.set_mode((1900, 1730))

menu = MainMenu(screen)
config = Config.get_configuration("../config.json")
game_data = GameData(config)
game_play = GamePlay(screen, game_data)
state = "menu"
running = True
while running:
    if state == "menu":
        action = menu.handle_events()
        if action == "quit":
            running = False
        elif action == "start":
            state = "gameplay"
            screen.fill((0, 0, 0))
            continue

        menu.update()
        menu.draw()
    elif state == "gameplay":
        action = game_play.handle_events()
        if action == "quit":
            running = False

        game_play.update()
        game_play.draw()

pygame.quit()