from datetime import datetime, timedelta
import os
from job import Job
from car import (
    APPOINTMENT_DURATION_BY_CAR_TYPE,
    APPOINTMENT_REVENUE_BY_CAR_TYPE,
    CarType,
)
from schedule import Schedule
from time_utils import (
    to_csv_date,
    to_csv_date_str,
)


class Row:
    req_time: datetime
    appointment_start: datetime
    car_type: CarType

    def __init__(
        self,
        req_time: datetime,
        appointment_start: datetime,
        car_type: CarType,
    ):
        self.req_time = req_time
        self.appointment_start = appointment_start
        self.car_type = car_type

    def __str__(self) -> str:
        return f"{to_csv_date_str(self.req_time)},{to_csv_date_str(self.appointment_start)},{self.car_type.value}"


def csv_to_rows(filename: str) -> list[Row]:
    # Ensure that the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File '{filename}' does not exist.")

    rows = []
    with open(filename, "r") as f:
        for row in f.readlines():
            req_str, appointment_str, car_type = row.strip().split(",")
            rows.append(
                Row(
                    req_time=to_csv_date(req_str),
                    appointment_start=to_csv_date(appointment_str),
                    car_type=CarType(car_type),
                )
            )
    return rows


def main() -> None:
    rows = csv_to_rows("tests/cases.csv")
    # sort rows by req time
    rows.sort(key=lambda row: row.req_time)

    allowed_request_start_date = datetime(2022, 9, 1)
    allowed_appointment_start_date = datetime(2022, 10, 1)
    allowed_appointment_end_date = datetime(2022, 12, 1) - timedelta(seconds=1)
    jobs: list[Job] = []
    for row in rows:
        req_time = row.req_time
        if (
            req_time < allowed_request_start_date
            or req_time > allowed_appointment_end_date
        ):
            # Skip requests that were placed before September and after November
            print(
                f"Skipping appointment requested at {to_csv_date_str(req_time)} because the request was placed outside the allowed date range (September to November)"
            )
            continue
        appointment_start_time = row.appointment_start
        appointment_duration = APPOINTMENT_DURATION_BY_CAR_TYPE[row.car_type]
        appointment_revenue = APPOINTMENT_REVENUE_BY_CAR_TYPE[row.car_type]
        appointment_end_time = appointment_start_time + timedelta(
            minutes=appointment_duration
        )
        if req_time > appointment_start_time:
            print(
                '"Marty McFly, we won\'t be servicing the DeLorean today, come back yesterday" - Kevin McFly, 1985'
            )
            continue
        if (
            appointment_start_time < allowed_appointment_start_date
            or appointment_end_time > allowed_appointment_end_date
        ):
            # Skip appointments that are not in October and November
            print(
                f"Skipping appointment requested at {to_csv_date_str(req_time)} because its appointment start time ({to_csv_date_str(appointment_start_time)}, {to_csv_date_str(appointment_end_time)}) is outside the allowed date range (October to November)"
            )
            continue
        jobs.append(
            Job(
                req_time=req_time,
                start=appointment_start_time,
                finish=appointment_end_time,
                revenue=appointment_revenue,
                car_type=row.car_type,
            )
        )
    schedule = Schedule()
    for job in jobs:
        schedule.add_job(job)

    for day in schedule.days:
        day_of_year = day.start_time.timetuple().tm_yday
        if len(day.jobs) > 0:
            print(f"Day {day_of_year}:")
            print(day)


if __name__ == "__main__":
    main()
