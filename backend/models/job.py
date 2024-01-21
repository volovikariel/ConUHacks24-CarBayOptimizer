from datetime import datetime
from models.car import CarType
from utils.csv import CSV_DATE_FORMAT_STRING
from utils.misc import binarySearch


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


# Returns the maximum revenue, as well as the selected jobs needed to maximize the revenue
def schedule(jobs: list[Job]) -> (int, list[Job]):
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
        l = binarySearch([(job.start, job.finish) for job in jobs], i)
        if l != -1:
            inclProf += table[l]["revenue"]

        # Store maximum of including and excluding
        if inclProf > table[i - 1]["revenue"]:
            table[i]["revenue"] = inclProf
            table[i]["selected_jobs"] = table[l]["selected_jobs"] + [jobs[i]]
        else:
            table[i] = table[i - 1]

    return table[num_jobs - 1]["revenue"], table[num_jobs - 1]["selected_jobs"]
