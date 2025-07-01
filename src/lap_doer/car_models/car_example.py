"""Example usage of aero, chassis, and tyre models."""

from aero_model import aero_example
from chassis_model import chassis_example
from tyre_model import tyre_example


def main():
    """Run example demonstrations for tyre, aero, and chassis models."""
    tyre_example()
    print()
    aero_example()
    print()
    chassis_example()


if __name__ == '__main__':
    main()
