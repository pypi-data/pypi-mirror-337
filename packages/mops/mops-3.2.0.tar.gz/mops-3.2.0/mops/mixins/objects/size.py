import typing
from dataclasses import dataclass


@dataclass
class Size:
    """ Represents the dimensions of an object with width and height. """

    width: typing.Union[int, float, None] = None
    height: typing.Union[int, float, None] = None
