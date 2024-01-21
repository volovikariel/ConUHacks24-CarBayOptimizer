from enum import Enum
from typing import Optional


class CarType(Enum):
    compact = "compact"
    medium = "medium"
    full_size = "full-size"
    class_1_truck = "class 1 truck"
    class_2_truck = "class 2 truck"


# Duration in minutes
APPOINTMENT_DURATION_BY_CAR_TYPE = {
    CarType.compact: 30,
    CarType.medium: 30,
    CarType.full_size: 30,
    CarType.class_1_truck: 60,
    CarType.class_2_truck: 120,
}

# Revenue in dollars
APPOINTMENT_REVENUE_BY_CAR_TYPE = {
    CarType.compact: 150,
    CarType.medium: 150,
    CarType.full_size: 150,
    CarType.class_1_truck: 250,
    CarType.class_2_truck: 700,
}


def get_min_car_value() -> Optional[int]:
    return min(APPOINTMENT_REVENUE_BY_CAR_TYPE.values())


def get_max_car_value() -> Optional[int]:
    return max(APPOINTMENT_REVENUE_BY_CAR_TYPE.values())
