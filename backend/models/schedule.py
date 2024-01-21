from datetime import datetime, timedelta
import json
from models.day import Day
from models.job import Job
from utils.csv import to_csv_date_str


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

    def as_dict(self, selected_day: datetime):
        # return datetime string and day.as_dict object
        return {
            "days": [
                {
                    to_csv_date_str(day.start_time): day.as_dict(selected_day)
                    for day in self.days
                }
            ],
            "total_revenue_up_to_today": self.revenue_up_to(selected_day),
            "total_turned_away_revenue_up_to_today": self.get_total_turned_away_revenue_up_to(
                selected_day
            ),
        }

    def as_json(self, max_day: datetime):
        return json.dumps(self.as_dict(max_day), indent=4)