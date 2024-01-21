from datetime import datetime
from models.car import CarType
from utils.time import CSV_DATE_FORMAT_STRING


class Job:
    def __init__(
        self,
        req_time: datetime,
        start: datetime,
        finish: datetime,
        revenue: int,
        car_type: CarType,
    ):
        self.start = start
        self.finish = finish
        self.revenue = revenue
        self.car_type = car_type
        self.req_time = req_time

    def __str__(self) -> str:
        req_time_str = self.req_time.strftime(CSV_DATE_FORMAT_STRING)
        start_time_str = self.start.strftime(CSV_DATE_FORMAT_STRING)
        end_time_str = self.finish.strftime(CSV_DATE_FORMAT_STRING)
        job = f"{self.car_type.value} req@{req_time_str} appointment[{start_time_str},{end_time_str}]; Revenue: ${self.revenue}"
        return job


# The main function that returns the maximum possible
# revenue from the given array of jobs
def schedule(jobs: list[Job]):
    # Sort jobs according to finish time
    # NOTE: May be able to sort once before calling schedule, instead of sorting each time
    jobs = sorted(jobs, key=lambda j: j.finish)
    # Create an array to store solutions of subproblems. table[i]
    # stores the revenue for jobs till arr[i] (including arr[i])
    num_jobs = len(jobs)
    table = [{"revenue": 0, "selected_jobs": []} for _ in range(num_jobs)]

    table[0]["revenue"] = jobs[0].revenue
    table[0]["selected_jobs"].append(jobs[0])

    # Fill entries in table[] using recursive property
    for i in range(1, num_jobs):
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

    return table[num_jobs - 1]["revenue"], table[num_jobs - 1]["selected_jobs"]


def binarySearch(jobs: list[Job], start_index: int):
    # Initialize 'lo' and 'hi' for Binary Search
    lo = 0
    hi = start_index - 1

    # Perform binary Search iteratively
    while lo <= hi:
        mid = (lo + hi) // 2
        if jobs[mid].finish <= jobs[start_index].start:
            if jobs[mid + 1].finish <= jobs[start_index].start:
                lo = mid + 1
            else:
                return mid
        else:
            hi = mid - 1
    return -1
