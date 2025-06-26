from typing import Protocol


class TyreModelProtocol(Protocol):
    def lateral_force(self, slip_angle: float, normal_load: float) -> float:
        """Return lateral force in N for a given slip angle and normal load"""
        ...

    def longitudinal_force(self, slip_ratio: float, normal_load: float) -> float:
        """Return longitudinal force in N for a given slip ratio and normal load"""
        ...

    def force_coupling(self): ...


class AeroModelProtocol(Protocol):
    def downforce(self, speed: float) -> float:
        """Return downforce (N) at a given speed"""
        ...

    def drag(self, speed: float) -> float:
        """Return drag at a given speed"""
        ...


class CarGeometryProtocol(Protocol):
    @property
    def wheelbase(self) -> float: ...

    @property
    def track_width(self) -> float: ...

    @property
    def cog_height(self) -> float: ...

    @property
    def front_weight_dist(self) -> float: ...


class CarModelProtocol(Protocol):
    @property
    def mass(self) -> float:
        """Return car mass in kg"""
        ...

    @property
    def tyre_model(self) -> TyreModelProtocol: ...

    @property
    def aero_model(self) -> AeroModelProtocol: ...

    @property
    def geometry(self) -> CarGeometryProtocol: ...

    def front_slip_angle(self, front_body_slip_angle: float, stearing_angle: float) -> float: ...

    def back_slip_angle(slef, body_slip_angle: float) -> float: ...

    def max_speed_over_curvature(self, curvature: float) -> float: ...
