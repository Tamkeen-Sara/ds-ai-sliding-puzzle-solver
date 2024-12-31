#sprites.py
import pygame
from settings import *

pygame.font.init()

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x, self.y = x, y
        # Create a slightly larger surface for 3D effect
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.text = text
        self.rect = self.image.get_rect()

        if self.text != "empty":
            # Create 3D effect
            # Bottom layer (shadow)
            pygame.draw.rect(self.image, SHADOW,
                             (TILE_PADDING, TILE_PADDING,
                              TILESIZE - TILE_PADDING * 2, TILESIZE - TILE_PADDING * 2),
                             border_radius=10)

            # Top layer (main tile)
            pygame.draw.rect(self.image, WHITE,
                             (0, 0,
                              TILESIZE - TILE_PADDING, TILESIZE - TILE_PADDING),
                             border_radius=10)

            # Border
            pygame.draw.rect(self.image, ACCENT,
                             (0, 0,
                              TILESIZE - TILE_PADDING, TILESIZE - TILE_PADDING),
                             3, border_radius=10)

            # Add text
            self.font = pygame.font.SysFont("Arial", 50)
            font_surface = self.font.render(self.text, True, BLACK)
            font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - font_size[0] / 2 - TILE_PADDING / 2
            draw_y = (TILESIZE / 2) - font_size[1] / 2 - TILE_PADDING / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(BGCOLOUR)


    # Updates the position of the tile based on its x and y coordinates.
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


    # Checks if the mouse click occurs within the bounds of the tile.
    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom


    # Checks if the tile can move right (if it doesn't go beyond the game boundary).
    def right(self):
        return self.rect.x + TILESIZE < self.game.game_size * TILESIZE


    # Checks if the tile can move left (if it doesn't go beyond the left boundary).
    def left(self):
        return self.rect.x - TILESIZE >= 0


    # Checks if the tile can move up (if it doesn't go beyond the top boundary).
    def up(self):
        return self.rect.y - TILESIZE >= 0


    # Checks if the tile can move down (if it doesn't go beyond the bottom boundary).
    def down(self):
        return self.rect.y + TILESIZE < self.game.game_size * TILESIZE


class Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text, width, height):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.text = text

        # Enhanced button appearance
        self.font = pygame.font.SysFont("Arial", 30)
        self.image.fill(BLUE)
        pygame.draw.rect(self.image, ACCENT, self.rect, 2, border_radius=5)

        font_surface = self.font.render(self.text, True, WHITE)
        font_size = self.font.size(self.text)
        draw_x = (width / 2) - font_size[0] / 2
        draw_y = (height / 2) - font_size[1] / 2
        self.image.blit(font_surface, (draw_x, draw_y))


    # Updates the position of the button based on its x and y coordinates.
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y


    # Checks if the mouse click occurs within the bounds of the button.
    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom


# Defines the position and text for the UI element.
class UIElement:

    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    # Draws the UI element's text on the screen at the specified font size.
    def draw(self, screen, font_size):
        font = pygame.font.SysFont("Consolas", font_size)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))