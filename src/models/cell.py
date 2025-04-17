class Cell:
    """
    Represents a single cell in Conway's Game of Life.
    """

    def __init__(self, is_alive=False):
        """
        Initialize a cell with alive or dead state.

        Args:
            is_alive (bool): Initial state of the cell
        """
        self._alive = is_alive

    @property
    def is_alive(self):
        """
        Property to get the cell's state.

        Returns:
            bool: True if the cell is alive, False otherwise
        """
        return self._alive

    @is_alive.setter
    def is_alive(self, state):
        """
        Set the cell's state.

        Args:
            state (bool): New state of the cell
        """
        self._alive = bool(state)

    def toggle(self):
        """
        Toggle the cell's state between alive and dead.

        Returns:
            bool: The new state after toggling
        """
        self._alive = not self._alive
        return self._alive

    def will_be_alive(self, live_neighbors):
        """
        Determine if the cell will be alive in the next generation based on
        Conway's Game of Life rules.

        Rules:
        1. Any live cell with fewer than two live neighbors dies (underpopulation)
        2. Any live cell with two or three live neighbors lives on
        3. Any live cell with more than three live neighbors dies (overpopulation)
        4. Any dead cell with exactly three live neighbors becomes alive (reproduction)

        Args:
            live_neighbors (int): Number of live neighboring cells

        Returns:
            bool: True if the cell will be alive in the next generation
        """
        if self._alive:
            # Rules 1-3: Cell survival
            return 2 <= live_neighbors <= 3
        else:
            # Rule 4: Cell reproduction
            return live_neighbors == 3

    def __str__(self):
        """
        String representation of the cell.

        Returns:
            str: "■" if alive, "□" if dead
        """
        return "■" if self._alive else "□"

    def __repr__(self):
        """
        Developer representation of the cell.

        Returns:
            str: Cell(True) or Cell(False)
        """
        return f"Cell({self._alive})"