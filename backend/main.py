from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timedelta
import argparse
import re
from models.job import Job
from models.car import (
    APPOINTMENT_DURATION_BY_CAR_TYPE,
    APPOINTMENT_REVENUE_BY_CAR_TYPE,
)
from models.schedule import Schedule
from utils.csv import (
    csv_to_rows,
    to_csv_datetime,
    to_csv_datetime_str,
)

MIN_ALLOWED_REQUEST_START_DATE = datetime(2022, 9, 1)
MIN_ALLOWED_APPOINTMENT_START_DATE = datetime(2022, 10, 1, 7)
MAX_ALLOWED_APPOINTMENT_END_DATE = datetime(2022, 11, 30, 19)
jobs: list[Job] = []


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self) -> None:
        # Add the CORS headers to the response before sending the actual headers
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self):
        # extract params:
        # date, time
        path_pattern = re.compile(r"^/schedule/(\d{4}-\d{2}-\d{2})/(\d{2}:\d{2})$")
        match = path_pattern.match(self.path)
        if not match:
            self.send_error(404, "Not Found")
            self.end_headers()
            return
        date_str = match.group(1)
        time_str = match.group(2)
        curr_time = to_csv_datetime(f"{date_str} {time_str}")
        schedule = Schedule(
            start_date=MIN_ALLOWED_APPOINTMENT_START_DATE,
            end_date=MAX_ALLOWED_APPOINTMENT_END_DATE,
        )
        for job in jobs:
            if job.req_time <= curr_time:
                schedule.add_job(job)

        # Send response status code
        self.send_response(200)
        self.end_headers()

        # Send headers
        self.send_header("Content-type", "application/json")

        # Write content as utf-8 data
        self.wfile.write(bytes(schedule.as_json(), "utf8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Backend for the tire-shop scheduler")
    parser.add_argument(
        "-f", "--file", required=True, type=str, help="The file to parse and schedule"
    )

    # Parse the arguments
    args = parser.parse_args()
    rows = csv_to_rows(args.file)
    for row in rows:
        req_time = row.req_time
        if (
            req_time < MIN_ALLOWED_REQUEST_START_DATE
            or req_time > MAX_ALLOWED_APPOINTMENT_END_DATE
        ):
            # Skip requests that were placed before September and after November
            print(
                f"Skipping appointment requested at {to_csv_datetime_str(req_time)} because the request was placed outside the allowed date range (September to November)"
            )
            continue
        appointment_start_time = row.appointment_start
        appointment_duration = APPOINTMENT_DURATION_BY_CAR_TYPE[row.car_type]
        appointment_revenue = APPOINTMENT_REVENUE_BY_CAR_TYPE[row.car_type]
        appointment_end_time = appointment_start_time + timedelta(
            minutes=appointment_duration
        )
        if req_time > appointment_start_time:
            print(
                '"Marty McFly, we won\'t be servicing the DeLorean today, come back yesterday" - Kevin McFly, 1985'
            )
            continue
        if (
            appointment_start_time < MIN_ALLOWED_APPOINTMENT_START_DATE
            or appointment_end_time > MAX_ALLOWED_APPOINTMENT_END_DATE
        ):
            # Skip appointments that are not in October and November
            print(
                f"Skipping appointment requested at {to_csv_datetime_str(req_time)} because its appointment start time ({to_csv_datetime_str(appointment_start_time)}, {to_csv_datetime_str(appointment_end_time)}) is outside the allowed date range (October to November)"
            )
            continue
        jobs.append(
            Job(
                req_time=req_time,
                start=appointment_start_time,
                finish=appointment_end_time,
                revenue=appointment_revenue,
                car_type=row.car_type,
            )
        )

    # Process them in request order
    jobs.sort(key=lambda j: j.req_time)

    port = 8080
    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Serving on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
