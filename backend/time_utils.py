from datetime import datetime

CSV_DATE_FORMAT_STRING = r"%Y-%m-%d %H:%M"


# Convert minutes to seconds
def seconds(minutes: int) -> int:
    return minutes * 60


def to_csv_date_str(dt: datetime) -> str:
    return dt.strftime(CSV_DATE_FORMAT_STRING)


def to_csv_date(string: str) -> datetime:
    return datetime.strptime(string, CSV_DATE_FORMAT_STRING)
