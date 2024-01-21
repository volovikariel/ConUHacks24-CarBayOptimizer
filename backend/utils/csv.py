from datetime import datetime
import os

from models.car import CarType

CSV_DATE_FORMAT_STRING = r"%Y-%m-%d %H:%M"


class CSVRow:
    req_time: datetime
    appointment_start: datetime
    car_type: CarType

    def __init__(
        self,
        req_time: datetime,
        appointment_start: datetime,
        car_type: CarType,
    ):
        self.req_time = req_time
        self.appointment_start = appointment_start
        self.car_type = car_type

    def __str__(self) -> str:
        return f"{to_csv_date_str(self.req_time)},{to_csv_date_str(self.appointment_start)},{self.car_type.value}"


def csv_to_rows(filename: str) -> list[CSVRow]:
    # Ensure that the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File '{filename}' does not exist.")

    rows = []
    with open(filename, "r") as f:
        for row in f.readlines():
            # Just a comment, ignore this row~
            if row.startswith("#"):
                continue
            req_str, appointment_str, car_type = row.strip().split(",")
            rows.append(
                CSVRow(
                    req_time=to_csv_date(req_str),
                    appointment_start=to_csv_date(appointment_str),
                    car_type=CarType(car_type),
                )
            )
    return rows


def to_csv_date_str(dt: datetime) -> str:
    return dt.strftime(CSV_DATE_FORMAT_STRING)


def to_csv_date(string: str) -> datetime:
    return datetime.strptime(string, CSV_DATE_FORMAT_STRING)
