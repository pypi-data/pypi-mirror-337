# Contributing to Terminal Snake Game

Thank you for your interest in contributing to the Terminal Snake Game! This document provides guidelines and steps for contributing to the project.

## Development Setup

1. Fork the repository and clone your fork:
   ```bash
   git clone git@github.com:YOUR_USERNAME/snake-game.git
   cd snake-game
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   .\venv\Scripts\activate  # On Windows
   ```

3. Install development dependencies:
   ```bash
   python3 -m pip install --upgrade pip build twine
   ```

## Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

2. Make your changes to the code.

3. Test your changes:
   - Run the game locally: `python3 snake_game.py`
   - Ensure the game works in different terminal sizes (minimum 80x24 characters)
   - Check that high scores are saved correctly
   - Verify that all controls work as expected
   - Test on different operating systems if possible (Unix/macOS/Windows)
   - Check that the game exits cleanly without errors

## Building and Testing the Package

1. Clean any existing build files:
   ```bash
   rm -rf build/ dist/ terminal_snake_game.egg-info/ build_dist/
   ```

2. Build the package:
   ```bash
   python3 -m build
   ```

3. Test the built package locally:
   ```bash
   # Create a new virtual environment for testing
   python3 -m venv test_env
   source test_env/bin/activate  # On Unix/macOS
   # or
   .\test_env\Scripts\activate  # On Windows

   # Install the package from the wheel file
   pip install dist/terminal_snake_game-*.whl

   # Test running the game (make sure terminal is at least 80x24 characters)
   snake-game
   # or
   python3 -m snake_game
   ```

4. Clean up test environment when done:
   ```bash
   # Deactivate virtual environment
   deactivate
   
   # Remove test environment
   rm -rf test_env/
   
   # Uninstall package if needed
   pip uninstall terminal-snake-game
   ```

## Submitting Changes

1. Commit your changes with a descriptive message:
   ```bash
   git add .
   git commit -m "type: brief description of changes"
   ```
   Commit message types:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `style:` for formatting changes
   - `refactor:` for code refactoring
   - `test:` for adding tests
   - `chore:` for maintenance tasks (version bumps, etc.)

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request:
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template with details about your changes
   - Include screenshots or GIFs if you made UI changes
   - Reference any related issues

## Publishing to PyPI (for maintainers)

1. Update version number in `setup.py`:
   ```python
   setup(
       name="terminal-snake-game",
       version="X.Y.Z",  # Increment version number
       ...
   )
   ```
   Follow semantic versioning:
   - MAJOR version (X) for incompatible API changes
   - MINOR version (Y) for new features in a backward compatible manner
   - PATCH version (Z) for backward compatible bug fixes

2. Commit version bump:
   ```bash
   git add setup.py
   git commit -m "chore: bump version to X.Y.Z"
   git push
   ```

3. Clean and rebuild the package:
   ```bash
   # Create a new virtual environment for building
   python3 -m venv build_env
   source build_env/bin/activate
   
   # Install build tools
   python3 -m pip install --upgrade pip build twine
   
   # Clean old build files
   rm -rf build/ dist/ terminal_snake_game.egg-info/
   
   # Build the package
   python3 -m build
   ```

4. Upload to PyPI:
   ```bash
   python3 -m twine upload dist/*
   # Enter your PyPI username and password/token when prompted
   ```
   Note: For security, use an API token instead of your password. You can create one at https://pypi.org/manage/account/token/

5. Clean up build environment:
   ```bash
   deactivate
   rm -rf build_env/
   ```

6. Verify the package:
   - Check the PyPI page: https://pypi.org/project/terminal-snake-game/
   - Create a new virtual environment and test installation:
     ```bash
     python3 -m venv test_env
     source test_env/bin/activate
     pip install terminal-snake-game
     snake-game  # Test in a terminal of at least 80x24 characters
     ```
   - Verify that the README and demo are displayed correctly on PyPI
   - Check that all package metadata is correct

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular
- Update documentation for new features
- Ensure README.md is up to date with any new features or changes
- Add docstrings for new functions and classes
- Keep line length under 100 characters
- Use type hints where appropriate

## Need Help?

If you need help with any part of the contribution process:
1. Check existing issues and pull requests
2. Create a new issue with the "question" label
3. Reach out to the maintainers
4. Check the [Python Packaging User Guide](https://packaging.python.org/) for packaging help

Thank you for contributing to make the Terminal Snake Game better! 🐍 