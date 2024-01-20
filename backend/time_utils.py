import datetime
import time


def minutes_to_seconds(minutes: int) -> int:
    return minutes * 60


# Returns unix ts (seconds)
def date_to_unix_ts(date_str: str) -> int:
    # The date format of the CSV we're given
    date_format_string = "%Y-%m-%d %H:%M"
    date = datetime.datetime.strptime(date_str, date_format_string)
    return int(time.mktime(date.timetuple()))
