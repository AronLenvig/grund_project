import time
import datetime

import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.base import JobLookupError


class Scheduler:
    def __init__(self):
        self.jobId = 0
        self.interval = 0

        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.start()
        atexit.register(lambda: self.scheduler.shutdown())

    def setInterval(self, interval):
        if interval < 0.001:
            raise ValueError("Interval too short.")
        self.interval = interval
        print(f"{datetime.datetime.utcnow()} - job set interval {self.interval}s")

    def run(self, interval):
        if interval < 0.001:
            return  # Skip running if the interval is too short
        
        print(f"{datetime.datetime.utcnow()} - job {self.jobId} running")

    def addJob(self):
        try:
            self.scheduler.remove_job(str(self.jobId))
            print(f"{datetime.datetime.utcnow()} - job {self.jobId} stopped")
        except JobLookupError:
            pass
        
        self.jobId += 1
        self.scheduler.add_job(
            func=self.run,
            args=[self.interval],
            trigger=IntervalTrigger(seconds=self.interval),
            id=str(self.jobId)
        )
        print(f"{datetime.datetime.utcnow()} - job {self.jobId} started")


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.setInterval(1)  # Set the interval to 1 second
    scheduler.addJob()

    try:
        # To keep the main thread alive and observe the job execution.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scheduler stopped.")
