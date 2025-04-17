from typing import List


class Patterns:
    """
    Static utility class providing common patterns for Conway's Game of Life.
    """

    @staticmethod
    def glider() -> List[List[bool]]:
        """
        Returns a glider pattern that moves diagonally.

        Returns:
            List[List[bool]]: 2D array representing the glider pattern
        """
        return [
            [False, True, False],
            [False, False, True],
            [True, True, True]
        ]

    @staticmethod
    def blinker() -> List[List[bool]]:
        """
        Returns a blinker pattern that oscillates vertically and horizontally.

        Returns:
            List[List[bool]]: 2D array representing the blinker pattern
        """
        return [
            [False, False, False],
            [True, True, True],
            [False, False, False]
        ]

    @staticmethod
    def block() -> List[List[bool]]:
        """
        Returns a block pattern (2x2 square) that is stable.

        Returns:
            List[List[bool]]: 2D array representing the block pattern
        """
        return [
            [True, True],
            [True, True]
        ]

    @staticmethod
    def beacon() -> List[List[bool]]:
        """
        Returns a beacon pattern that oscillates.

        Returns:
            List[List[bool]]: 2D array representing the beacon pattern
        """
        return [
            [True, True, False, False],
            [True, True, False, False],
            [False, False, True, True],
            [False, False, True, True]
        ]

    @staticmethod
    def pulsar() -> List[List[bool]]:
        """
        Returns a pulsar pattern, which is a larger oscillator.

        Returns:
            List[List[bool]]: 2D array representing the pulsar pattern
        """
        # Create a 17x17 grid of False values
        pattern = [[False for _ in range(17)] for _ in range(17)]

        # Define the coordinates that should be True
        # Using the symmetry of the pattern to define it more concisely
        points = [
            # Top row of each 3x3 section
            (2, 4), (2, 5), (2, 6),
            (2, 10), (2, 11), (2, 12),

            # Middle row of each 3x3 section
            (4, 2), (5, 2), (6, 2),
            (4, 7), (5, 7), (6, 7),
            (4, 9), (5, 9), (6, 9),
            (4, 14), (5, 14), (6, 14),

            # Bottom row of each 3x3 section
            (7, 4), (7, 5), (7, 6),
            (7, 10), (7, 11), (7, 12),

            # Replicated for the bottom half by symmetry
            (9, 4), (9, 5), (9, 6),
            (9, 10), (9, 11), (9, 12),

            (10, 2), (11, 2), (12, 2),
            (10, 7), (11, 7), (12, 7),
            (10, 9), (11, 9), (12, 9),
            (10, 14), (11, 14), (12, 14),

            (14, 4), (14, 5), (14, 6),
            (14, 10), (14, 11), (14, 12),
        ]

        # Set the specified points to True
        for x, y in points:
            pattern[y][x] = True

        return pattern

    @staticmethod
    def gosper_glider_gun() -> List[List[bool]]:
        """
        Returns the Gosper Glider Gun pattern which periodically creates gliders.

        Returns:
            List[List[bool]]: 2D array representing the glider gun pattern
        """
        pattern = [[False for _ in range(36)] for _ in range(9)]

        # Define the points to be set as alive
        points = [
            # Left block
            (0, 4), (1, 4), (0, 5), (1, 5),

            # Left ship
            (10, 4), (10, 5), (10, 6),
            (11, 3), (11, 7),
            (12, 2), (12, 8),
            (13, 2), (13, 8),
            (14, 5),
            (15, 3), (15, 7),
            (16, 4), (16, 5), (16, 6),
            (17, 5),

            # Right ship
            (20, 2), (20, 3), (20, 4),
            (21, 2), (21, 3), (21, 4),
            (22, 1), (22, 5),
            (24, 0), (24, 1), (24, 5), (24, 6),

            # Right block
            (34, 2), (34, 3),
            (35, 2), (35, 3)
        ]

        # Set the specified points to True
        for x, y in points:
            pattern[y][x] = True

        return pattern

    @staticmethod
    def random(width: int, height: int, probability: float = 0.3) -> List[List[bool]]:
        """
        Generates a random pattern with the specified probability of cells being alive.

        Args:
            width (int): Width of the pattern
            height (int): Height of the pattern
            probability (float): Probability of each cell being alive (0-1)

        Returns:
            List[List[bool]]: 2D array representing the random pattern
        """
        import random

        pattern = []
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(random.random() < probability)
            pattern.append(row)

        return pattern