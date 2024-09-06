# AI-agent-2048

This project demonstrates an AI agent playing the popular 2048 game, striving to achieve high scores through intelligent decision-making. The agent employs the Expectimax search algorithm and strategic heuristics to guide its gameplay.
***
## Project Overview
- **Goal:** Create an AI capable of playing 2048 autonomously and achieving high scores.
- **Approach:** Utilize a combination of the Expectimax algorithm and heuristics to evaluate possible moves and select the most promising one.
- **Implementation:** Developed in Python using the Pygame library for game visualization.
***
## Algorithms and Techniques
- **Expectimax Algorithm:** A decision-making algorithm for scenarios involving randomness (like the new tile placement in 2048).
The AI simulates different moves and evaluates the expected outcomes, considering the probabilities of various tile placements.
- **Heuristics:**
  - **Monotonicity:** Promotes keeping tiles in increasing or decreasing order for easier merging.
  - **Smoothness:** Encourages a board with adjacent tiles of similar values to facilitate merges.
  - **Free Tiles:** Values having more empty tiles, providing more flexibility for future moves.
***
## How to Run the Project
0. **Prerequisites:**
- `Python 3.x`: Make sure you have Python 3 installed on your system. You can check by running python --version in your terminal.
- `Pygame`: Install the Pygame library using pip: pip install pygame

1. **Run the Game:**
  Navigate to the project directory in your terminal and then execute the following command:
  ```
  python withAI.py
  ```
  The game window will appear, and the AI agent will start playing.
***
## Understanding the Code
- `withAI.py`: It contains the main game logic, including the implementation of the game board, move mechanics, Expectimax algorithm, heuristics, and the Pygame visualization.
- **Key Functions**
  1. **expectimax(grid, depth, maximizing_player):**
     - Core of the AI decision-making, implementing the Expectimax algorithm.
     - Recursively explores possible moves and tile placements to evaluate their potential scores.
  2. **monotonicity(grid), smoothness(grid), free_tiles(grid):**
     - Heuristic functions that assess the favorability of different board states.
  4. **move(grid, direction):**
     - Handles tile movement, merging, and adding new tiles based on the chosen direction.
  6. **game_over(grid):**
     - Checks if the game has ended (no more valid moves or the 2048 tile has been reached).
  8. **draw_board():**
     - Renders the game board and tiles using Pygame.

***
