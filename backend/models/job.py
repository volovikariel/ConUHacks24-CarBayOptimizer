from datetime import datetime
import json
from models.car import CarType
from utils.csv import CSV_DATE_FORMAT_STRING


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
        self.treat_as_inf = False

    def __str__(self) -> str:
        req_time_str = self.req_time.strftime(CSV_DATE_FORMAT_STRING)
        start_time_str = self.start.strftime(CSV_DATE_FORMAT_STRING)
        end_time_str = self.finish.strftime(CSV_DATE_FORMAT_STRING)
        job = f"{self.car_type.value} req@{req_time_str} appointment[{start_time_str},{end_time_str}]; Revenue: ${self.revenue}"
        return job

    def as_dict(self):
        return {
            "req_time": self.req_time.strftime(CSV_DATE_FORMAT_STRING),
            "start_time": self.start.strftime(CSV_DATE_FORMAT_STRING),
            "end_time": self.finish.strftime(CSV_DATE_FORMAT_STRING),
            "revenue": self.revenue,
            "car_type": self.car_type.value,
        }

    def as_json(self):
        return json.dumps(self.as_dict(), indent=4)
