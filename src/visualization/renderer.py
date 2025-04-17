import time
import os
import sys
from typing import Optional, Callable
from src.models.grid import Grid


class ConsoleRenderer:
    """
    Renders the Game of Life grid in the console with proper in-place animation.
    """

    def __init__(self, grid: Grid, fps: int = 5):
        """
        Initialize the console renderer.

        Args:
            grid (Grid): The grid to render
            fps (int): Frames per second for animation
        """
        self.grid = grid
        self.fps = fps
        self.frame_delay = 1.0 / fps
        self.running = False

        # Display characters for cells
        self._alive_char = "■"
        self._dead_char = " "

        # Get terminal size
        self.terminal_width = 80  # Default fallback
        self.terminal_height = 24  # Default fallback
        try:
            # Try to get actual terminal size
            import shutil
            self.terminal_width, self.terminal_height = shutil.get_terminal_size()
        except:
            pass  # Use defaults if we can't get terminal size

    def _reset_cursor(self):
        """Reset cursor to the beginning of the console output."""
        # ANSI escape code to move cursor to the beginning
        print("\033[H", end="", flush=True)

    def _clear_screen(self):
        """Clear the entire screen."""
        # ANSI escape code to clear the screen and move cursor to home position
        print("\033[2J\033[H", end="", flush=True)

    def render_frame(self):
        """Render a single frame of the grid to a string."""
        # Create the output string
        output = []

        # Add header
        output.append(f"Conway's Game of Life - Generation: {self.grid.generation}")
        output.append(f"Live cells: {sum(1 for _ in self.grid.get_live_cells())}")
        output.append(f"Press Ctrl+C to exit")

        # Add top border
        border = "+" + "-" * (self.grid.width + 2) + "+"
        output.append(border)

        # Add grid content with borders
        for y in range(self.grid.height):
            row = "| "
            for x in range(self.grid.width):
                if self.grid.get_cell(x, y).is_alive:
                    row += self._alive_char
                else:
                    row += self._dead_char
            row += " |"
            output.append(row)

        # Add bottom border
        output.append(border)

        # Join all lines with newlines
        return "\n".join(output)

    def start_animation(self, generations: Optional[int] = None,
                        update_callback: Optional[Callable] = None):
        """
        Start animating the Game of Life.

        Args:
            generations (Optional[int]): Number of generations to animate
                                         (None for infinite)
            update_callback (Optional[Callable]): Function to call before each frame
                                                 to update the grid
        """
        try:
            # Clear screen once at the beginning
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

            self.running = True
            gen_count = 0

            while self.running and (generations is None or gen_count < generations):
                # Call the update callback if provided
                if update_callback is not None:
                    update_callback(self.grid)

                # Render the current frame
                frame = self.render_frame()

                # Reset cursor to top of console and print the frame
                self._reset_cursor()
                print(frame, end="", flush=True)

                # Advance to the next generation
                self.grid.next_generation()
                gen_count += 1

                # Wait for the next frame
                time.sleep(self.frame_delay)

        except KeyboardInterrupt:
            # Allow the user to stop the animation with Ctrl+C
            self.running = False
            print("\n\nAnimation stopped by user.")

    def stop_animation(self):
        """Stop the animation."""
        self.running = False