BY Abdur Rafey (481971), Muhammad Furqan Raza (460535), and Tamkeen Sara (474585), students of NUST, SEECS, BSDS 1 2k23 A.

FOR the course Artificial Intelligence, taught by Dr. Seemab Latif, at NUST, SEECS.

FOR the Artificial Intelligence Project "Sliding Puzzle Solver Using A* Algorithm".

INSTRUCTIONS:
1. Open the folder in a python editor such as Visual Studio Code.
2. If you do not have version 2.5.0 of pygame installed, run "pip3 install -r requirements.txt" in the terminal to do so now.
3. Run main.py.

FILE DESCRIPTIONS:
1. main.py
	- defines the core logic and functionality for the sliding puzzle game, including tile movement, shuffling, puzzle-solving, high score tracking, and game controls.
2. sprites.py
	- classes for game tiles, buttons, and UI elements in Pygame.
3. settings.py
	- defines colors, screen dimensions, and game settings.
4. high_scores.txt
	- tracks highscores.
5. requirements.txt
	- project requirements.

NOTICE:
Depending on the processing power of your device, automatically solving the 15 and 24 puzzles might take some time. This is not an issue with the program's efficiency. The 15 and 24 puzzles have 15 trillion and 24 quintillion reachable configurations respectively, and it takes some time to solve them. In our testing, the 8 puzzle took, on average, under a second to solve, while the 14 puzzle took minutes. We were only able to solve the 24 puzzle on a device with a GPU.