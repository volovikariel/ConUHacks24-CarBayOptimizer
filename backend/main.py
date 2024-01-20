import os
from job import Job
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

    jobs = []
    for row in rows:
        req_time = row.req_unix_ts
        appointment_start_time = row.appointment_start_unix_ts
        appointment_duration = APPOINTMENT_DURATION_BY_CAR_TYPE[row.car_type]
        appointment_end_time = appointment_start_time + appointment_duration
        appointment_revenue = APPOINTMENT_REVENUE_BY_CAR_TYPE[row.car_type]
        jobs.append(
            Job(
                start=appointment_start_time,
                finish=appointment_end_time,
                revenue=appointment_revenue,
                type=row.car_type,
            )
        )
        print(
            f"{req_time=} {appointment_start_time=} {appointment_end_time=} {appointment_revenue=}"
        )

    max_revenue, selected_jobs = schedule(jobs)
    print(max_revenue)
    for job in selected_jobs:
        print(job)


# The main function that returns the maximum possible
# revenue from the given array of jobs
def schedule(jobs: list[Job]):
    # Sort jobs according to finish time
    jobs = sorted(jobs, key=lambda j: j.finish)

    # Create an array to store solutions of subproblems. table[i]
    # stores the revenue for jobs till arr[i] (including arr[i])
    n = len(jobs)
    table = [{"revenue": 0, "selected_jobs": []} for _ in range(n)]

    table[0]["revenue"] = jobs[0].revenue
    table[0]["selected_jobs"].append(jobs[0])

    # Fill entries in table[] using recursive property
    for i in range(1, n):
        # Find revenue including the current job
        inclProf = jobs[i].revenue
        l = binarySearch(jobs, i)
        if l != -1:
            inclProf += table[l]["revenue"]

        # Store maximum of including and excluding
        if inclProf > table[i - 1]["revenue"]:
            table[i]["revenue"] = inclProf
            table[i]["selected_jobs"] = table[l]["selected_jobs"] + [jobs[i]]
        else:
            table[i] = table[i - 1]

    return table[n - 1]["revenue"], table[n - 1]["selected_jobs"]


def binarySearch(job, start_index):
    # Initialize 'lo' and 'hi' for Binary Search
    lo = 0
    hi = start_index - 1

    # Perform binary Search iteratively
    while lo <= hi:
        mid = (lo + hi) // 2
        if job[mid].finish <= job[start_index].start:
            if job[mid + 1].finish <= job[start_index].start:
                lo = mid + 1
            else:
                return mid
        else:
            hi = mid - 1
    return -1


if __name__ == "__main__":
    main()
