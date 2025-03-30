# Snake Game

A classic Snake game implemented in Python using the curses library. This terminal-based game features colorful graphics, score tracking, and an intuitive interface.

## Demo

![Snake Game Demo](demo/snake-game-demo.gif)

## Features

- Colorful terminal-based UI
- Score and high score tracking
- Direction-aware snake appearance
- Game over screen with restart option
- Persistent high score storage

## Requirements

- Python 3.6 or higher
- curses library (included in standard Python distribution)

## Installation & Running

There are two ways to install and run the game:

### Method 1: Using pip (Recommended)

1. Install the package:
   ```bash
   pip install terminal-snake-game
   ```

2. Run the game:
   ```bash
   # Either use the command-line tool
   snake-game

   # Or run as a Python module
   python3 -m snake_game
   ```

### Method 2: From Source

1. Clone the repository:
   ```bash
   git clone git@github.com:SwetaTanwar/snake-game.git
   cd snake-game
   ```

2. Run the game:
   ```bash
   # Using Python directly
   python3 snake_game.py
   ```

   Or make it executable first:
   ```bash
   # Make the script executable
   chmod +x snake_game.py
   
   # Then run directly
   ./snake_game.py
   ```

## How to Play

### Controls
- Use arrow keys (↑ ↓ ← →) to control the snake
- Eat ★ to grow and score points
- Press 'q' to quit
- Press 'r' to restart after game over

## Game Elements

- 🐍 Snake head shows direction (▶ ◀ ▲ ▼)
- ◆ Snake body
- ★ Food
- Score and high score display at the top
- Control instructions at the bottom 