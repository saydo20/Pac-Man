import pygame
import time
import string

from src.gamedata import GameData, Direction
from src.enums_helper import Mode
from src.pacman import Pacman
from src.ghost import Ghost


class Adapter():
    def __init__(self, maze_width: int):
        self.CELL_SIZE = 70
        self.WALL_THICKNESS = 5
        AREA_X = 70
        AREA_Y = 400
        AREA_WIDTH = 1760
        AREA_HEIGHT = 1130

        self.maze_pixel_size = maze_width * self.CELL_SIZE

        self.start_x = AREA_X + (AREA_WIDTH - self.maze_pixel_size) // 2
        self.start_y = AREA_Y + (AREA_HEIGHT - self.maze_pixel_size) // 2


class Player:
    def __init__(self, pacman: Pacman, adapter: Adapter):
        self.adpater = adapter
        self.pacman = pacman
        self.current_position = pacman.current_position
        self.lives = pacman.lives
        self.score = pacman.score
        self.pacman_possition = (0, 0)
        self.pacman_mode = Mode.FLEE.name.lower()
        self.pacman_name = "pacman_player"
        self.pacman_direction = "_right"
        self.requested_direction = Direction.RIGHT
        self.pacman_prev_position = self.pacman.current_position
        self.pexel_posstion = (0, 0)
        self.mode = pacman.mode
        self.mouth_closed = False

    def move_player(self, last_move_time):
        now = time.monotonic()
        t = min((now - last_move_time) / 0.2, 1.0)

        prev_x, prev_y = self.pacman_prev_position
        curr_x, curr_y = self.current_position

        interp_x = prev_x + (curr_x - prev_x) * t
        interp_y = prev_y + (curr_y - prev_y) * t

        pixel_x = (int(70 * interp_x) + self.adpater.start_x +
                   self.adpater.WALL_THICKNESS * 2)
        pixel_y = (int(70 * interp_y) + self.adpater.start_y +
                   self.adpater.WALL_THICKNESS * 2)

        self.pexel_posstion = (pixel_x, pixel_y)

    def reset_to_spawn(self):
        self.pacman.start_position()
        self.current_position = self.pacman.current_position
        self.pacman_prev_position = self.current_position
        self.move_player(time.monotonic())


class Ghost_G:
    def __init__(self, ghost: Ghost, adapter: Adapter):
        self.adapter = adapter
        self.ghost = ghost
        self.current_position = ghost.current_position
        self.prev_position = ghost.current_position
        self.mode = ghost.mode
        self.pexel_posstion = (0, 0)
        self.last_step_time = time.monotonic()
        self.time_of_death = 0.0
        self.is_dead = False

    def die(self, now: float):
        self.is_dead = True
        self.time_of_death = now
        self.reset_to_spawn()

    def update_death_state(self, now: float):
        if self.is_dead and (now - self.time_of_death >= 2):
            self.is_dead = False

    def step_ghost(self, pacman_position: tuple):
        self.prev_position = self.current_position
        self.ghost.move_ghost(pacman_position)
        self.current_position = self.ghost.current_position
        self.last_step_time = time.monotonic()

    def update_pixel_position(self):
        now = time.monotonic()
        t = min((now - self.last_step_time) / 0.5, 1.0)

        prev_x, prev_y = self.prev_position
        curr_x, curr_y = self.current_position

        interp_x = prev_x + (curr_x - prev_x) * t
        interp_y = prev_y + (curr_y - prev_y) * t

        pixel_x = (int(70 * interp_x) + self.adapter.start_x +
                   self.adapter.WALL_THICKNESS * 2)
        pixel_y = (int(70 * interp_y) + self.adapter.start_y +
                   self.adapter.WALL_THICKNESS * 2)

        self.pexel_posstion = (pixel_x, pixel_y)

    def reset_to_spawn(self):
        self.ghost.set_start_position()
        self.current_position = self.ghost.current_position
        self.prev_position = self.current_position
        self.last_step_time = time.monotonic()
        self.update_pixel_position()


