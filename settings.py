# settings.py
# this file defines all the settings and parameters to be used in GAME

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (44, 62, 80)
LIGHTGREY = (149, 165, 166)
GREEN = (46, 204, 113)
BLUE = (41, 128, 185)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
BGCOLOUR = DARKGREY
ACCENT = (52, 152, 219)
SHADOW = (34, 49, 63)  # Coloring for 3D effect

# Base tile size and padding
WIDTH = 1100
HEIGHT = 641
FPS = 60
title = "The Sliding Puzzle Game and Solver"
TILESIZE = 128
TILE_PADDING = 4
BUTTON_PANEL_WIDTH = 500   # Fixed width for button panel

# Dynamic window sizing
BASE_HEIGHT = 641
MIN_WIDTH = 1100

# Grid sizes
Very_EASY = 2 * TILESIZE
EASY = 3 * TILESIZE
MEDIUM = 4 * TILESIZE
HARD = 5 * TILESIZE