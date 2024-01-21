from datetime import datetime
import time

CSV_DATE_FORMAT_STRING = r"%Y-%m-%d %H:%M"


# Convert minutes to seconds
def seconds(minutes: int) -> int:
    return minutes * 60


# Returns unix ts (seconds)
def date_to_unix_ts(date_str: str, date_fmt: str) -> int:
    date = datetime.strptime(date_str, date_fmt)
    return int(time.mktime(date.timetuple()))


def unix_ts_to_date(unix_ts: int, date_fmt: str) -> str:
    date = datetime.fromtimestamp(unix_ts)
    return date.strftime(date_fmt)
