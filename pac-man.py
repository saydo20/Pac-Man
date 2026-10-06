import pygame
from sys import argv

from UI.main_menu import MainMenu
from UI.game_play import GamePlay
from UI.pause import Pause
from UI.highscores import Highscores
from UI.game_over import GameOver
from UI.win import GameWin
from UI.instructions import Instructions
from src.score import Score
from src.gamedata import GameData
from src.parse_config import Config


pygame.init()

screen = pygame.display.set_mode((1900, 1730))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

if len(argv) > 1:
    file_name = argv[1]

try:
    config = Config.get_configuration(file_name)
except (FileNotFoundError, PermissionError, Exception):
    config = Config.get_configuration("config.json")

score = Score()
highscores = Highscores(screen)
instructions = Instructions(screen)

state = "menu"
running = True
new_game = True

while running:
    screen.fill((0, 0, 0))

    if state == "menu":
        if new_game:
            menu = MainMenu(screen)
            game_data = GameData(config)
            pause = Pause(screen)
            game_over = GameOver(screen, game_data)
<<<<<<< HEAD
            game_win =  GameWin(screen, game_data)
=======
            game_win = GameWin(screen, game_data)
>>>>>>> saad
            game_play = GamePlay(screen, game_data)
            new_game = False

        action = menu.handle_events()

        if action == "quit":
            running = False
        elif action == "start":
            state = "gameplay"
        elif action == "highscores":
            state = "highscores"
        elif action == "instructions":
            state = "instructions"

        menu.update()
        menu.draw()

    elif state == "gameplay":
        action = game_play.handle_events()

        if action == "quit":
            running = False
        elif action == "pause":
            state = "pause"
        elif action == "menu":
            state = "menu"
            new_game = True

        if game_play.update() == "game_over":
            state = "game_over"
<<<<<<< HEAD
        if game_play.update() == "game_win":
            state = "game_win"
=======
            continue
        if game_play.update() == "game_win":
            state = "game_win"
            continue
>>>>>>> saad
        game_play.draw()

    elif state == "pause":
        action = pause.handle_events()

        if action == "quit":
            running = False
        elif action == "gameplay":
            state = "gameplay"
        elif action == "menu":
            state = "menu"
            new_game = True

        pause.update()
        pause.draw()

    elif state == "game_over":
        action = game_over.handle_events()

        if action == "quit":
            running = False
        else:
            if action is not None:
                name, player_score = action
                score.save_score(name, player_score)
                new_game = True
                state = "menu"

        game_over.update()
        game_over.draw()
    elif state == "game_win":
        action = game_win.handle_events()

        if action == "quit":
            running = False
        else:
            if action is not None:
                name, player_score = action
                score.save_score(name, player_score)
                new_game = True
                state = "menu"

        game_win.update()
        game_win.draw()

    elif state == "highscores":
        action = highscores.handle_events()

        if action == "quit":
            running = False
        elif action == "menu":
            state = "menu"

        highscores.update(score.get_scores)
        highscores.draw()

    elif state == "instructions":
        action = instructions.handle_events()

        if action == "quit":
            running = False
        elif action == "menu":
            state = "menu"

        instructions.update()
        instructions.draw()

    clock.tick(60)

pygame.quit()
