"""Protocols defining interfaces for car simulation components."""

from typing import Protocol


class SuspensionModelProtocol(Protocol):
    """Protocol for suspension model components."""


class DriveTrainModelProtocol(Protocol):
    """Protocol for drivetrain model components."""

    def torque_on_axle(self, velocity: float) -> float:
        """Return torque in N·m applied on powered axle for a given velocity."""
        ...


class TyreModelProtocol(Protocol):
    """Protocol for tyre model components."""

    def lateral_force(self, slip_angle: float, normal_load: float) -> float:
        """Return lateral force in Newtons for a given slip angle and normal load."""
        ...

    def longitudinal_force(self, slip_ratio: float, normal_load: float) -> float:
        """Return longitudinal force in Newtons for a given slip ratio and normal load."""
        ...

    def force_coupling(self) -> None:
        """Method to model force coupling behavior."""
        ...


class AeroModelProtocol(Protocol):
    """Protocol for aerodynamic model components."""

    def downforce(self, speed: float) -> float:
        """Return downforce in Newtons at a given speed."""
        ...

    def drag(self, speed: float) -> float:
        """Return aerodynamic drag at a given speed."""
        ...


class ChassisProtocol(Protocol):
    """Protocol defining chassis geometry properties."""

    @property
    def wheelbase(self) -> float:
        """Wheelbase length in meters."""
        ...

    @property
    def front_track_width(self) -> float:
        """Front track width in meters."""
        ...

    @property
    def back_track_width(self) -> float:
        """Rear track width in meters."""
        ...

    @property
    def cog_height(self) -> float:
        """Center of gravity height in meters."""
        ...

    @property
    def front_weight_dist(self) -> float:
        """Fraction of weight on the front axle (0 to 1)."""
        ...


class CarModelProtocol(Protocol):
    """Protocol for a car model combining tyre, aero, and chassis models."""

    @property
    def tyre_model(self) -> TyreModelProtocol:
        """Return the tyre model component."""
        ...

    @property
    def aero_model(self) -> AeroModelProtocol:
        """Return the aerodynamic model component."""
        ...

    @property
    def geometry(self) -> ChassisProtocol:
        """Return the chassis geometry component."""
        ...

    def front_slip_angle(self, front_body_slip_angle: float, steering_angle: float) -> float:
        """Calculate front tire slip angle from body slip and steering input."""
        ...

    def back_slip_angle(self, body_slip_angle: float) -> float:
        """Calculate rear tire slip angle from body slip angle."""
        ...

    def max_speed_over_curvature(self, curvature: float) -> float:
        """Compute maximum speed achievable for a given path curvature."""
        ...
