from datetime import datetime, timedelta
from day import Day
from job import Job
from time_utils import CSV_DATE_FORMAT_STRING, date_to_unix_ts

NUM_SEC_IN_DAY = 86400


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
                    start_unix_ts=date_to_unix_ts(
                        (
                            # 7am
                            current_date + timedelta(hours=7)
                        ).strftime(CSV_DATE_FORMAT_STRING),
                        CSV_DATE_FORMAT_STRING,
                    ),
                    end_unix_ts=date_to_unix_ts(
                        (
                            # 7pm
                            current_date + timedelta(hours=7 + 12)
                        ).strftime(CSV_DATE_FORMAT_STRING),
                        CSV_DATE_FORMAT_STRING,
                    ),
                )
            )
            current_date += timedelta(days=1)

    def add_job(self, job: Job) -> None:
        day_idx = get_day_idx_of_year(2022, job.start)
        # Make sure the jobs are within the day's working hours (7am to 7pm)
        if (
            job.start < self.days[day_idx].start_unix_ts
            or job.finish > self.days[day_idx].end_unix_ts
        ):
            return
        # It's a walk-in
        if job.req_time == job.start:
            self.days[day_idx].handle_walk_in_job(job)
        else:
            self.days[day_idx].handle_reserved_job(job)


def get_day_idx_of_year(year: int, unix_ts: int):
    return seconds_since_year_start(year, unix_ts) // NUM_SEC_IN_DAY


def seconds_since_year_start(year, unix_ts):
    start_of_year = datetime(year, 1, 1)
    timestamp_datetime = datetime.fromtimestamp(unix_ts)
    elapsed_seconds = int((timestamp_datetime - start_of_year).total_seconds())
    return elapsed_seconds
