import pygame
import time


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.border_x = pygame.Surface((1900, 10))
        self.border_y = pygame.Surface((10, 1730))
        self.border_inside_x = pygame.Surface((1860, 15))
        self.border_inside_y = pygame.Surface((15, 1690))
        self.border_inside_x2 = pygame.Surface((1800, 10))
        self.border_inside_y2 = pygame.Surface((10, 1300))
        self.border_inside_x3 = pygame.Surface((1760, 10))
        self.border_inside_y3 = pygame.Surface((10, 1260))

        self.border_x.fill((0, 0, 128))
        self.border_y.fill((0, 0, 128))

        blue_color = (9, 9, 232)
        for surface in [self.border_inside_x, self.border_inside_y,
                        self.border_inside_x2, self.border_inside_y2,
                        self.border_inside_x3, self.border_inside_y3]:
            surface.fill(blue_color)

        self.title = pygame.image.load("UI/images/title.png")
        self.title_dark = pygame.image.load("UI/images/title_dark.png")
        self.pac_man_title = pygame.image.load("UI/images/pacman.png")

        self.start_game = pygame.image.load("UI/images/start_game.png")
        self.view_highscores = pygame.image.load(
            "UI/images/veiw_highscores.png")
        self.instructions = pygame.image.load("UI/images/instractions.png")
        self.exit_button = pygame.image.load("UI/images/exit.png")

        self.start_game_selected = pygame.image.load(
            "UI/images/start_game_selected.png")
        self.view_highscores_selected = pygame.image.load(
            "UI/images/veiw_highscores_selected.png")
        self.instructions_selected = pygame.image.load(
            "UI/images/instractions_selected.png")
        self.exit_button_selected = pygame.image.load(
            "UI/images/exit_selected.png")

        self.arrow = pygame.image.load("UI/images/arow.png")
        self.coin = pygame.image.load("UI/images/insert_coin.png")

        self.selected = 0
        self.arrow_places = [800, 900, 1000, 1100]
        self.last_switch = time.monotonic()
        self.last_switch_coin = time.monotonic()
        self.current_title = self.title
        self.show_coin = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % 4
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % 4
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:
                        return "start"
                    elif self.selected == 1:
                        return "instructions"
                    elif self.selected == 2:
                        return "highscores"
                    elif self.selected == 3:
                        return "quit"
        return None

    def update(self):
        now = time.monotonic()
        if now - self.last_switch >= 0.5:
            self.current_title = self.title_dark if self.current_title == self.title else self.title
            self.last_switch = now

        if now - self.last_switch_coin >= 0.3:
            self.show_coin = not self.show_coin
            self.last_switch_coin = now

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

        self.screen.blit(self.pac_man_title, (750, 650))

        start = self.start_game_selected if self.selected == 0 else self.start_game
        instr = self.instructions_selected if self.selected == 1 else self.instructions
        high = self.view_highscores_selected if self.selected == 2 else self.view_highscores
        exit_btn = self.exit_button_selected if self.selected == 3 else self.exit_button

        self.screen.blit(self.arrow, (640, self.arrow_places[self.selected]))
        self.screen.blit(start, (700, 800))
        self.screen.blit(instr, (700, 900))
        self.screen.blit(high, (700, 1000))
        self.screen.blit(exit_btn, (700, 1100))

        if self.show_coin:
            self.screen.blit(self.coin, (800, 1600))

        pygame.display.flip()
