import pygame
from UI.main_menu import MainMenu
from UI.game_play import GamePlay
from UI.pause import Pause
from UI.highscores import Highscores
from score import Score
from gamedata import GameData
from parse_config import Config

pygame.init()

screen = pygame.display.set_mode((1900, 1730))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


config = Config.get_configuration("../config.json")
score = Score()
highscores = Highscores(screen)

state = "menu"
running = True
new_game = True

score.save_score("saad", 1200)

while running:
    screen.fill((0, 0, 0)) 
    
    if state == "menu":
        if new_game:
            menu = MainMenu(screen)
            game_data = GameData(config)
            pause = Pause(screen)
            game_play = GamePlay(screen, game_data)
            new_game = False
            
        action = menu.handle_events()
        
        if action == "quit":
            running = False
        elif action == "start":
            state = "gameplay"
        elif action == "highscores":
            state = "highscores"
            
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
            
        game_play.update()
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

    elif state == "highscores":
        action = highscores.handle_events()
        
        if action == "quit":
            running = False
        elif action == "menu":
            state = "menu"
            
        highscores.update(score.get_scores)
        highscores.draw()

    clock.tick(60) 

pygame.quit()