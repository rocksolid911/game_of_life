import pygame
import time
from typing import Optional, Callable
from src.models.grid import Grid


class PygameRenderer:
    """
    Renders the Game of Life grid using Pygame for smooth animation.
    """

    def __init__(self, grid: Grid, cell_size: int = 20, fps: int = 10):
        """
        Initialize the Pygame renderer.

        Args:
            grid (Grid): The grid to render
            cell_size (int): Size of each cell in pixels
            fps (int): Frames per second for animation
        """
        self.grid = grid
        self.cell_size = cell_size
        self.fps = fps
        self.running = False

        # Calculate window dimensions
        self.width = grid.width * cell_size
        self.height = grid.height * cell_size

        # Colors
        self.bg_color = (10, 10, 10)  # Almost black
        self.grid_color = (40, 40, 40)  # Dark gray
        self.cell_color = (0, 255, 0)  # Green
        self.text_color = (200, 200, 200)  # Light gray

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height + 40))  # Extra height for text
        pygame.display.set_caption("Conway's Game of Life")
        self.font = pygame.font.SysFont('Arial', 16)
        self.clock = pygame.time.Clock()

    def render_frame(self):
        """Render a single frame of the grid."""
        # Fill the background
        self.screen.fill(self.bg_color)

        # Draw grid lines
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))

        # Draw living cells
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid.get_cell(x, y).is_alive:
                    rect = pygame.Rect(
                        x * self.cell_size + 1,  # +1 to account for grid lines
                        y * self.cell_size + 1,
                        self.cell_size - 1,
                        self.cell_size - 1
                    )
                    pygame.draw.rect(self.screen, self.cell_color, rect)

        # Draw generation and live cell count
        gen_text = self.font.render(f"Generation: {self.grid.generation}", True, self.text_color)
        self.screen.blit(gen_text, (10, self.height + 5))

        live_count = sum(1 for _ in self.grid.get_live_cells())
        count_text = self.font.render(f"Live cells: {live_count}", True, self.text_color)
        self.screen.blit(count_text, (10, self.height + 25))

        # Update the display
        pygame.display.flip()

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
        self.running = True
        gen_count = 0

        while self.running and (generations is None or gen_count < generations):
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.running = False

            # Call the update callback if provided
            if update_callback is not None:
                update_callback(self.grid)

            # Render the current state
            self.render_frame()

            # Advance to the next generation
            self.grid.next_generation()
            gen_count += 1

            # Control the frame rate
            self.clock.tick(self.fps)

        # Clean up
        pygame.quit()

    def stop_animation(self):
        """Stop the animation."""
        self.running = False