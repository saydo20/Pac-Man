import pygame
import time
import string


class GamePlay:
    def __init__(self, screen: pygame.Surface):
        self.score = 0
        self.hearts = 3
        self.level_count = 2
        self.time_count = 90
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


        self.last_switch = time.monotonic()

        self.title = pygame.image.load("UI/images/title.png")
        self.title_dark = pygame.image.load("UI/images/title_dark.png")
        self.score_text = pygame.image.load("UI/images/SCORE.png")
        self.level = pygame.image.load("UI/images/LEVEL.png")
        self.lives = pygame.image.load("UI/images/LIVES.png")
        self.time = pygame.image.load("UI/images/TIME.png")
        self.heart = pygame.image.load("UI/images/heart.png")

        self.current_title = self.title

        blue_color = (9, 9, 232)
        for surface in [self.border_inside_x, self.border_inside_y,
                        self.border_inside_x2, self.border_inside_y2,
                        self.border_inside_x3, self.border_inside_y3]:
            surface.fill(blue_color)
        self.images = {}
        for char in string.ascii_uppercase + string.digits:
            self.images[char] = pygame.image.load(f"UI/images/{char}.png")
        self.images["_"] = pygame.image.load("UI/images/_.png")
        self.images["."] = pygame.image.load("UI/images/dot.png")
        self.images[":"] = pygame.image.load("UI/images/:.png")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "quit"
        return None

    def update(self):
        now = time.monotonic()
        if now - self.last_switch >= 1:
            self.current_title = self.title_dark if self.current_title == self.title else self.title
            self.time_count -= 1
            self.last_switch = now

    def draw_text(self, text: str, x, y, max_size):
        for char in text:
            if char == " ":
                x += 10
                continue
            if x >= max_size - 32:
                self.screen.blit(self.images["."], (x, y))
                self.screen.blit(self.images["."], (x + 15, y))
                self.screen.blit(self.images["."], (x + 30, y))
                break
            image = self.images[char.upper() if char.isalpha() else char]
            self.screen.blit(image, (x, y))
            x += 32

    def draw(self, maze):
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

        self.screen.blit(self.border_inside_x3, (70, 400))

        self.screen.blit(self.score_text, (300, 290))
        self.screen.blit(self.lives, (700, 290))
        self.screen.blit(self.level, (1100, 290))
        self.screen.blit(self.time, (1500, 290))

        self.draw_text(f"{self.score:06d}", 290, 350, 4000)
        x = 680
        for i in range(self.hearts):
            self.screen.blit(self.heart, (x, 350))
            x += 60
        self.draw_text(f"{self.level_count:02d}", 1140, 350, 1400)
        self.draw_text(f"{self.time_count}", 1530, 350, 1800)
#########################################################################
        maze_width = len(maze[1])
        MAX_MAZE_SIZE = 1080
        CELL_SIZE = MAX_MAZE_SIZE // maze_width
        WALL_THICKNESS = max(1, CELL_SIZE // 5)

        self.wall_x = pygame.Surface((CELL_SIZE, WALL_THICKNESS))
        self.wall_y = pygame.Surface((WALL_THICKNESS, CELL_SIZE))

        self.wall_x.fill((255, 255, 255))
        self.wall_y.fill((255, 255, 255))

        maze_pixel_size = maze_width * CELL_SIZE

        AREA_X = 70
        AREA_Y = 400
        AREA_WIDTH = 1760
        AREA_HEIGHT = 1130

        start_x = AREA_X + (AREA_WIDTH - maze_pixel_size) // 2
        start_y = AREA_Y + (AREA_HEIGHT - maze_pixel_size) // 2
        x = start_x
        y = start_y
        for line in maze:
            for cell in line:
                if cell & 1:
                    self.screen.blit(self.wall_x, (x, y))
                if cell & 2:
                    self.screen.blit(self.wall_y, (x + CELL_SIZE - WALL_THICKNESS, y))
                if cell & 4:
                    self.screen.blit(self.wall_x, (x, y + CELL_SIZE - WALL_THICKNESS))
                if cell & 8:
                    self.screen.blit(self.wall_y, (x, y))
                x += CELL_SIZE
            x = start_x
            y += CELL_SIZE
        pygame.display.flip()

