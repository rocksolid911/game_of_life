import sys
import time
from src.models.grid import Grid
from src.utils.patterns import Patterns
from src.visualization.renderer import ConsoleRenderer


def main():
    # Parse command line arguments or use defaults
    width = 30
    height = 20
    fps = 10
    generations = None  # None for infinite

    # Parse optional arguments
    pattern_name = "glider"
    if len(sys.argv) > 1:
        pattern_name = sys.argv[1].lower()

    # Create the grid with the selected pattern
    grid = None

    if pattern_name == "glider":
        grid = Grid.from_pattern(Patterns.glider(), width, height)
    elif pattern_name == "blinker":
        grid = Grid.from_pattern(Patterns.blinker(), width, height)
    elif pattern_name == "block":
        grid = Grid.from_pattern(Patterns.block(), width, height)
    elif pattern_name == "beacon":
        grid = Grid.from_pattern(Patterns.beacon(), width, height)
    elif pattern_name == "pulsar":
        grid = Grid.from_pattern(Patterns.pulsar(), 30, 30)
    elif pattern_name == "glider_gun":
        grid = Grid.from_pattern(Patterns.gosper_glider_gun(), 50, 30)
    elif pattern_name == "random":
        grid = Grid.from_pattern(Patterns.random(width, height), width, height)
    else:
        print(f"Unknown pattern: {pattern_name}")
        print("Available patterns: glider, blinker, block, beacon, pulsar, glider_gun, random")
        return

    # Create the renderer
    renderer = ConsoleRenderer(grid, fps)

    print(f"Conway's Game of Life - Pattern: {pattern_name}")
    print("Press Ctrl+C to stop the animation")
    time.sleep(2)  # Give the user time to read the message

    # Start the animation
    renderer.start_animation(generations)

    print("Game of Life simulation ended.")


if __name__ == "__main__":
    main()