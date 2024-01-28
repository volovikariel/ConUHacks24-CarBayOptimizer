# Returns the maximum revenue, as well as the selected jobs needed to maximize the revenue
from models.job import Job
from utils.misc import get_nearest_prev_finish_time


def schedule(jobs: list[Job]) -> (int, list[Job]):
    # Order by end time
    sorted_jobs = sorted(jobs, key=lambda j: j.finish)

    max_revenue, selected_job_idxs = get_max_revenue(
        sorted_jobs, considered_job_idx=len(sorted_jobs) - 1
    )
    return max_revenue, [sorted_jobs[job_idx] for job_idx in selected_job_idxs]


def get_max_revenue(
    jobs: list[Job],
    considered_job_idx: int,
) -> tuple[int, list[int]]:
    memo: dict[int, tuple[int, list[int]]] = {}

    def get_max_revenue_helper(
        jobs: list[Job], considered_job_idx: int
    ) -> tuple[int, list[int]]:
        # Assuming jobs is sorted by finish time
        if considered_job_idx in memo:
            return memo[considered_job_idx]

        # Index out of bounds
        if considered_job_idx < 0 or considered_job_idx >= len(jobs):
            return 0, []
        # We can either take a job or not
        take_job_revenue, selected_jobs_idx_taken = get_max_revenue_helper(
            jobs,
            get_nearest_prev_finish_time(
                [(job.start, job.finish) for job in jobs], considered_job_idx
            ),
        )
        take_job_revenue += jobs[considered_job_idx].revenue
        if jobs[considered_job_idx].treat_as_inf:
            take_job_revenue = float("inf")
            result = (
                take_job_revenue,
                selected_jobs_idx_taken + [considered_job_idx],
            )
        else:
            skip_job_revenue, selected_jobs_idx_skipped = get_max_revenue_helper(
                jobs, considered_job_idx - 1
            )

            # NOTE: Tiebreakers shouldn't matter?
            if take_job_revenue >= skip_job_revenue:
                result = (
                    take_job_revenue,
                    selected_jobs_idx_taken + [considered_job_idx],
                )
            else:
                result = (
                    skip_job_revenue,
                    selected_jobs_idx_skipped,
                )

        memo[considered_job_idx] = result
        return result

    result = get_max_revenue_helper(jobs, considered_job_idx)
    return result
