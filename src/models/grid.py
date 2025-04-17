from typing import List, Tuple, Generator, Optional
from .cell import Cell


class Grid:
    """
    Represents the 2D grid for Conway's Game of Life.
    """

    def __init__(self, width: int, height: int):
        """
        Initialize a grid with the specified dimensions.

        Args:
            width (int): Width of the grid
            height (int): Height of the grid
        """
        self.width = width
        self.height = height
        # Initialize grid with dead cells
        self._grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self._generation = 0

    @property
    def generation(self) -> int:
        """Return the current generation number."""
        return self._generation

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Get the cell at the specified position.

        Args:
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            Cell: The cell at the specified position
        """
        # Handle wrapping around the edges (toroidal grid)
        x = x % self.width
        y = y % self.height
        return self._grid[y][x]

    def set_cell(self, x: int, y: int, alive: bool = True) -> None:
        """
        Set the state of the cell at the specified position.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            alive (bool): Whether the cell should be alive
        """
        # Handle wrapping around the edges
        x = x % self.width
        y = y % self.height
        self._grid[y][x].is_alive = alive

    def toggle_cell(self, x: int, y: int) -> bool:
        """
        Toggle the state of the cell at the specified position.

        Args:
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            bool: The new state of the cell
        """
        # Handle wrapping around the edges
        x = x % self.width
        y = y % self.height
        return self._grid[y][x].toggle()

    def count_live_neighbors(self, x: int, y: int) -> int:
        """
        Count the number of live neighboring cells for a given position.

        Args:
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            int: Number of live neighbors
        """
        count = 0
        # Check all 8 neighboring cells
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                # Skip the cell itself
                if dx == 0 and dy == 0:
                    continue

                # Get neighbor coordinates with wrapping
                nx, ny = (x + dx) % self.width, (y + dy) % self.height

                # Count if the neighbor is alive
                if self._grid[ny][nx].is_alive:
                    count += 1

        return count

    def next_generation(self) -> None:
        """
        Advance the grid to the next generation according to Game of Life rules.
        """
        # Calculate the next state for each cell
        next_states = {}
        for y in range(self.height):
            for x in range(self.width):
                live_neighbors = self.count_live_neighbors(x, y)
                cell = self.get_cell(x, y)
                next_states[(x, y)] = cell.will_be_alive(live_neighbors)

        # Update all cells with their new states
        for (x, y), alive in next_states.items():
            self.set_cell(x, y, alive)

        # Increment generation counter
        self._generation += 1

    def clear(self) -> None:
        """Reset all cells to dead state."""
        for y in range(self.height):
            for x in range(self.width):
                self.set_cell(x, y, False)
        self._generation = 0

    @classmethod
    def from_pattern(cls, pattern: List[List[bool]], width: Optional[int] = None,
                     height: Optional[int] = None) -> 'Grid':
        """
        Create a grid with a predefined pattern.

        Args:
            pattern (List[List[bool]]): 2D array of boolean values representing the pattern
            width (Optional[int]): Width of the grid, defaults to pattern width + 10
            height (Optional[int]): Height of the grid, defaults to pattern height + 10

        Returns:
            Grid: New grid with the pattern set
        """
        pattern_height = len(pattern)
        pattern_width = len(pattern[0]) if pattern_height > 0 else 0

        # Set default grid size if not specified
        if width is None:
            width = pattern_width + 10
        if height is None:
            height = pattern_height + 10

        # Create new grid
        grid = cls(width, height)

        # Calculate starting position to center the pattern
        start_x = (width - pattern_width) // 2
        start_y = (height - pattern_height) // 2

        # Set cells according to pattern
        for y, row in enumerate(pattern):
            for x, cell_state in enumerate(row):
                if cell_state:
                    grid.set_cell(start_x + x, start_y + y, True)

        return grid

    def get_live_cells(self) -> Generator[Tuple[int, int], None, None]:
        """
        Generator that yields the coordinates of all live cells.

        Yields:
            Tuple[int, int]: Coordinates (x, y) of live cells
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.get_cell(x, y).is_alive:
                    yield x, y

    def __str__(self) -> str:
        """
        String representation of the grid.

        Returns:
            str: Visual representation of the grid
        """
        result = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(str(self.get_cell(x, y)))
            result.append(''.join(row))
        return '\n'.join(result)