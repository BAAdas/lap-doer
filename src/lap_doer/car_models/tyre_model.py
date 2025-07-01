"""Classes for modeling tyres."""

import math
from typing import Callable


class GenericTyreModel:
    """Tyre model with user-defined force functions and customizable coupling."""

    def __init__(
        self,
        lateral_force_func: Callable[[float, float], float],
        longitudinal_force_func: Callable[[float, float], float],
        coupling_func: Callable[[float, float, float], float],
    ):
        """Initialize the tyre model with force and coupling functions.

        Args:
            lateral_force_func: (slip_angle, normal_load) → lateral force (N).
            longitudinal_force_func: (slip_ratio, normal_load) → longitudinal force (N).
            coupling_func: (given_force, normal_load) → remaining other force (N).
        """
        self._lateral_force_func = lateral_force_func
        self._longitudinal_force_func = longitudinal_force_func
        self._coupling_func = coupling_func

    def lateral_force(self, slip_angle: float, normal_load: float) -> float:
        """Compute lateral force (N)."""
        return self._lateral_force_func(slip_angle, normal_load)

    def longitudinal_force(self, slip_ratio: float, normal_load: float) -> float:
        """Compute longitudinal force (N)."""
        return self._longitudinal_force_func(slip_ratio, normal_load)

    def force_coupling(self, given_force: float, normal_load: float) -> float:
        """Compute remaining allowable force (N) using custom coupling function.

        Args:
            given_force: Force that has already been applied (N)
            normal_load: Normal load (N)

        Returns:
            Remaining force (N)
        """
        return self._coupling_func(given_force, normal_load)


def tyre_example():
    """Example usage of the GenericTyreModel demonstrating force calculations."""
    print('TYRE EXAMPLE')
    # Define basic linear lateral and longitudinal force functions

    def lat_func(slip_angle: float, normal_load: float) -> float:
        return 10.0 * normal_load * slip_angle

    def long_func(slip_ratio: float, normal_load: float) -> float:
        return 12.0 * normal_load * slip_ratio

    def ellipse_coupling(given_force: float, normal_load: float) -> float:
        if abs(given_force) <= normal_load:
            return max(0.0, math.sqrt(normal_load**2 - given_force**2))
        return 0.0

    # Create tyre model
    tyre = GenericTyreModel(
        lateral_force_func=lat_func,
        longitudinal_force_func=long_func,
        coupling_func=ellipse_coupling,
    )

    # Example conditions
    normal_load = 3000  # N
    slip_angle = 0.05  # rad
    slip_ratio = 0.1  # dimensionless

    # Compute forces
    lat_force = tyre.lateral_force(slip_angle, normal_load)
    long_force = tyre.longitudinal_force(slip_ratio, normal_load)

    # Compute remaining capacity for lateral force after longitudinal force applied
    remaining_lat = tyre.force_coupling(long_force, normal_load)

    # Compute remaining capacity for longitudinal force after lateral force applied
    remaining_long = tyre.force_coupling(lat_force, normal_load)

    # Show results
    print(f'Normal load: {normal_load} N')
    print(f'Slip angle: {slip_angle} rad → Lateral force: {lat_force:.1f} N')
    print(f'Slip ratio: {slip_ratio} → Longitudinal force: {long_force:.1f} N')
    print(f'Remaining lateral force capacity after {long_force:.1f} N long. force: {remaining_lat:.1f} N')
    print(f'Remaining longitudinal force capacity after {lat_force:.1f} N lat. force: {remaining_long:.1f} N')
