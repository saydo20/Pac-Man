"""Highscores screen module for Pac-Man."""

import pygame
import time
from src.score import Score
import string


class Highscores:
    """Manages and displays the high scores screen."""

    def __init__(self, screen: pygame.Surface):
        """Initialize the highscores screen.

        Args:
            screen: Pygame display surface.
        """
        self.screen = screen
        self.border_x = pygame.Surface((1900, 10))
        self.border_y = pygame.Surface((10, 1730))
        self.border_inside_x = pygame.Surface((1860, 15))
        self.border_inside_y = pygame.Surface((15, 1690))
        self.border_inside_x2 = pygame.Surface((1800, 10))
        self.border_inside_y2 = pygame.Surface((10, 1300))
        self.border_inside_x3 = pygame.Surface((1760, 10))
        self.border_inside_y3 = pygame.Surface((10, 1260))
        self.scores: list = []

        self.line = pygame.Surface((1660, 5))
        self.last_switch = time.monotonic()

        self.title = pygame.image.load("UI/images/title.png")
        self.title_dark = pygame.image.load("UI/images/title_dark.png")

        self.border_x.fill((0, 0, 128))
        self.border_y.fill((0, 0, 128))

        blue_color = (9, 9, 232)
        for surface in [self.border_inside_x, self.border_inside_y,
                        self.border_inside_x2, self.border_inside_y2,
                        self.border_inside_x3, self.border_inside_y3,
                        self.line]:
            surface.fill(blue_color)

        self.title = pygame.image.load("UI/images/title.png")
        self.title_dark = pygame.image.load("UI/images/title_dark.png")
        self.pac_man_title = pygame.image.load("UI/images/pacman.png")
        self.player_name = pygame.image.load("UI/images/name.png")
        self.rank = pygame.image.load("UI/images/rank.png")
        self.score_field = pygame.image.load("UI/images/score_field.png")
        self.top_scores = pygame.image.load("UI/images/top_scores.png")
        self.current_title = self.title
        self.images = {}
        for char in string.ascii_uppercase + string.digits:
            self.images[char] = pygame.image.load(f"UI/images/{char}.png")
        self.images["_"] = pygame.image.load("UI/images/_.png")
        self.images["."] = pygame.image.load("UI/images/dot.png")
        self.images[":"] = pygame.image.load("UI/images/:.png")

    def draw_text(self, text: str, x: int, y: int, max_size: int) -> None:
        """Render text character by character on the screen.

        Args:
            text: Text string to render.
            x: Starting x-coordinate.
            y: Starting y-coordinate.
            max_size: Maximum horizontal pixel boundary.
        """
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

    def handle_events(self) -> str | None:
        """Handle window and keyboard events on the highscores screen.

        Returns:
            'quit' on window close, 'menu' on Escape, or None.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
        return None

    def update(self, score: Score) -> None:
        """Toggle the title image and load the latest scores.

        Args:
            score: Score object that provides the high score list.
        """
        now = time.monotonic()
        if now - self.last_switch >= 1:
            self.current_title = self.title_dark if (
                self.current_title == self.title) else self.title
            self.last_switch = now
        self.scores = score.get_scores

    def draw(self) -> None:
        """Draw the borders, title, column headers and score rows."""
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

        self.screen.blit(self.top_scores, (660, 370))

        self.screen.blit(self.rank, ((180, 450)))
        self.screen.blit(self.player_name, ((400, 450)))
        self.screen.blit(self.score_field, ((1660, 450)))

        self.screen.blit(self.line, (115, 480))

        y = 500
        for score in self.scores:
            self.draw_text(f"{score['rank']}", 200, y, 5000)
            self.draw_text(f"{score['Player']}", 400, y, 5000)
            self.draw_text(f"{score['score']}", 1650, y, 5000)
            self.screen.blit(self.line, (115, y + 60))
            y += 80

        pygame.display.flip()
        return None
