from dataclasses import dataclass


@dataclass
class Direction:
    """
    Stores angles in degrees.
    """
    water: float = None
    food: float = None
    monster: float = None
