from datetime import datetime, timedelta
import os
from bay import Bay
from job import Job
from car import (
    APPOINTMENT_DURATION_BY_CAR_TYPE,
    APPOINTMENT_REVENUE_BY_CAR_TYPE,
    CarType,
)
from schedule import Schedule, get_day_idx_of_year
from time_utils import CSV_DATE_FORMAT_STRING, date_to_unix_ts, unix_ts_to_date


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
                    req_unix_ts=date_to_unix_ts(req, CSV_DATE_FORMAT_STRING),
                    appointment_start_unix_ts=date_to_unix_ts(
                        appointment, CSV_DATE_FORMAT_STRING
                    ),
                    car_type=CarType(car_type),
                )
            )
    return rows


def main() -> None:
    rows = csv_to_rows("tests/cases.csv")
    # sort rows by req time
    rows.sort(key=lambda row: row.req_unix_ts)

    allowed_request_start_date = date_to_unix_ts(
        datetime(2022, 9, 1).strftime(CSV_DATE_FORMAT_STRING),
        CSV_DATE_FORMAT_STRING,
    )
    allowed_appointment_start_date = date_to_unix_ts(
        datetime(2022, 10, 1).strftime(CSV_DATE_FORMAT_STRING),
        CSV_DATE_FORMAT_STRING,
    )
    allowed_appointment_end_date = date_to_unix_ts(
        (datetime(2022, 11, 30) + timedelta(hours=24) - timedelta(seconds=1)).strftime(
            CSV_DATE_FORMAT_STRING
        ),
        CSV_DATE_FORMAT_STRING,
    )
    jobs: list[Job] = []
    for row in rows:
        req_time = row.req_unix_ts
        if (
            req_time < allowed_request_start_date
            or req_time > allowed_appointment_end_date
        ):
            # Skip requests that were placed before September and after November
            print(
                f"Skipping appointment requested at {unix_ts_to_date(req_time, CSV_DATE_FORMAT_STRING)} because the request was placed outside the allowed date range (September to November)"
            )
            continue
        appointment_start_time = row.appointment_start_unix_ts
        appointment_duration = APPOINTMENT_DURATION_BY_CAR_TYPE[row.car_type]
        appointment_revenue = APPOINTMENT_REVENUE_BY_CAR_TYPE[row.car_type]
        appointment_end_time = appointment_start_time + appointment_duration
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
                f"Skipping appointment requested at {unix_ts_to_date(req_time, CSV_DATE_FORMAT_STRING)} because its appointment start time ({unix_ts_to_date(appointment_start_time, CSV_DATE_FORMAT_STRING)}, {unix_ts_to_date(appointment_end_time, CSV_DATE_FORMAT_STRING)}) is outside the allowed date range (October to November)"
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
        day_of_year = get_day_idx_of_year(2022, day.start_unix_ts) + 1
        if len(day.jobs) > 0:
            print(f"Day {day_of_year}:")
            print(day)


if __name__ == "__main__":
    main()
