from job import Job


class Bay:
    def __init__(self, jobs: list[Job] = []):
        self.jobs = jobs

    def __str__(self) -> str:
        return f"[{', '.join([str(job) for job in self.jobs])}]"
