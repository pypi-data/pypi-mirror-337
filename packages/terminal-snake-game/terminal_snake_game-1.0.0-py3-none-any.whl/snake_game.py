#!/opt/homebrew/bin/python3

import curses
import random
import time
import os

class Snake:
    def __init__(self, start_y, start_x, window):
        self.body = [
            [start_y, start_x],       # Head
            [start_y, start_x - 1],   # Body
            [start_y, start_x - 2]    # Tail
        ]
        self.direction = curses.KEY_RIGHT
        self.window = window
        self.score = 0
        self.growth_pending = 0
    
    def draw(self):
        # Draw the snake on the window
        for i, segment in enumerate(self.body):
            # Different characters for head, body, and tail
            if i == 0:  # Head
                if self.direction == curses.KEY_RIGHT:
                    char = '▶'
                elif self.direction == curses.KEY_LEFT:
                    char = '◀'
                elif self.direction == curses.KEY_UP:
                    char = '▲'
                else:  # DOWN
                    char = '▼'
            else:  # Body and tail
                char = '◆'  # Diamond for horizontal movement
            try:
                self.window.addch(segment[0], segment[1], char, curses.color_pair(1) | curses.A_BOLD)
            except curses.error:
                pass  # Ignore errors when trying to draw at the edge
    
    def move(self, direction):
        # Update direction if it's valid (can't go directly opposite)
        if direction == curses.KEY_DOWN and self.direction != curses.KEY_UP:
            self.direction = direction
        elif direction == curses.KEY_UP and self.direction != curses.KEY_DOWN:
            self.direction = direction
        elif direction == curses.KEY_LEFT and self.direction != curses.KEY_RIGHT:
            self.direction = direction
        elif direction == curses.KEY_RIGHT and self.direction != curses.KEY_LEFT:
            self.direction = direction
        
        # Get current head position
        head = self.body[0].copy()
        
        # Calculate new head position based on direction
        if self.direction == curses.KEY_UP:
            head[0] -= 1
        elif self.direction == curses.KEY_DOWN:
            head[0] += 1
        elif self.direction == curses.KEY_LEFT:
            head[1] -= 1
        elif self.direction == curses.KEY_RIGHT:
            head[1] += 1
        
        # Insert new head
        self.body.insert(0, head)
        
        # Remove tail if no growth pending
        if self.growth_pending <= 0:
            tail = self.body.pop()
            try:
                self.window.addch(tail[0], tail[1], ' ')  # Clear the tail position
            except curses.error:
                pass
        else:
            self.growth_pending -= 1
    
    def grow(self, amount=1):
        """Add segments to the snake when it eats food"""
        self.growth_pending += amount
        self.score += 1
    
    def check_collision(self, sh, sw):
        """Check if snake has collided with wall or itself"""
        head = self.body[0]
        
        # Check wall collision (respecting the border)
        if head[0] <= 0 or head[0] >= sh-1 or head[1] <= 0 or head[1] >= sw-1:
            return True
        
        # Check self collision (if head collides with any segment)
        if head in self.body[1:]:
            return True
        
        return False
    
    def check_food(self, food):
        """Check if snake has eaten food"""
        if self.body[0] == food:
            return True
        return False

class Food:
    def __init__(self, window, sh, sw):
        self.window = window
        self.position = [0, 0]
        self.sh = sh
        self.sw = sw
        self.generate()
    
    def generate(self, snake_body=None):
        """Generate food at random position, avoiding snake body"""
        while True:
            # Generate random position within bounds
            # Add extra margin to avoid borders
            y = random.randint(2, self.sh-3)
            x = random.randint(2, self.sw-3)
            
            # Ensure it's not on the snake
            if snake_body and [y, x] in snake_body:
                continue
            
            # Set position and draw
            self.position = [y, x]
            try:
                self.window.addch(y, x, '★', curses.color_pair(2) | curses.A_BOLD)
                break  # Only break the loop if drawing was successful
            except curses.error:
                # Try a different position if we couldn't draw here
                continue
    
    def draw(self):
        """Draw food on the screen"""
        try:
            self.window.addch(self.position[0], self.position[1], '★', curses.color_pair(2) | curses.A_BOLD)
        except curses.error:
            pass

