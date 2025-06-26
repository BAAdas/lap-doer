import math
from typing import Callable

from car_protocol import *


class GenericAeroModel:
    """Class representing generic aerodynamic model with customizable functions."""

    def __init__(self, downforce_func: Callable[[float], float], drag_func: Callable[[float], float]):
        """Initialize with custom functions for downforce and drag.

        Args:
            downforce_func: A function that takes speed (float) and returns downforce (float, N).
            drag_func: A function that takes speed (float) and returns drag (float, N).
        """
        self._downforce_func = downforce_func
        self._drag_func = drag_func

    def downforce(self, speed: float) -> float:
        """Return downforce (N) at a given speed."""
        return self._downforce_func(speed)

    def drag(self, speed: float) -> float:
        """Return drag (N) at a given speed."""
        return self._drag_func(speed)


def aero_example():
    print('AERO EXAMPLE')
    # Define basic linear lateral and longitudinal force functions
    negative_lift_func = lambda velocity: 0.15 * velocity + 0.1 * velocity**2
    drag_func = lambda velocity: 0.3 * velocity**2

    aero = GenericAeroModel(
        downforce_func=negative_lift_func,
        drag_func=drag_func,
    )

    velocity = 15

    # Compute forces
    downforce = aero.downforce(velocity)
    drag = aero.drag(velocity)

    # Show results
    print(f'Given velocity {velocity} v[m/s]')
    print(f'Downforce at that velocity {downforce} N')
    print(f'Drag at that velocity {drag} N')
