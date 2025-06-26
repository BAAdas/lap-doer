import math
from typing import Callable

from car_protocol import *


class GenericCarGeometry:
    """Class representing geometry of the car"""

    def __init__(self, wheelbase: float, track_width: float, cog_height: float, front_weight_dist: float):
        self.__wheelbase = wheelbase
        self.__track_width = track_width
        self.__cog_height = cog_height
        self.__front_weight_dist = front_weight_dist

    @property
    def wheelbase(self) -> float:
        """Wheelbase of the car (distance between front and rear axles)"""
        return self.__wheelbase

    @property
    def track_width(self) -> float:
        """Track width of the car (distance between left and right wheels)"""
        return self.__track_width

    @property
    def cog_height(self) -> float:
        """Height of the center of gravity (COG)"""
        return self.__cog_height

    @property
    def front_weight_dist(self) -> float:
        """Fraction of the total weight on the front axle (0 to 1)"""
        return self.__front_weight_dist

    def static_lateral_load_transfer(self, total_mass: float, lateral_accel: float) -> dict:
        """Estimate static lateral load transfer at front and rear axles during cornering.

        Args:
            total_mass: total mass of the car (kg)
            lateral_accel: lateral acceleration (m/s^2)

        Returns:
            dict: load transfer at front and rear axles (N)
        """
        g = 9.81  # gravity
        total_weight = total_mass * g
        load_transfer_total = total_mass * lateral_accel * self.cog_height / self.track_width

        front_transfer = load_transfer_total * self.front_weight_dist
        rear_transfer = load_transfer_total * (1 - self.front_weight_dist)

        return {'front_transfer_N': front_transfer, 'rear_transfer_N': rear_transfer}

    def static_longitudinal_load_transfer(self, total_mass: float, longitudinal_accel: float) -> dict:
        """Estimate static longitudinal load transfer during acceleration or braking.

        Args:
            total_mass: total mass of the car (kg)
            longitudinal_accel: longitudinal acceleration (m/s^2), + for accel, - for braking

        Returns:
            dict: load transfer (N) to front and rear
        """
        g = 9.81  # gravity
        total_weight = total_mass * g
        load_transfer = total_mass * longitudinal_accel * self.cog_height / self.wheelbase

        front_transfer = load_transfer  # positive accel shifts weight rearward, so front loses load
        rear_transfer = -load_transfer

        return {'front_transfer_N': front_transfer, 'rear_transfer_N': rear_transfer}


class CarModel:
    def __init__(self, mass: float, tyre_model: TyreModelProtocol, aero_model: AeroModelProtocol, geometry: CarGeometryProtocol):
        self._mass = mass
        self._tyre_model = tyre_model
        self._aero_model = aero_model
        self._geometry = geometry

    @property
    def mass(self) -> float:
        """Return car mass in kg"""
        return self._mass

    @property
    def tyre_model(self) -> TyreModelProtocol:
        return self._tyre_model

    @property
    def aero_model(self) -> AeroModelProtocol:
        return self._aero_model

    @property
    def geometry(self) -> CarGeometryProtocol:
        return self._geometry

    def required_lateral_force(self, speed: float, curvature: float) -> float:
        """Compute lateral force needed to follow curvature at speed"""
        return self.mass * speed**2 * curvature

    def body_slip_angle(self, lateral_velocity: float, longitudinal_velocity: float) -> float:
        """Compute body slip angle at CG"""
        return math.atan2(lateral_velocity, longitudinal_velocity)

    def front_body_slip_angle(self, body_slip: float, curvature: float) -> float:
        """Compute front body slip angle"""
        a = self.geometry.wheelbase * self.geometry.front_weight_dist
        return body_slip + a * curvature

    def back_body_slip_angle(self, body_slip: float, curvature: float) -> float:
        """Compute rear body slip angle"""
        b = self.geometry.wheelbase * (1 - self.geometry.front_weight_dist)
        return body_slip - b * curvature

    def front_slip_angle(self, front_body_slip: float, steering_angle: float) -> float:
        return front_body_slip - steering_angle

    def back_slip_angle(self, back_body_slip: float) -> float:
        return back_body_slip

    def steering_angle(self, front_slip: float, curvature: float, back_slip: float) -> float:
        """Compute steering angle required"""
        return front_slip + curvature * self.geometry.wheelbase - back_slip

    def max_speed_over_curvature(self, curvature: float) -> float: ...


def geometry_example():
    print('GEOMETRY EXAMPLE')

    wheelbase_par = 2.5
    track_width_par = 1.2
    cog_height_par = 0.4
    front_weight_dist_par = 0.3

    geometry = GenericCarGeometry(
        wheelbase=wheelbase_par,
        track_width=track_width_par,
        cog_height=cog_height_par,
        front_weight_dist=front_weight_dist_par,
    )

    result = geometry.static_lateral_load_transfer(total_mass=1200, lateral_accel=5.0)
    print(f'Front load transfer: {result["front_transfer_N"]:.1f} N')
    print(f'Rear load transfer: {result["rear_transfer_N"]:.1f} N')
    print()
    result_long = geometry.static_longitudinal_load_transfer(total_mass=1200, longitudinal_accel=3.0)
    print(f'Front load transfer: {result_long["front_transfer_N"]:.1f} N')
    print(f'Rear load transfer: {result_long["rear_transfer_N"]:.1f} N')
