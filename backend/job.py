class Job:
    def __init__(self, start, finish, revenue, type):
        self.start = start
        self.finish = finish
        self.revenue = revenue
        self.type = type
    def __str__(self) -> str:
        job = f"{self.type} starts at: {self.start}, ends at: {self.finish}. Revenue = {self.revenue}"
        return job