class GamePlay:
    def __init__(self, screen: pygame.Surface, game_data: GameData):
        self.adapter = Adapter(len(game_data.maze.maze[0]))
        self.pacman = Player(game_data.pacman, self.adapter)
        self.screen = screen
        self.border_x = pygame.Surface((1900, 10))
        self.border_y = pygame.Surface((10, 1730))
        self.border_inside_x = pygame.Surface((1860, 15))
        self.border_inside_y = pygame.Surface((15, 1690))
        self.border_inside_x2 = pygame.Surface((1800, 10))
        self.border_inside_y2 = pygame.Surface((10, 1300))
        self.border_inside_x3 = pygame.Surface((1760, 10))
        self.border_inside_y3 = pygame.Surface((10, 1260))
        self.for_two = pygame.Surface((70, 70))
        self.pacgum = pygame.Surface((10, 10))
        self.super_pacgum = pygame.Surface((15, 15))

        self.game_data = game_data
        self.maze = self.game_data.maze

        self.ghost_blue = Ghost_G(game_data.ghost_blue, self.adapter)
        self.ghost_red = Ghost_G(game_data.ghost_red, self.adapter)
        self.ghost_green = Ghost_G(game_data.ghost_green, self.adapter)
        self.ghost_yellow = Ghost_G(game_data.ghost_yellow, self.adapter)
        self.ghosts = [self.ghost_blue, self.ghost_green, self.ghost_red,
                       self.ghost_yellow]

        self.pacgums = self.game_data.regular_pacgums
        self.super_pacgums = self.game_data.super_pacgums

        self.score = self.pacman.pacman.score
        self.hearts = self.pacman.pacman.lives

        self.border_x.fill((0, 0, 128))
        self.border_y.fill((0, 0, 128))
        self.pacgum.fill((255, 0, 255))
        self.for_two.fill((0, 0, 255))
        self.super_pacgum.fill((43, 243, 251))

        self.last_switch = time.monotonic()
        self.time_of_death = 0.0
        self.attack = float('inf')
        self.last_switch_pacman = time.monotonic()
        self.last_move_time = time.monotonic()
        self.player_death = False

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
                if event.key == pygame.K_p:
                    return "pause"
                if event.key == pygame.K_q:
                    return "menu"
                if not self.player_death:
                    if event.key == pygame.K_DOWN:
                        self.pacman.requested_direction = Direction.DOWN
                        self.pacman.pacman_direction = "_down"
                    if event.key == pygame.K_UP:
                        self.pacman.requested_direction = Direction.UP
                        self.pacman.pacman_direction = "_up"
                    if event.key == pygame.K_RIGHT:
                        self.pacman.requested_direction = Direction.RIGHT
                        self.pacman.pacman_direction = "_right"
                    if event.key == pygame.K_LEFT:
                        self.pacman.requested_direction = Direction.LEFT
                        self.pacman.pacman_direction = "_left"

        self.hearts = self.pacman.lives
        self.score = self.pacman.score
        return None

    def update(self):
        self.pacman.score = self.pacman.pacman.score
        now = time.monotonic()
        for ghost in self.ghosts:
            ghost.update_death_state(now)
        if self.player_death:
            if now - self.time_of_death < 2.0:
                return
            else:
                self.player_death = False
                self.last_move_time = now
                self.last_switch_pacman = now
                self.last_switch = now
                for ghost in self.ghosts:
                    ghost.last_step_time = now

        self.pacman.move_player(self.last_move_time)
        for ghost in self.ghosts:
            ghost.update_pixel_position()

        self.hearts = self.pacman.lives
        if now - self.last_move_time >= 0.2:
            self.pacman.pacman_prev_position = self.pacman.current_position
            self.pacman.current_position = self.game_data.update_pos_by_dirc(
                self.pacman.current_position, self.pacman.requested_direction
            )
            self.last_move_time = now

        if now - self.last_switch >= 1:
            self.current_title = self.title_dark if (
                self.current_title == self.title) else self.title
            self.game_data.time_count -= 1
            self.last_switch = now

        if now - self.last_switch_pacman >= 0.5:
            if self.pacman.mouth_closed:
                self.pacman.pacman_name = "pacman_player"
                self.pacman.mouth_closed = False
            else:
                self.pacman.pacman_name = "pacman_closed"
                self.pacman.mouth_closed = True
            for ghost in self.ghosts:
                ghost.step_ghost(self.pacman.current_position)
            self.last_switch_pacman = now

        x_player, y_player = self.pacman.pexel_posstion
        for ghost in self.ghosts:
            x_ghost, y_ghost = ghost.pexel_posstion
            if (x_ghost - x_player)**2 + (y_ghost - y_player)**2 <= 10**2:
                if self.pacman.mode == Mode.FLEE:
                    self.time_of_death = now
                    self.player_death = True
                    self.pacman.lives -= 1
                    self.pacman.pacman.lives -= 1
                    self.hearts = self.pacman.lives
                    self.pacman.reset_to_spawn()
                    for g in self.ghosts:
                        g.reset_to_spawn()
                    if self.pacman.lives == 0:
                        return "game_over"
                    break
                elif self.pacman.mode == Mode.ATTACK:
                    if not ghost.is_dead:
                        ghost.die(now)
        if all(value == 0 for row in self.pacgums.pacgums_grid
               for value in row):
            self.game_data.generate_next_level()

        if (self.game_data.pacman.mode == Mode.ATTACK and
                self.pacman.pacman_mode == "flee"):
            self.attack = time.monotonic()
        if now - self.attack >= 200:
            self.game_data.change_mode_player_ghosts(Mode.FLEE, Mode.ATTACK)
        self.pacman.mode = self.game_data.pacman.mode
        self.pacman.pacman_mode = self.game_data.pacman.mode.name.lower()

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
        self.draw_text(f"{self.game_data.nb_level:02d}", 1140, 350, 1400)
        self.draw_text(f"{self.game_data.time_count}", 1530, 350, 1800)

        maze = self.maze.maze
        pacgums = self.pacgums.pacgums_grid
        self.pacman_player = pygame.image.load(
            f"UI/images/{self.pacman.pacman_name}"
            f"{self.pacman.pacman_direction}_"
            f"{self.pacman.pacman_mode}.png"
        )
        ghost_yellow = pygame.image.load("UI/images/ghost_yellow.png")
        ghost_red = pygame.image.load("UI/images/ghost_red.png")
        ghost_blue = pygame.image.load("UI/images/ghost_blue.png")
        ghost_green = pygame.image.load("UI/images/ghost_green.png")
        ghost_dead = pygame.image.load("UI/images/ghost_dead.png")

        self.wall_x = pygame.Surface(
            (self.adapter.CELL_SIZE, self.adapter.WALL_THICKNESS))
        self.wall_y = pygame.Surface(
            (self.adapter.WALL_THICKNESS, self.adapter.CELL_SIZE))

        self.wall_x.fill((255, 255, 255))
        self.wall_y.fill((255, 255, 255))

        x = self.adapter.start_x
        y = self.adapter.start_y
        for row_index, row in enumerate(maze):
            for col_index, cell in enumerate(row):
                if cell & 1 and cell & 2 and cell & 4 and cell & 8:
                    self.screen.blit(self.for_two, (x, y))
                if cell & 1:
                    self.screen.blit(self.wall_x, (x, y))
                if cell & 2:
                    if col_index == len(row) - 1:
                        self.screen.blit(self.wall_y,
                                         ((x + self.adapter.CELL_SIZE -
                                           self.adapter.WALL_THICKNESS), y))
                if cell & 4:
                    if row_index == len(maze) - 1:
                        self.screen.blit(self.wall_x,
                                         (x, (y + self.adapter.CELL_SIZE -
                                              self.adapter.WALL_THICKNESS)))
                if cell & 8:
                    self.screen.blit(self.wall_y, (x, y))
                if pacgums[row_index][col_index]:
                    self.screen.blit(self.pacgum, (x + 30, y + 30))
                if (col_index, row_index) in self.super_pacgums.positions:
                    self.screen.blit(self.super_pacgum, (x + 17, y + 17))
                x += self.adapter.CELL_SIZE
            x = self.adapter.start_x
            y += self.adapter.CELL_SIZE

        self.screen.blit(self.pacman_player, self.pacman.pexel_posstion)
        yellow = ghost_dead if self.ghost_yellow.is_dead else ghost_yellow
        red = ghost_dead if self.ghost_red.is_dead else ghost_red
        blue = ghost_dead if self.ghost_blue.is_dead else ghost_blue
        green = ghost_dead if self.ghost_green.is_dead else ghost_green

        self.screen.blit(yellow, self.ghost_yellow.pexel_posstion)
        self.screen.blit(red, self.ghost_red.pexel_posstion)
        self.screen.blit(blue, self.ghost_blue.pexel_posstion)
        self.screen.blit(green, self.ghost_green.pexel_posstion)

        pygame.display.flip()