def display_score(score_window, control_window, score):
    """Display the current score and high score in separate windows"""
    high_score = get_high_score()
    score_text = f"⭐ Score: {score} ⭐"
    high_score_text = f"🏆 High Score: {high_score} 🏆"
    controls_text = "Controls: ↑ ↓ ← → | q: Quit | r: Restart"
    
    try:
        # Clear the score window and redraw
        score_window.clear()
        sw = score_window.getmaxyx()[1]
        
        # Add decorative elements and scores
        score_window.addstr(1, 4, score_text, curses.color_pair(6) | curses.A_BOLD)
        score_window.addstr(1, sw - len(high_score_text) - 4, high_score_text, curses.color_pair(6) | curses.A_BOLD)
        
        # Add fancy border to score window
        score_window.attrset(curses.color_pair(5))
        score_window.box()
        score_window.refresh()
        
        # Clear the control window and redraw
        control_window.clear()
        cw = control_window.getmaxyx()[1]
        
        # Add controls with decorative elements
        control_window.addstr(1, (cw-len(controls_text))//2, controls_text, curses.color_pair(7) | curses.A_BOLD)
        
        # Add fancy border to control window
        control_window.attrset(curses.color_pair(5))
        control_window.box()
        control_window.refresh()
    except curses.error:
        pass

def display_game_over(window, score):
    """Display game over message with a border"""
    sh, sw = window.getmaxyx()
    game_over_msg = "💀 GAME OVER! 💀"
    final_score_msg = f" Final Score: {score}"
    
    # Update high score if needed
    high_score = get_high_score()
    if score > high_score:
        set_high_score(score)
        high_score = score
        high_score_msg = f"🏆 NEW HIGH SCORE: {high_score}! 🏆"
    else:
        high_score_msg = f" High Score: {high_score}"
    
    restart_msg = "Press 'r' to restart or 'q' to quit"
    
    try:
        # Clear the screen
        window.clear()
        
        # Draw fancy border
        window.attrset(curses.color_pair(5))
        window.border()
        window.refresh()
        
        # Create box for game over message
        box_height = 7
        box_width = max(len(game_over_msg), len(final_score_msg), len(high_score_msg), len(restart_msg)) + 8
        box_y = (sh - box_height) // 2
        box_x = (sw - box_width) // 2
        
        # Draw decorative box
        for y in range(box_y, box_y + box_height):
            for x in range(box_x, box_x + box_width):
                if y in (box_y, box_y + box_height - 1):
                    if x == box_x:
                        window.addch(y, x, '╔' if y == box_y else '╚', curses.color_pair(4))
                    elif x == box_x + box_width - 1:
                        window.addch(y, x, '╗' if y == box_y else '╝', curses.color_pair(4))
                    else:
                        window.addch(y, x, '═', curses.color_pair(4))
                elif x in (box_x, box_x + box_width - 1):
                    window.addch(y, x, '║', curses.color_pair(4))
        
        # Center each message in the box
        box_inner_width = box_width - 2
        window.addstr(box_y + 2, box_x + (box_inner_width - len(game_over_msg))//2 + 1, 
                     game_over_msg, curses.color_pair(4) | curses.A_BOLD)
        window.addstr(box_y + 3, box_x + (box_inner_width - len(final_score_msg))//2 + 1, 
                     final_score_msg, curses.color_pair(6) | curses.A_BOLD)
        window.addstr(box_y + 4, box_x + (box_inner_width - len(high_score_msg))//2 + 1, 
                     high_score_msg, curses.color_pair(2) | curses.A_BOLD)
        window.addstr(box_y + 5, box_x + (box_inner_width - len(restart_msg))//2 + 1, 
                     restart_msg, curses.color_pair(3) | curses.A_BOLD)
        window.refresh()
    except curses.error:
        pass

def display_welcome_screen(window):
    """Display welcome screen with instructions"""
    sh, sw = window.getmaxyx()
    title = "🐍 SNAKE GAME 🐍"
    instructions = [
        "How to Play:",
        "• Use arrow keys (↑ ↓ ← →) to control the snake",
        "• Eat ★ to grow and score points",  # Changed to match the actual food character
        "• Avoid hitting walls and yourself",
        "",
        "Press any key to start..."
    ]
    
    try:
        # Clear and draw welcome screen
        window.clear()
        window.refresh()
        
        # Draw fancy border
        window.attrset(curses.color_pair(5))
        window.border()
        window.refresh()
        
        # Draw title and instructions
        title_y = sh//2 - len(instructions)//2 - 2
        title_x = (sw-len(title))//2
        
        # Draw title with a decorative box
        window.addstr(title_y - 1, title_x - 2, "╔" + "═" * (len(title) + 4) + "╗", curses.color_pair(2))
        window.addstr(title_y, title_x - 2, "║ " + title + " ║", curses.color_pair(2) | curses.A_BOLD)
        window.addstr(title_y + 1, title_x - 2, "╚" + "═" * (len(title) + 4) + "╝", curses.color_pair(2))
        
        # Draw instructions with different colors
        colors = [3, 6, 2, 3, 7, 4]  # Different colors for each line
        for i, line in enumerate(instructions):
            window.addstr(title_y + 3 + i, (sw-len(line))//2, line, 
                        curses.color_pair(colors[i]) | curses.A_BOLD)
        
        window.refresh()
        
        # Wait for user to press a key
        window.getch()
        
        # Clear screen after key press
        window.clear()
        window.refresh()
        
        # Redraw border for game screen
        window.attrset(curses.color_pair(5))
        window.border()
        window.refresh()
    except curses.error:
        pass

def get_high_score():
    """Read high score from file"""
    try:
        with open(os.path.expanduser('~/.snake_game_score'), 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def set_high_score(score):
    """Save high score to file"""
    try:
        with open(os.path.expanduser('~/.snake_game_score'), 'w') as f:
            f.write(str(score))
    except:
        pass

def main():
    # Initial curses setup
    screen = curses.initscr()
    
    try:
        # Initialize curses settings
        curses.start_color()
        curses.curs_set(0)  # Hide the cursor
        screen.keypad(1)  # Enable keypad input
        curses.noecho()  # Don't echo keypresses
        curses.cbreak()  # React to keys instantly
        
        # Initialize colors with more vibrant combinations
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Snake body
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Food
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)     # Info text
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)      # Game Over
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Borders
        curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)     # Score
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Controls
        
        # Get screen dimensions
        sh, sw = screen.getmaxyx()
        
        # Create windows for different parts of the game
        score_height = 3
        control_height = 3
        game_height = sh - score_height - control_height
        
        # Create the three windows: score at top, game in middle, controls at bottom
        score_window = curses.newwin(score_height, sw, 0, 0)
        game_window = curses.newwin(game_height, sw, score_height, 0)
        control_window = curses.newwin(control_height, sw, sh-control_height, 0)
        
        game_window.keypad(1)
        
        # Add decorative attributes to windows
        score_window.attrset(curses.color_pair(6))
        control_window.attrset(curses.color_pair(7))
        game_window.attrset(curses.color_pair(5))

        while True:  # Main game session loop
            # Show welcome screen first
            game_window.timeout(-1)  # Wait indefinitely for input on welcome screen
            display_welcome_screen(game_window)
            
            # Set up game speed after welcome screen
            game_window.timeout(100)  # Refresh rate in milliseconds
            
            # Initialize game state
            snake = Snake(game_height // 2, max(sw // 4, 3), game_window)
            food = Food(game_window, game_height-1, sw-1)
            
            # Draw initial game state
            snake.draw()
            food.draw()
            display_score(score_window, control_window, 0)
            game_window.refresh()
            
            # Initialize key variable with default direction
            key = curses.KEY_RIGHT
            
            # Game loop
            while True:
                # Get next key input (non-blocking)
                next_key = game_window.getch()
                
                # If user pressed a key, update direction
                if next_key != -1:
                    key = next_key
                
                # Check for restart or quit
                if key == ord('q'):
                    return  # Exit the entire game
                
                # Move snake
                snake.move(key)
                
                # Check for collision
                if snake.check_collision(game_height, sw):
                    game_window.timeout(-1)  # Wait indefinitely for input on game over screen
                    display_game_over(game_window, snake.score)
                    while True:
                        choice = game_window.getch()
                        if choice == ord('r'):
                            break  # Break inner loop to restart game
                        elif choice == ord('q'):
                            return  # Exit the entire game
                    break  # Break game loop to show welcome screen again
                
                # Draw the snake
                snake.draw()
                
                # Check if food eaten
                if snake.check_food(food.position):
                    snake.grow()
                    # Pass the snake's body to ensure food doesn't spawn on snake
                    food.generate(snake_body=snake.body)
                    # Update score display
                    display_score(score_window, control_window, snake.score)
                
                # Draw food
                food.draw()
                
                # Make sure border is intact
                game_window.border(curses.ACS_VLINE, curses.ACS_VLINE, 
                                curses.ACS_HLINE, curses.ACS_HLINE, 
                                curses.ACS_ULCORNER, curses.ACS_URCORNER, 
                                curses.ACS_LLCORNER, curses.ACS_LRCORNER)
                
                # Refresh the game window
                game_window.refresh()
    finally:
        # Clean up curses
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()

if __name__ == "__main__":
    # Ensure the terminal is in a clean state before starting
    os.system('clear')
    # Add a small delay to ensure terminal is ready
    time.sleep(0.1)
    main()

