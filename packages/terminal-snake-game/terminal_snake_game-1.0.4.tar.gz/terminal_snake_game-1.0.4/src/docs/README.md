# Snake Game

A classic Snake game implemented in Python using the curses library. This terminal-based game features colorful graphics, score tracking, and an intuitive interface.

## Demo

![Snake Game Demo](https://raw.githubusercontent.com/SwetaTanwar/snake-game/main/demo/snake-game-demo.gif)

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

## Development and Testing

### Setting up Development Environment

1. Create a virtual environment:
   ```bash
   python -m venv test_env
   source test_env/bin/activate  # On Unix/macOS
   # or
   test_env\Scripts\activate  # On Windows
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[test]"
   ```

### Running Tests

The game includes a comprehensive test suite that verifies core functionality. To run the tests:

```bash
# Run all tests
python -m pytest src/tests/

# Run tests with verbose output
python -m pytest src/tests/ -v

# Run tests with coverage report
python -m pytest src/tests/ --cov=terminal_snake_game
```

The test suite covers:
- Snake movement and collision detection
- Food generation and placement
- Score tracking
- Window management and display
- Game mechanics validation

When contributing new features, please ensure to:
1. Add appropriate test cases
2. Run the full test suite before submitting changes
3. Maintain or improve the current test coverage 