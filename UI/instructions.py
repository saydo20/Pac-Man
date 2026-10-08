"""Instructions screen module."""

import pygame
import time


class Instructions:
    """Manages and displays the instructions screen."""

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the instructions screen, borders and images.

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

        self.line = pygame.Surface((1660, 5))
        self.last_switch = time.monotonic()

        self.title = pygame.image.load("UI/images/title.png")
        self.title_dark = pygame.image.load("UI/images/title_dark.png")

        self.current_title = self.title

        blue_color = (9, 9, 232)
        for surface in [self.border_inside_x, self.border_inside_y,
                        self.border_inside_x2, self.border_inside_y2,
                        self.border_inside_x3, self.border_inside_y3,
                        self.line]:
            surface.fill(blue_color)

        self.how_play = pygame.image.load("UI/images/how_to_play.png")
        self.rules = pygame.image.load("UI/images/rules.png")
        self.controls = pygame.image.load("UI/images/controls.png")

    def handle_events(self) -> str | None:
        """Handle window and keyboard events on the instructions screen.

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

    def update(self) -> None:
        """Toggle the title image once per second."""
        now = time.monotonic()
        if now - self.last_switch >= 1:
            self.current_title = self.title_dark if (
                self.current_title == self.title) else self.title
            self.last_switch = now

    def draw(self) -> None:
        """Draw the borders, title and instruction images,
        then flip display."""
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

        self.screen.blit(self.how_play, (700, 370))
        self.screen.blit(self.controls, (200, 600))
        self.screen.blit(self.rules, (1000, 600))

        pygame.display.flip()
        return None
