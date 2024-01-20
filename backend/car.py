from enum import Enum
from time_utils import minutes_to_seconds


class CarType(Enum):
    compact = "compact"
    medium = "medium"
    full_size = "full-size"
    class_1_truck = "class 1 truck"
    class_2_truck = "class 2 truck"


APPOINTMENT_DURATION_BY_CAR_TYPE = {
    CarType.compact: minutes_to_seconds(30),
    CarType.medium: minutes_to_seconds(30),
    CarType.full_size: minutes_to_seconds(30),
    CarType.class_1_truck: minutes_to_seconds(60),
    CarType.class_2_truck: minutes_to_seconds(120),
}

APPOINTMENT_REVENUE_BY_CAR_TYPE = {
    CarType.compact: 150,
    CarType.medium: 150,
    CarType.full_size: 150,
    CarType.class_1_truck: 250,
    CarType.class_2_truck: 700,
}
