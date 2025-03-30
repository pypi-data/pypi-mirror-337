"""Useful constants."""

import importlib.util
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterator, Self, SupportsIndex, cast

import numpy as np

__all__ = [
    "Direction",
    "ORIGIN",
    "LEFT",
    "RIGHT",
    "DOWN",
    "UP",
    "DL",
    "DR",
    "UL",
    "UR",
    "ALWAYS",
    "EXTRAS_INSTALLED",
    "Quality",
    "QualitySetting",
]


@dataclass
class Direction:
    """A 2D vector.

    Args:
        x: X position, typically in the unit square.
        y: Y position, typically in the unit square.
    """

    x: float
    y: float

    def __post_init__(self) -> None:
        self.vector = np.array([self.x, self.y], dtype=np.float64)

    def __add__(self, other: Any) -> Self:
        if isinstance(other, Direction):
            return type(self)(*(self.vector + other.vector))
        elif isinstance(other, (np.ndarray, float, int)):
            return type(self)(*(self.vector + np.array(other)))
        return NotImplemented

    def __radd__(self, other: Any) -> Self:
        return self.__add__(other)

    def __sub__(self, other: Any) -> Self:
        if isinstance(other, Direction):
            return type(self)(*(self.vector - other.vector))
        elif isinstance(other, (np.ndarray, float, int)):
            return type(self)(*(self.vector - np.array(other)))
        return NotImplemented

    def __rsub__(self, other: Any) -> "Direction":
        if isinstance(other, (np.ndarray, float, int)):
            return Direction(*(np.array(other, dtype=np.float64) - self.vector))
        return NotImplemented

    def __mul__(self, other: Any) -> Self:
        if isinstance(other, (int, float)):
            return type(self)(*(self.vector * other))
        return NotImplemented

    def __rmul__(self, other: Any) -> Self:
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> Self:
        if isinstance(other, (int, float)):
            if other == 0:
                raise ValueError("Division by 0.")
            return type(self)(*(self.vector / other))
        return NotImplemented

    def __eq__(self, other: Any) -> bool:
        return np.array_equal(self.vector, other.vector) if isinstance(other, Direction) else False

    def __neg__(self) -> Self:
        return -1 * self

    def __hash__(self) -> int:
        return hash(tuple(self.vector))

    def __getitem__(self, idx: SupportsIndex) -> float:
        return cast(float, self.vector[idx.__index__()])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.vector[0]}, {self.vector[1]})"


ORIGIN = Direction(0.0, 0.0)
"""Center."""
LEFT = Direction(-1.0, 0.0)
"""Left side."""
RIGHT = Direction(1.0, 0.0)
"""Right side."""
DOWN = Direction(0.0, -1.0)
"""Bottom side."""
UP = Direction(0.0, 1.0)
"""Top side."""
DL = DOWN + LEFT
"""Bottom left side."""
DR = DOWN + RIGHT
"""Bottom right side."""
UL = UP + LEFT
"""Top left side."""
UR = UP + RIGHT
"""Top right side."""

ALWAYS = -9_999_999
"""Basically, this makes sure the animation is in effect far into the past.

This is a weird hack, and I'm not thrilled about it."""

EXTRAS_INSTALLED = importlib.util.find_spec("keyed_extras") is not None
"""Whether or not `keyed-extras` is installed."""


@dataclass(frozen=True)
class QualitySetting:
    """Animation quality setting.

    Args:
        width: Width of the preview window.
        height: Height of the preview window.
    """

    width: int
    height: int

    def __post_init__(self) -> None:
        assert self.width / self.height == 16 / 9, "Not 16:9"
        assert self.width <= 1920, "Too big to fit on preview window"

    def __str__(self) -> str:
        return f"{self.width}x{self.height}"

    def __iter__(self) -> Iterator[int]:
        yield self.width
        yield self.height


class Quality(Enum):
    """Enum of animation previewer squality settings.

    Attributes:
        very_low: 1024x576 resolution (SD)
        low: 1152x648 resolution
        medium: 1280x720 resolution (720p HD)
        high: 1600x900 resolution
        very_high: 1920x1080 resolution (1080p Full HD)
    """

    very_low = QualitySetting(width=1024, height=576)
    low = QualitySetting(width=1152, height=648)
    medium = QualitySetting(width=1280, height=720)
    high = QualitySetting(width=1600, height=900)
    very_high = QualitySetting(width=1920, height=1080)
