import pygame
import time
import string
from gamedata import GameData
from direction import Movement, Direction


class GamePlay:
    def __init__(self, screen: pygame.Surface, game_data: GameData):
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
        self.for_two = pygame.Surface((44, 44))
        self.pacgum = pygame.Surface((10, 10))
        self.super_pacgum = pygame.Surface((15, 15))

        self.maze = game_data.maze
        self.pacman = game_data.pacman
        self.ghost_blue = game_data.ghost_blue
        self.ghost_red = game_data.ghost_red
        self.ghost_green = game_data.ghost_green
        self.ghost_yellow = game_data.ghost_yellow
        self.pacman_name = "pacman_player"
        self.pacgums = game_data.regular_pacgums
        self.super_pacgums = game_data.super_pacgums
        self.pacman_direction = "_right"

        self.mouth_closed = False

        self.border_x.fill((0, 0, 128))
        self.border_y.fill((0, 0, 128))
        self.pacgum.fill((255, 0, 255))
        self.for_two.fill((0, 0, 255))
        self.super_pacgum.fill((43, 243, 251))

        self.last_switch = time.monotonic()
        self.last_switch_pacman = time.monotonic()

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
                if event.key == pygame.K_DOWN:
                    self.pacman.current_position = Movement.update_position_by_direction(self.pacman.current_position, Direction.DOWN)
                    self.pacman_direction = "_down"
                if event.key == pygame.K_UP:
                    self.pacman.current_position = Movement.update_position_by_direction(self.pacman.current_position, Direction.UP)
                    self.pacman_direction = "_up"
                if event.key == pygame.K_RIGHT:
                    self.pacman.current_position = Movement.update_position_by_direction(self.pacman.current_position, Direction.RIGHT)
                    self.pacman_direction = "_right"
                if event.key == pygame.K_LEFT:
                    self.pacman.current_position = Movement.update_position_by_direction(self.pacman.current_position, Direction.LEFT)
                    self.pacman_direction = "_left"
        return None

    def update(self):
        self.hearts = self.pacman.lives
        now = time.monotonic()
        if now - self.last_switch >= 1:
            self.current_title = self.title_dark if self.current_title == self.title else self.title
            self.time_count -= 1
            self.last_switch = now
        if now - self.last_switch_pacman >= 0.2:
            if self.mouth_closed:
                self.pacman_name = "pacman_player"
                self.mouth_closed = False
            else:
                self.pacman_name = "pacman_closed"
                self.mouth_closed = True
            self.last_switch_pacman = now

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
        maze = self.maze.maze
        player = self.pacman
        pacgums = self.pacgums.pacgums_positions
        super_pacgums = self.super_pacgums.get_super_pacgums_positions()
        self.pacman_player = pygame.image.load(f"UI/images/{self.pacman_name}{self.pacman_direction}.png")
        ghost_yellow = pygame.image.load("UI/images/ghost_yellow.png")
        ghost_red = pygame.image.load("UI/images/ghost_red.png")
        ghost_blue = pygame.image.load("UI/images/ghost_blue.png")
        ghost_green = pygame.image.load("UI/images/ghost_green.png")
        maze_width = len(maze[0])
        CELL_SIZE = 44
        WALL_THICKNESS = 5

        self.wall_x = pygame.Surface((CELL_SIZE, WALL_THICKNESS))
        self.wall_y = pygame.Surface((WALL_THICKNESS, CELL_SIZE))

        self.wall_x.fill((255, 255, 255))
        self.wall_y.fill((255, 255, 255))

        maze_width = len(maze[0])
        maze_pixel_size = maze_width * CELL_SIZE

        AREA_X = 70
        AREA_Y = 400
        AREA_WIDTH = 1760
        AREA_HEIGHT = 1130

        start_x = AREA_X + (AREA_WIDTH - maze_pixel_size) // 2
        start_y = AREA_Y + (AREA_HEIGHT - maze_pixel_size) // 2
        x = start_x
        y = start_y
        for row_index, row in enumerate(maze):
            for col_index, cell in enumerate(row):
                if cell & 1 and cell & 2 and cell & 4 and cell & 8:
                    self.screen.blit(self.for_two, (x, y))
                if cell & 1:
                    self.screen.blit(self.wall_x, (x, y))
                if cell & 2:
                    if col_index == len(row) - 1:
                        self.screen.blit(self.wall_y, (x + CELL_SIZE - WALL_THICKNESS, y))
                if cell & 4:
                    if row_index == len(maze) - 1:
                        self.screen.blit(self.wall_x, (x, y + CELL_SIZE - WALL_THICKNESS))
                if cell & 8:
                    self.screen.blit(self.wall_y, (x, y))
                if (row_index, col_index) in pacgums:
                    self.screen.blit(self.pacgum, ((x + 15, y + 15)))
                if (row_index, col_index) in super_pacgums:
                    self.screen.blit(self.super_pacgum, ((x + 17, y + 17)))
                x += CELL_SIZE
            x = start_x
            y += CELL_SIZE

        x_payer, y_player = player.current_position
        self.screen.blit(self.pacman_player, ((CELL_SIZE * x_payer) + start_x + WALL_THICKNESS * 2, (CELL_SIZE * y_player) + start_y + WALL_THICKNESS * 2))
        ghost_x, ghost_y = self.ghost_yellow.current_position
        self.screen.blit(ghost_yellow, ((CELL_SIZE * ghost_x) + start_x + WALL_THICKNESS * 2, (CELL_SIZE * ghost_y) + start_y + WALL_THICKNESS * 2))
        ghost_x, ghost_y = self.ghost_red.current_position
        self.screen.blit(ghost_red, ((CELL_SIZE * ghost_x) + start_x + WALL_THICKNESS * 2, (CELL_SIZE * ghost_y) + start_y + WALL_THICKNESS * 2))
        ghost_x, ghost_y = self.ghost_blue.current_position
        self.screen.blit(ghost_blue, ((CELL_SIZE * ghost_x) + start_x + WALL_THICKNESS * 2, (CELL_SIZE * ghost_y) + start_y + WALL_THICKNESS * 2))
        ghost_x, ghost_y = self.ghost_green.current_position
        self.screen.blit(ghost_green, ((CELL_SIZE * ghost_x) + start_x + WALL_THICKNESS * 2, (CELL_SIZE * ghost_y) + start_y + WALL_THICKNESS * 2))
        pygame.display.flip()

