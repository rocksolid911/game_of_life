import time
import os
from typing import Optional, Callable
from src.models.grid import Grid


class ConsoleRenderer:
    """
    Renders the Game of Life grid in the console.
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

    def _clear_console(self) -> None:
        """Clear the console screen."""
        # This works on Windows, macOS, and Linux
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_frame(self) -> None:
        """Render a single frame of the grid."""
        self._clear_console()

        # Print generation info
        print(f"Generation: {self.grid.generation}")
        print(f"Live cells: {sum(1 for _ in self.grid.get_live_cells())}")

        # Print grid border
        border = "+" + "-" * (self.grid.width + 2) + "+"
        print(border)

        # Print grid with border
        for y in range(self.grid.height):
            row = "| "
            for x in range(self.grid.width):
                if self.grid.get_cell(x, y).is_alive:
                    row += self._alive_char
                else:
                    row += self._dead_char
            row += " |"
            print(row)

        # Print bottom border
        print(border)

    def start_animation(self, generations: Optional[int] = None,
                        update_callback: Optional[Callable] = None) -> None:
        """
        Start animating the Game of Life.

        Args:
            generations (Optional[int]): Number of generations to animate
                                         (None for infinite)
            update_callback (Optional[Callable]): Function to call before each frame
                                                 to update the grid
        """
        self.running = True
        gen_count = 0

        try:
            while self.running and (generations is None or gen_count < generations):
                # Call the update callback if provided
                if update_callback is not None:
                    update_callback(self.grid)

                # Render the current state
                self.render_frame()

                # Advance to the next generation
                self.grid.next_generation()
                gen_count += 1

                # Wait for the next frame
                time.sleep(self.frame_delay)

        except KeyboardInterrupt:
            # Allow the user to stop the animation with Ctrl+C
            self.running = False
            print("\nAnimation stopped by user.")

    def stop_animation(self) -> None:
        """Stop the animation."""
        self.running = False