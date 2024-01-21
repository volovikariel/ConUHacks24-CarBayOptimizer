from datetime import datetime
from models.bay import Bay
from models.car import CarType
from models.job import Job, schedule
from utils.misc import ranges_overlap


class Day:
    def __init__(
        self,
        start_time: datetime,
        end_time: datetime,
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.reserved_bays: list[Bay] = [Bay()] * 5
        self.walk_in_bay_by_type = {
            CarType.compact: Bay(),
            CarType.medium: Bay(),
            CarType.full_size: Bay(),
            CarType.class_1_truck: Bay(),
            CarType.class_2_truck: Bay(),
        }
        self.jobs = []
        self.selected_jobs = []
        # TODO
        self.revenue_by_car_type = 0
        # TODO
        self.turned_away_revenue_by_car_type = 0

    def add_reserved_job(self, job: Job) -> None:
        self.jobs.append(job)

    def optimize_reserved_bays(self):
        remaining_jobs = self.jobs
        self.selected_jobs = []
        for i in range(len(self.reserved_bays)):
            # Short circuit if no remaining jobs
            if len(remaining_jobs) == 0:
                break
            max_revenue, selected_jobs = schedule(remaining_jobs)
            self.selected_jobs.extend(selected_jobs)
            self.reserved_bays[i] = Bay(selected_jobs)
            remaining_jobs = self.get_remaining_jobs()

    def handle_walk_in_job(self, added_job: Job) -> None:
        walk_in_bay = self.walk_in_bay_by_type[added_job.car_type]
        added_job_range = (added_job.start, added_job.finish)
        if not ranges_overlap(added_job_range, walk_in_bay.jobs):
            walk_in_bay.jobs.append(added_job)
            return
        # Otherwise check if a reserved bay has no jobs and until this job is finished
        # if so, then add it to the reserved bays
        for reserved_bay in self.reserved_bays:
            if not ranges_overlap(added_job_range, reserved_bay.jobs):
                reserved_bay.jobs.append(added_job)
                return

        # Otherwise, it's turned away
        # TODO: keep track of the amount and car type that was turned away

    def handle_reserved_job(self, added_job: Job) -> None:
        self.add_reserved_job(added_job)
        self.optimize_reserved_bays()

    def get_remaining_jobs(self) -> list[Job]:
        return [job for job in self.jobs if job not in self.selected_jobs]

    def __str__(self) -> str:
        string = ""
        if len(self.selected_jobs) > 0:
            for bay_idx, bay in enumerate(self.reserved_bays):
                string += f"Bay {bay_idx}: {bay}\n"
        return string
