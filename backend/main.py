import os

from car import (
    APPOINTMENT_DURATION_BY_CAR_TYPE,
    APPOINTMENT_REVENUE_BY_CAR_TYPE,
    CarType,
)
from time_utils import date_to_unix_ts


class Row:
    req_unix_ts: int
    appointment_start_unix_ts: int
    car_type: CarType

    def __init__(
        self,
        req_unix_ts: int,
        appointment_start_unix_ts: int,
        car_type: CarType,
    ):
        self.req_unix_ts = req_unix_ts
        self.appointment_start_unix_ts = appointment_start_unix_ts
        self.car_type = car_type

    def __str__(self) -> str:
        return f"{self.req_unix_ts},{self.appointment_start_unix_ts},{self.car_type}"


def csv_to_rows(filename: str) -> list[Row]:
    # Ensure that the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File '{filename}' does not exist.")

    rows = []
    with open(filename, "r") as f:
        for row in f.readlines():
            req, appointment, car_type = row.strip().split(",")
            rows.append(
                Row(
                    req_unix_ts=date_to_unix_ts(req),
                    appointment_start_unix_ts=date_to_unix_ts(appointment),
                    car_type=CarType(car_type),
                )
            )
    return rows


def main() -> None:
    rows = csv_to_rows("tests/cases.csv")
    # sort rows by req time
    rows.sort(key=lambda row: row.req_unix_ts)

    for row in rows:
        req_time = row.req_unix_ts
        appointment_start_time = row.appointment_start_unix_ts
        appointment_duration = APPOINTMENT_DURATION_BY_CAR_TYPE[row.car_type]
        appointment_end_time = appointment_start_time + appointment_duration
        appointment_revenue = APPOINTMENT_REVENUE_BY_CAR_TYPE[row.car_type]
        print(
            f"{req_time=} {appointment_start_time=} {appointment_end_time=} {appointment_revenue=}"
        )


if __name__ == "__main__":
    main()
