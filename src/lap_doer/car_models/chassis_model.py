"""Classes for modeling chassis."""


class GenericChassis:
    """Class representing geometry of the car."""

    def __init__(self, wheelbase: float, front_track_width: float, back_track_width: float, cog_height: float, front_weight_dist: float, mass: float):
        """Initialize chassis geometry and mass distribution parameters."""
        self.__wheelbase = wheelbase
        self.__front_track_width = front_track_width
        self.__back_track_width = back_track_width
        self.__cog_height = cog_height
        self.__front_weight_dist = front_weight_dist
        self.__mass = mass

    @property
    def wheelbase(self) -> float:
        """Wheelbase of the car (distance between front and rear axles)."""
        return self.__wheelbase

    @property
    def mass(self) -> float:
        """Wheelbase of the car (distance between front and rear axles)."""
        return self.__mass

    @property
    def front_track_width(self) -> float:
        """Track width of the car (distance between left and right wheels)."""
        return self.__front_track_width

    @property
    def back_track_width(self) -> float:
        """Track width of the car (distance between left and right wheels)."""
        return self.__back_track_width

    @property
    def cog_height(self) -> float:
        """Height of the center of gravity (COG)."""
        return self.__cog_height

    @property
    def front_weight_dist(self) -> float:
        """Fraction of the total weight on the front axle (0 to 1)."""
        return self.__front_weight_dist

    def static_lateral_load_transfer(self, total_mass: float, lateral_accel: float) -> dict:
        """Estimate static lateral load transfer at front and rear axles.

        Args:
            total_mass: total mass of the car (kg)
            lateral_accel: lateral acceleration (m/s^2)

        Returns:
            dict: load transfer at front and rear axles (N)
        """
        front_load_transfer_total = total_mass * lateral_accel * self.cog_height / self.front_track_width
        back_load_transfer_total = total_mass * lateral_accel * self.cog_height / self.back_track_width

        front_transfer = front_load_transfer_total * self.front_weight_dist
        rear_transfer = back_load_transfer_total * (1 - self.front_weight_dist)

        return {'front_transfer_N': front_transfer, 'rear_transfer_N': rear_transfer}

    def static_longitudinal_load_transfer(self, total_mass: float, longitudinal_accel: float) -> dict:
        """Estimate static longitudinal load transfer during acceleration or braking.

        Args:
            total_mass: total mass of the car (kg)
            longitudinal_accel: longitudinal acceleration (m/s^2).
                Positive for acceleration, negative for braking.

        Returns:
            dict: load transfer (N) to front and rear
        """
        load_transfer = total_mass * longitudinal_accel * self.cog_height / self.wheelbase

        front_transfer = -load_transfer
        rear_transfer = load_transfer

        return {'front_transfer_N': front_transfer, 'rear_transfer_N': rear_transfer}


def chassis_example():
    """Example usage of the GenericChassisi demonstrating load transfer calculations."""
    print('CHASSIS EXAMPLE')

    mass_par = 280
    wheelbase_par = 1.53
    front_track_width_par = 1.25  # do sprawdzenia
    back_track_width_par = 1.21  # do sprawdzenia
    cog_height_par = 0.33
    front_weight_dist_par = 0.45  # do sprawdzenia

    geometry = GenericChassis(
        wheelbase=wheelbase_par,
        front_track_width=front_track_width_par,
        back_track_width=back_track_width_par,
        cog_height=cog_height_par,
        front_weight_dist=front_weight_dist_par,
        mass=mass_par,
    )

    longitudinal_accel = 1.5 * 9.81
    lateral_accel = 2 * 9.81

    result = geometry.static_lateral_load_transfer(mass_par, lateral_accel)
    print(f'Lateral acceleration {lateral_accel} [m/s/s]')
    print(f'Front lateral load transfer: {result["front_transfer_N"]:.1f} N')
    print(f'Rear lateral load transfer: {result["rear_transfer_N"]:.1f} N')
    print()
    result_long = geometry.static_longitudinal_load_transfer(mass_par, longitudinal_accel)
    print(f'Longitudinal acceleration {longitudinal_accel} [m/s/s]')
    print(f'Front longitudinal load transfer: {result_long["front_transfer_N"]:.1f} N')
    print(f'Rear longitudinal load transfer: {result_long["rear_transfer_N"]:.1f} N')
