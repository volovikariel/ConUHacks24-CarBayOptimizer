from datetime import datetime, timedelta
import os
from models.job import Job
from models.car import (
    APPOINTMENT_DURATION_BY_CAR_TYPE,
    APPOINTMENT_REVENUE_BY_CAR_TYPE,
)
from models.schedule import Schedule
from utils.csv import (
    csv_to_rows,
    to_csv_date_str,
)

MIN_ALLOWED_REQUEST_START_DATE = datetime(2022, 9, 1)
ALLOWED_APPOINTMENT_START_DATE = datetime(2022, 10, 1)
MAX_ALLOWED_APPOINTMENT_END_DATE = datetime(2022, 12, 1) - timedelta(seconds=1)


def main() -> None:
    rows = csv_to_rows("tests/cases.csv")
    # sort rows by req time
    rows.sort(key=lambda row: row.req_time)

    jobs: list[Job] = []
    for row in rows:
        req_time = row.req_time
        if (
            req_time < MIN_ALLOWED_REQUEST_START_DATE
            or req_time > MAX_ALLOWED_APPOINTMENT_END_DATE
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
            appointment_start_time < ALLOWED_APPOINTMENT_START_DATE
            or appointment_end_time > MAX_ALLOWED_APPOINTMENT_END_DATE
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
