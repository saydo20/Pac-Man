import pygame
import time


class GameOver:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.border_x = pygame.Surface((1900, 10))
        self.border_y = pygame.Surface((10, 1730))
        self.border_inside_x = pygame.Surface((1860, 15))
        self.border_inside_y = pygame.Surface((15, 1690))
        self.border_inside_x2 = pygame.Surface((1800, 10))
        self.border_inside_y2 = pygame.Surface((10, 1300))
        self.border_inside_x3 = pygame.Surface((1760, 10))
        self.border_inside_y3 = pygame.Surface((10, 1260))
        self.border_yellow_x = pygame.Surface((800, 10))
        self.border_yellow_y = pygame.Surface((10, 450))
        self.border_red_x = pygame.Surface((770, 10))
        self.border_red_y = pygame.Surface((10, 400))
        self.last_switch = time.monotonic()
        self.last_switch_pasue = time.monotonic()

        self.title = pygame.image.load("UI/images/title.png")
        self.title_dark = pygame.image.load("UI/images/title_dark.png")
        self.paused_section = pygame.image.load("UI/images/paused.png")
        self.resume_normal = pygame.image.load("UI/images/resume_normal.png")
        self.resume_hover = pygame.image.load("UI/images/resume_hover.png")
        self.return_normal = pygame.image.load("UI/images/return_normal.png")
        self.return_hover = pygame.image.load("UI/images/return_hover.png")
        self.game_over = pygame.image.load("UI/images/game_over.png")
        self.final_score = pygame.image.load("UI/images/final_score.png")
        self.enter_name = pygame.image.load("UI/images/enter_name.png")
        self.current_title = self.title
        self.paused_show = True
        self.current_resume = self.resume_normal
        self.current_return = self.return_normal
        self.selected = 0

        blue_color = (9, 9, 232)
        for surface in [self.border_inside_x, self.border_inside_y,
                        self.border_inside_x2, self.border_inside_y2,
                        self.border_inside_x3, self.border_inside_y3]:
            surface.fill(blue_color)

        self.title = pygame.image.load("UI/images/title.png")
        self.title_dark = pygame.image.load("UI/images/title_dark.png")
        self.pac_man_title = pygame.image.load("UI/images/pacman.png")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "gameplay"

    def update(self):
        now = time.monotonic()
        if now - self.last_switch >= 1:
            self.current_title = self.title_dark if self.current_title == self.title else self.title
            self.last_switch = now
        if now - self.last_switch_pasue >= 0.3:
            self.paused_show = not self.paused_show
            self.last_switch_pasue = now

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.border_x, (0, 0))
        self.screen.blit(self.border_y, (1890, 0))
        self.screen.blit(self.border_x, (0, 1720))
        self.screen.blit(self.border_y, (0, 0))
        self.screen.blit(self.border_inside_x, (20, 20))
        self.screen.blit(self.border_inside_y, (1865, 20))
        self.screen.blit(self.border_inside_y, (20, 20))
        self.screen.blit(self.border_inside_x, (20, 1695))

        self.screen.blit(self.current_title, (600, 50))

        self.screen.blit(self.border_inside_x2, (50, 250))
        self.screen.blit(self.border_inside_y2, (50, 250))
        self.screen.blit(self.border_inside_y2, (1840, 250))
        self.screen.blit(self.border_inside_x2, (50, 1550))

        self.screen.blit(self.border_inside_x3, (70, 270))
        self.screen.blit(self.border_inside_y3, (70, 270))
        self.screen.blit(self.border_inside_y3, (1820, 270))
        self.screen.blit(self.border_inside_x3, (70, 1530))

        self.screen.blit(self.border_yellow_x, (550, 670))
        self.screen.blit(self.border_yellow_y, (550, 670))
        self.screen.blit(self.border_yellow_x, (550, 1110))
        self.screen.blit(self.border_yellow_y, (1350, 670))

        self.screen.blit(self.game_over, (620, 600))
        self.screen.blit(self.final_score, (780, 720))


        pygame.display.flip()
