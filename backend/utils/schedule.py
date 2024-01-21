# Returns the maximum revenue, as well as the selected jobs needed to maximize the revenue
from datetime import datetime
from models.day import Day
from models.job import Job
from utils.misc import get_nearest_prev_finish_time


def schedule(jobs: list[Job]) -> (int, list[Job]):
    # Order by end time
    sorted_jobs = sorted(jobs, key=lambda j: j.finish)

    max_revenue, selected_job_idxs = get_max_revenue(
        sorted_jobs, memo={}, considered_job_idx=len(sorted_jobs) - 1
    )
    return max_revenue, [sorted_jobs[job_idx] for job_idx in selected_job_idxs]


def get_max_revenue(
    jobs: list[Job],
    # ConsideredJobIdx -> (Revenue, Selected Jobs Idxs)
    memo: dict[int, (int, list[int])],
    considered_job_idx: int,
) -> tuple[int, list[int]]:
    # Assuming jobs is sorted by finish time

    # Index out of bounds
    if considered_job_idx < 0 or considered_job_idx >= len(jobs):
        return 0, []
    # we have a memo table to prevent duplicating calculations
    if considered_job_idx in memo:
        return memo[considered_job_idx]
    # We can either take a job or not
    take_job_revenue, selected_jobs_idx_taken = get_max_revenue(
        jobs,
        memo,
        get_nearest_prev_finish_time(
            [(job.start, job.finish) for job in jobs], considered_job_idx
        ),
    )
    take_job_revenue += jobs[considered_job_idx].revenue
    if jobs[considered_job_idx].treat_as_inf:
        take_job_revenue = float("inf")
        memo[considered_job_idx] = (
            take_job_revenue,
            selected_jobs_idx_taken + [considered_job_idx],
        )
        return memo[considered_job_idx]
    skip_job_revenue, selected_jobs_idx_skipped = get_max_revenue(
        jobs, memo, considered_job_idx - 1
    )

    # NOTE: Tiebreakers shouldn't matter?
    if take_job_revenue >= skip_job_revenue:
        memo[considered_job_idx] = (
            take_job_revenue,
            selected_jobs_idx_taken + [considered_job_idx],
        )
    else:
        memo[considered_job_idx] = (
            skip_job_revenue,
            selected_jobs_idx_skipped,
        )

    return memo[considered_job_idx]


def get_revenue_up_to(days: list[Day], max_day: datetime) -> int:
    total = 0
    for d in days:
        if d.start_time < max_day:
            # The days are 1 indexed, so subtract 1
            day_idx = d.start_time.timetuple().tm_yday - 1
            total += days[day_idx].get_total_bays_revenue(
                datetime(2022, 1, 1),
                max_day.replace(hour=7 + 12, minute=0, second=0),
            )
    return total


def get_total_turned_away_revenue_up_to(
    self, days: list[Day], max_day: datetime
) -> int:
    total = 0
    for d in days:
        if d.start_time < max_day:
            # The days are 1 indexed, so subtract 1
            day_idx = d.start_time.timetuple().tm_yday - 1
            total += days[day_idx].get_total_turned_away_revenue(
                datetime(2022, 1, 1),
                max_day.replace(hour=7 + 12, minute=0, second=0),
            )
    return total
