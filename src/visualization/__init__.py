# from .renderer import ConsoleRenderer
#
# __all__ = ['ConsoleRenderer']

from .renderer import ConsoleRenderer
from .pygame_renderer import PygameRenderer

__all__ = ['ConsoleRenderer', 'PygameRenderer']