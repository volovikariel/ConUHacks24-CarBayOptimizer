import json
from models.job import Job


class Bay:
    def __init__(self, jobs: list[Job]):
        self.jobs = jobs

    def __str__(self) -> str:
        return f"[{', '.join([str(job) for job in self.jobs])}]"

    def as_dict(self):
        return {
            "jobs": [job.as_dict() for job in self.jobs],
        }

    def as_json(self):
        return json.dumps(self.as_dict(), indent=4)
