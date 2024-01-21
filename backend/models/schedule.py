from datetime import datetime, timedelta
from models.day import Day
from models.job import Job
from utils.misc import binary_search


class Schedule:
    def __init__(self):
        self.days: list[Day] = []

        # Initializing only the year 2022 for simplicity
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 12, 31)
        current_date = start_date
        while current_date <= end_date:
            self.days.append(
                Day(
                    start_time=current_date + timedelta(hours=7),  # 7am
                    end_time=current_date + timedelta(hours=7 + 12),  # 7pm
                )
            )
            current_date += timedelta(days=1)

    def add_job(self, job: Job) -> None:
        # The days are 1 indexed, so subtract 1
        day_idx = job.start.timetuple().tm_yday - 1
        # Make sure the jobs are within the day's working hours (7am to 7pm)
        if (
            job.start < self.days[day_idx].start_time
            or job.finish > self.days[day_idx].end_time
        ):
            return
        # It's a walk-in
        if job.req_time == job.start:
            self.days[day_idx].handle_walk_in_job(job)
        # The reservation date is the same as the job's date (but it's not a walk-in)
        elif job.req_time.timetuple().tm_yday == job.start.timetuple().tm_yday:
            self.days[day_idx].handle_same_day_reserved_job(job)
        else:
            self.days[day_idx].handle_reserved_job(job)


# Returns the maximum revenue, as well as the selected jobs needed to maximize the revenue
# TODO: Verify that this is correct...and understand what the heck it is doing
# TODO: Probably rewrite this...
def schedule(jobs: list[Job]) -> (int, list[Job]):
    # NOTE: May be able to sort once before calling schedule, instead of sorting each time
    jobs = sorted(jobs, key=lambda j: j.finish)
    # Create an array to store solutions of subproblems. table[i]
    # stores the revenue for jobs till arr[i] (including arr[i])
    num_jobs = len(jobs)
    table = [
        {"revenue": 0, "selected_jobs": [], "treat_as_inf": False}
        for _ in range(num_jobs)
    ]

    table[0]["revenue"] = jobs[0].revenue
    if jobs[0].treat_as_inf is True:
        table[0]["revenue"] = float("inf")
    table[0]["selected_jobs"].append(jobs[0])

    # Fill entries in table[] using recursive property
    for i in range(1, num_jobs):
        # Find revenue including the current job
        inclProf = jobs[i].revenue
        if jobs[i].treat_as_inf is True:
            inclProf = float("inf")
        l = binary_search([(job.start, job.finish) for job in jobs], i)
        if l != -1:
            inclProf += table[l]["revenue"]

        # Store maximum of including and excluding
        if inclProf > table[i - 1]["revenue"]:
            table[i]["revenue"] = inclProf
            table[i]["selected_jobs"] = table[l]["selected_jobs"] + [jobs[i]]
        else:
            table[i] = table[i - 1]

    return table[num_jobs - 1]["revenue"], table[num_jobs - 1]["selected_jobs"]
