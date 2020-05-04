import datetime


class timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = datetime.datetime.now()

    def stop(self):
        self.end_time = datetime.datetime.now()
        # seconds
        interval = (end_time-start_time).seconds
        return interval
