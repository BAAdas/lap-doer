"""Classes for modeling aero."""

from typing import Callable


class GenericAeroModel:
    """Class representing a generic aerodynamic model with customizable functions.

    Allows user-defined functions for calculating downforce and drag forces
    based on speed and optionally air density.
    """

    def __init__(self, downforce_func: Callable[[float], float], drag_func: Callable[[float], float]):
        """Initialize with custom functions for downforce and drag.

        Args:
            downforce_func: A function that takes speed (float) and air density (float),
                and returns downforce (float, N).
            drag_func: A function that takes speed (float) and air density (float),
                and returns drag (float, N).
        """
        self._downforce_func = downforce_func
        self._drag_func = drag_func

    def downforce(self, speed: float, rho: float = 1.25) -> float:
        """Calculate and return downforce at a given speed and air density.

        Args:
            speed: Vehicle speed in meters per second.
            rho: Air density in kg/m³ (default is 1.25).

        Returns:
            Downforce in Newtons (N).
        """
        return self._downforce_func(speed, rho)

    def drag(self, speed: float, rho: float = 1.25) -> float:
        """Calculate and return drag at a given speed and air density.

        Args:
            speed: Vehicle speed in meters per second.
            rho: Air density in kg/m³ (default is 1.25).

        Returns:
            Drag force in Newtons (N).
        """
        return self._drag_func(speed, rho)


def aero_example():
    """Example demonstrating the usage of GenericAeroModel.

    Defines simple linear aerodynamic force functions, creates an aero model,
    computes downforce and drag at a sample velocity, and prints the results.
    """
    print('AERO EXAMPLE')

    def negative_lift_func(velocity: float, rho: float, cla: float = 4.3) -> float:
        return 0.5 * rho * cla * velocity**2

    def drag_func(velocity: float, rho: float, cda: float = 1.7) -> float:
        return 0.5 * rho * cda * velocity**2

    aero = GenericAeroModel(
        downforce_func=negative_lift_func,
        drag_func=drag_func,
    )

    velocity = 12

    # Compute forces
    downforce = aero.downforce(velocity)
    drag = aero.drag(velocity)

    # Show results
    print(f'Given velocity {velocity} v[m/s]')
    print(f'Downforce at that velocity {downforce} N')
    print(f'Drag at that velocity {drag} N')
