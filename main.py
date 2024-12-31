# main.py
# file to play game
# This is Project of Artificial Intelligence , basically a game " Sliding Puzzle Solver "

import time
import pygame
import random
import heapq
from sprites import *
from settings import *

# game class to handle functionality of the game
class Game:
    def __init__(self):
        pygame.init()
        self.game_size = 3  # Default size
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(400, 100)

        # Initializing sprite group early
        self.all_sprites = pygame.sprite.Group()

        # Initializing other game state variables
        self.start_shuffle = False
        self.shuffle_time = 0
        self.previous_choice = ""
        self.choice = ""
        self.start_timer = False
        self.start_game = False
        self.display_congrats = False
        self.congrats_timer = 0
        self.elapsed_time = 0
        self.tiles = []

        # Initializing high scores
        self.high_score_very_easy = float(self.get_high_scores()[0])
        self.high_score_easy = float(self.get_high_scores()[1])
        self.high_score_medium = float(self.get_high_scores()[2])
        self.high_score_hard = float(self.get_high_scores()[3])

    #function to return high score
    @staticmethod
    def get_high_scores():
        """Read high scores from file."""
        with open("high_scores.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    # function to create game grid
    @staticmethod
    def create_game(game_size):
        grid = [[x + y * game_size for x in range(1, game_size + 1)] for y in range(game_size)]
        grid[-1][-1] = 0
        return grid

    # function to shuffle the tiles
    def shuffle(self):
        possible_moves = []
        # Iterates over the tiles to find possible moves for the empty tile.
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    # Determines valid moves based on the position of the empty tile.
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        # Removes invalid moves based on the previous choice to avoid backtracking.
        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        # Selects a random valid move for the empty tile.
        self.choice = random.choice(possible_moves)
        self.previous_choice = self.choice
        # Swaps the tiles based on the chosen move.
        if self.choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                self.tiles_grid[row][col]
        elif self.choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                self.tiles_grid[row][col]
        elif self.choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                self.tiles_grid[row][col]
        elif self.choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                self.tiles_grid[row][col]


    # function to move in a specific direction
    def make_move(self, row, col, direction):
        if direction == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = \
                self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
        elif direction == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = \
                self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
        elif direction == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = \
                self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
        elif direction == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = \
                self.tiles_grid[row + 1][col], self.tiles_grid[row][col]


    # function to calculate required width based on game size
    def update_window_size(self):
        game_width = self.game_size * TILESIZE
        window_width = max(MIN_WIDTH, game_width + BUTTON_PANEL_WIDTH)
        window_height = max(BASE_HEIGHT, game_width + 50)  # Add padding
        self.screen = pygame.display.set_mode((window_width, window_height))


    # function to save high scores to the files
    def save_score(self):
        with open("high_scores.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score_very_easy))
            file.write(str("%.3f\n" % self.high_score_easy))
            file.write(str("%.3f\n" % self.high_score_medium))
            file.write(str("%.3f" % self.high_score_hard))


    # Function to initialize the game grid and completed grid for the new game.
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game(self.game_size)
        self.tiles_grid_completed = self.create_game(self.game_size)
        self.elapsed_time = 0
        self.moves = 0
        self.start_timer = False
        self.start_game = False
        # Draws buttons and tiles for the new game.
        self.draw_buttons()
        self.draw_tiles()

    # function to draws the timer on the screen.
    def draw_timer(self, timer):
        UIElement(825, 35, timer).draw(self.screen, 40)

    # function to draws the high score on the screen.
    def draw_high_score(self, score):
        UIElement(710, 380, score).draw(self.screen, 30)


    # function to draw the buttons on the screen.
    def draw_buttons(self):
        board_width = self.game_size * TILESIZE
        start_x = board_width + 50  # Padding from the board

        self.buttons_list = []
        # Arrange buttons vertically with proper spacing
        self.buttons_list.append(Button(self, start_x, 100, "Shuffle", 200, 50))
        self.buttons_list.append(Button(self, start_x, 170, "Reset", 200, 50))

        # Difficulty buttons in a grid
        diff_y = 240
        diff_x = start_x
        self.buttons_list.append(Button(self, diff_x, diff_y, "Very Easy", 170, 50))
        self.buttons_list.append(Button(self, diff_x + 190, diff_y, "Easy", 100, 50))
        self.buttons_list.append(Button(self, diff_x, diff_y + 70, "Medium", 150, 50))
        self.buttons_list.append(Button(self, diff_x + 190, diff_y + 70, "Hard", 100, 50))

        # Solve button at the bottom
        self.buttons_list.append(Button(self, diff_x, diff_y + 200, "Solve it for me!", 290, 50))

    # function to draws the tiles on the screen.
    def draw_tiles(self):
        self.tiles = []
        # Iterates over the grid and creates tile objects.
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))


    # Main game loop that keeps the game Running.
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # function to QUIT Game
    def quit(self):
        pygame.quit()


    def update(self):
        if self.start_game:
            # Checks if the player has completed the puzzle and updates the score.
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                self.display_congrats = True
                print("Congratulations! The puzzle is solved successfully")
                if self.game_choice == Very_EASY:
                    if self.high_score_very_easy > 0:
                        self.high_score_very_easy = self.elapsed_time if self.elapsed_time < self.high_score_very_easy else self.high_score_very_easy
                    else:
                        self.high_score_easy = self.elapsed_time
                elif self.game_choice == EASY:
                    if self.high_score_easy > 0:
                        self.high_score_easy = self.elapsed_time if self.elapsed_time < self.high_score_easy else self.high_score_easy
                    else:
                        self.high_score_easy = self.elapsed_time
                elif self.game_choice == MEDIUM:
                    if self.high_score_medium > 0:
                        self.high_score_medium = self.elapsed_time if self.elapsed_time < self.high_score_medium else self.high_score_medium
                    else:
                        self.high_score_medium = self.elapsed_time
                elif self.game_choice == HARD:
                    if self.high_score_hard > 0:
                        self.high_score_hard = self.elapsed_time if self.elapsed_time < self.high_score_hard else self.high_score_hard
                    else:
                        self.high_score_hard = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            # Shuffles the grid and redraws the tiles.
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 100:
                self.start_shuffle = False
                self.start_timer = True
                self.start_game = True

        # Add processing for solution steps.
        if hasattr(self, 'solution_steps') and self.solution_index < len(self.solution_steps):
            self.process_solution_step()
            pygame.time.delay(200)

        if self.display_congrats:
            if self.congrats_timer == 0:
                self.congrats_timer = time.time()
            elif time.time() - self.congrats_timer > 3:  # 3 seconds
                self.display_congrats = False
                self.congrats_timer = 0
        self.all_sprites.update()


    def draw_grid(self):
        # Enhanced 3D grid
        for row in range(self.game_size + 1):
            # Horizontal lines with shadow
            y = row * TILESIZE
            pygame.draw.line(self.screen, SHADOW, (0, y + 2), (self.game_size * TILESIZE, y + 2), 3)
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (self.game_size * TILESIZE, y), 2)

        for col in range(self.game_size + 1):
            # Vertical lines with shadow
            x = col * TILESIZE
            pygame.draw.line(self.screen, SHADOW, (x + 2, 0), (x + 2, self.game_size * TILESIZE), 3)
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, self.game_size * TILESIZE), 2)


    def draw(self):
        # Fills the screen with the background color and draws all sprites.
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        if self.display_congrats:
            UIElement(150, 550, "Congratulations! The puzzle is solved successfully").draw(self.screen, 30)
        if self.game_choice == Very_EASY:
            UIElement(730, 320, "Level: Very Easy").draw(self.screen, 30)
            self.draw_high_score("High Score - %.3f" % (self.high_score_very_easy if self.high_score_very_easy > 0 else 0))
        elif self.game_choice == EASY:
            UIElement(800, 320, "Level: Easy").draw(self.screen, 30)
            self.draw_high_score("High Score - %.3f" % (self.high_score_easy if self.high_score_easy > 0 else 0))
        elif self.game_choice == MEDIUM:
            UIElement(870, 320, "Level: Medium").draw(self.screen, 28)
            self.draw_high_score("High Score - %.3f" % (self.high_score_medium if self.high_score_medium > 0 else 0))
        elif self.game_choice == HARD:
            UIElement(985, 325, "Level: Hard").draw(self.screen, 18)
            self.draw_high_score("High Score - %.3f" % (self.high_score_hard if self.high_score_hard > 0 else 0))
        self.draw_timer("%.3f" % self.elapsed_time)
        pygame.display.flip()


    #function to implement A* algorithm to solve the puzzle
    def solve_for_me(self):
        initial_state = self.tiles_grid
        goal_state = self.get_goal_state()

        if self.is_solved(initial_state, goal_state):
            return

        open_list = []
        closed_list = set()
        came_from = {}

        initial_node = self.create_node(initial_state, 0, self.manhattan_distance(initial_state), None)
        heapq.heappush(open_list, initial_node)

        while open_list:
            current_node = heapq.heappop(open_list)
            current_state = current_node[2]

            if self.is_solved(current_state, goal_state):
                self.reconstruct_solution(came_from, current_node)
                return

            closed_list.add(self.state_to_tuple(current_state))

            for next_state, action in self.get_neighbors(current_state):
                if self.state_to_tuple(next_state) in closed_list:
                    continue

                cost = current_node[1] + 1
                heuristic = self.manhattan_distance(next_state)
                f = cost + heuristic

                next_node = self.create_node(next_state, cost, heuristic, current_node)
                heapq.heappush(open_list, next_node)
                came_from[self.state_to_tuple(next_state)] = current_node

        print("No Solution Found.")


    # Creates a node for the A* algorithm.
    def create_node(self, state, g, h, parent_node):
        return (g + h, g, state, parent_node)


    # Generates the goal state for the puzzle.
    def get_goal_state(self):
        size = self.game_size
        goal = [list(range(i * size + 1, (i + 1) * size + 1)) for i in range(size)]
        goal[size - 1][size - 1] = 0
        return goal

    # function to check if puzzle is solved or not , checks if the current state matches the goal state.
    def is_solved(self, state, goal):
        return state == goal


    def get_neighbors(self, state):
        # Gets all possible neighbor states based on the empty tile's position.
        size = self.game_size
        neighbors = []
        empty_pos = self.find_empty_tile(state)
        row, col = empty_pos

        possible_moves = [
            (row-1, col),
            (row+1, col),
            (row, col-1),
            (row, col+1)
        ]

        for r, c in possible_moves:
            if 0 <= r < size and 0 <= c < size:
                new_state = self.make_move(state, (row, col), (r, c))
                neighbors.append((new_state, (r, c)))

        return neighbors


    def find_empty_tile(self, state):
        # Finds the position of the empty tile in the state.
        for r in range(self.game_size):
            for c in range(self.game_size):
                if state[r][c] == 0:
                    return (r, c)


    def make_move(self, state, empty_pos, new_pos):
        # Makes a move by swapping tiles in the state.
        r1, c1 = empty_pos
        r2, c2 = new_pos
        new_state = [row[:] for row in state]
        new_state[r1][c1], new_state[r2][c2] = new_state[r2][c2], new_state[r1][c1]
        return new_state

    def linear_conflict(self, state):
        size = self.game_size
        linear_conflicts = 0

        for row in range(size):
            max_conflict = -1
            for col in range(size):
                tile = state[row][col]
                if tile == 0:
                    continue
                target_row = (tile - 1) // size
                target_col = (tile - 1) % size

                # Check if the tile is in the same row as its goal position
                if target_row == row:
                    for k in range(col + 1, size):  # Check tiles which are on the right
                        other_tile = state[row][k]
                        if other_tile == 0:
                            continue
                        other_target_row = (other_tile - 1) // size
                        other_target_col = (other_tile - 1) % size
                        if other_target_row == row and other_target_col < target_col:
                            linear_conflicts += 1

                # Check if the tile is in the same column as its goal position
                if target_col == col:
                    for k in range(row + 1, size):  # Check tiles in the rows below
                        other_tile = state[k][col]
                        if other_tile == 0:
                            continue
                        other_target_row = (other_tile - 1) // size
                        other_target_col = (other_tile - 1) % size
                        if other_target_col == col and other_target_row < target_row:
                            linear_conflicts += 1

        return 2 * linear_conflicts  # Each conflict adds 2 to the cost

    def manhattan_distance(self, state):
        # Calculates the Manhattan distance heuristic for A*.
        size = self.game_size
        dist = 0
        for r in range(size):
            for c in range(size):
                value = state[r][c]
                if value != 0:
                    target_row = (value - 1) // size
                    target_col = (value - 1) % size
                    dist += abs(target_row - r) + abs(target_col - c)
        return dist + self.linear_conflict(state)


    # Converts the state to a tuple for comparison and storing in sets.
    def state_to_tuple(self, state):
        return tuple(tuple(row) for row in state)


    # Reconstructs the solution path.
    def reconstruct_solution(self, came_from, current_node):
        path = []
        while current_node:
            path.append(current_node[2])
            current_node = current_node[3]
        path.reverse()

        # Store the path for step-by-step visualization.
        self.solution_steps = path[1:]
        self.solution_index = 0


    # Add this method to process and display each move step-by-step.
    def process_solution_step(self):
        if self.solution_index < len(self.solution_steps):
            state = self.solution_steps[self.solution_index]
            self.apply_move(state)
            self.draw_tiles()
            self.all_sprites.update()
            pygame.display.flip()
            self.solution_index += 1


    # Applies a new state to the game grid.
    def apply_move(self, new_state):
        self.tiles_grid = new_state


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            # Handles tile movement based on user input.
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][
                                                                                               col + 1], \
                                                                                           self.tiles_grid[row][col]

                            elif tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][
                                                                                               col - 1], \
                                                                                           self.tiles_grid[row][col]

                            elif tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][
                                                                                               col], \
                                                                                           self.tiles_grid[row][col]

                            elif tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][
                                                                                               col], \
                                                                                           self.tiles_grid[row][col]
                            self.draw_tiles()
                            self.moves += 1

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Very Easy":
                            self.game_choice = Very_EASY
                            self.game_size = 2
                            self.new()
                        elif button.text == "Easy":
                            self.game_choice = EASY
                            self.game_size = 3
                            self.new()
                        elif button.text == "Medium":
                            self.game_choice = MEDIUM
                            self.game_size = 4
                            self.new()
                        elif button.text == "Hard":
                            self.game_choice = HARD
                            self.game_size = 5
                            self.new()
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                        if button.text == "Reset":
                            self.new()
                        elif button.text == "Solve it for me!":
                            self.solve_for_me()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start_shuffle = not self.start_shuffle


    # Sets the default game choice to Easy.
    def show_start_screen(self):
        self.game_choice = EASY
        self.game_size = 3


    # Placeholder for any game over screen logic.
    def show_go_screen(self):
        pass


game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
    game.show_go_screen()