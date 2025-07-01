"""Classes for modeling car."""

import math

from car_protocol import AeroModelProtocol
from car_protocol import ChassisProtocol
from car_protocol import TyreModelProtocol


class CarModel:
    """Model representing a car combining tyres, aerodynamics, and chassis geometry."""

    def __init__(self, tyre_model: TyreModelProtocol, aero_model: AeroModelProtocol, geometry: ChassisProtocol):
        """Initialize car model with tyres, aero, and chassis components."""
        self._tyre_model = tyre_model
        self._aero_model = aero_model
        self._geometry = geometry

    @property
    def tyre_model(self) -> TyreModelProtocol:
        """Return the tyre model."""
        return self._tyre_model

    @property
    def aero_model(self) -> AeroModelProtocol:
        """Return the aero model."""
        return self._aero_model

    @property
    def geometry(self) -> ChassisProtocol:
        """Return the chassis model."""
        return self._geometry

    def required_lateral_force(self, speed: float, curvature: float) -> float:
        """Compute lateral force needed to follow a curvature at specified speed.

        Args:
            speed: vehicle speed in m/s.
            curvature: path curvature in 1/m.

        Returns:
            Required lateral force in Newtons.
        """
        return self.mass * speed**2 * curvature

    def body_slip_angle(self, lateral_velocity: float, longitudinal_velocity: float) -> float:
        """Calculate slip angle of the car body at its center of gravity.

        Args:
            lateral_velocity: lateral velocity in m/s.
            longitudinal_velocity: longitudinal velocity in m/s.

        Returns:
            Body slip angle in radians.
        """
        return math.atan2(lateral_velocity, longitudinal_velocity)

    def front_body_slip_angle(self, body_slip: float, curvature: float) -> float:
        """Compute slip angle at the front axle body location.

        Args:
            body_slip: slip angle at center of gravity in radians.
            curvature: path curvature in 1/m.

        Returns:
            Front body slip angle in radians.
        """
        a = self.geometry.wheelbase * self.geometry.front_weight_dist
        return body_slip + a * curvature

    def back_body_slip_angle(self, body_slip: float, curvature: float) -> float:
        """Compute slip angle at the rear axle body location.

        Args:
            body_slip: slip angle at center of gravity in radians.
            curvature: path curvature in 1/m.

        Returns:
            Rear body slip angle in radians.
        """
        b = self.geometry.wheelbase * (1 - self.geometry.front_weight_dist)
        return body_slip - b * curvature

    def front_slip_angle(self, front_body_slip: float, steering_angle: float) -> float:
        """Calculate front tire slip angle.

        Args:
            front_body_slip: front body slip angle in radians.
            steering_angle: steering input angle in radians.

        Returns:
            Front slip angle in radians.
        """
        return front_body_slip - steering_angle

    def back_slip_angle(self, back_body_slip: float) -> float:
        """Calculate rear tire slip angle.

        Args:
            back_body_slip: rear body slip angle in radians.

        Returns:
            Rear slip angle in radians.
        """
        return back_body_slip

    def steering_angle(self, front_slip: float, curvature: float, back_slip: float) -> float:
        """Calculate steering angle required to achieve the desired slip angles and curvature.

        Args:
            front_slip: front tire slip angle in radians.
            curvature: path curvature in 1/m.
            back_slip: rear tire slip angle in radians.

        Returns:
            Steering angle in radians.
        """
        return front_slip + curvature * self.geometry.wheelbase - back_slip

    def max_speed_over_curvature(self, curvature: float) -> float:
        """Compute the maximum speed for a given curvature.

        Args:
            curvature: path curvature in 1/m.

        Returns:
            Maximum achievable speed in m/s.
        """
