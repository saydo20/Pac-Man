import pygame
from UI.main_menu import MainMenu
from UI.game_play import GamePlay
from gamedata import GameData
import json

pygame.init()
screen = pygame.display.set_mode((1900, 1730))

menu = MainMenu(screen)
game_play = GamePlay(screen)
with open("../config.json") as f:
    data = json.load(f)
game_data = GameData(data)
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

        game_play.draw(game_data.maze.maze)
        game_play.update()

pygame.quit()