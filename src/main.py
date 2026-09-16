import pygame
import UI.main_menu as main

pygame.init()
screen = pygame.display.set_mode((1900, 1730))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen.blit(main.border_x, (0, 0))
        screen.blit(main.border_y, (1890, 0))
        screen.blit(main.border_x, (0, 1720))
        screen.blit(main.border_y, (0, 0))
        ##########################
        screen.blit(main.border_inside_x, (20, 20))
        # screen.blit(main.border_y, (1880, 10))
        # screen.blit(main.border_x, (0, 1710))
        # screen.blit(main.border_y, (10, 10))
        pygame.display.flip()

pygame.quit()