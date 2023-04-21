import time


class Timer:
    def __init__(self, name):
        self.name = name
        self.start = time.time()
        self.stop = None
        self.duration = 0

    def stop_the_clock(self):
        self.stop = time.time()
        return self.check_watch()

    def check_watch(self, p=True):
        if self.stop is not None:
            self.duration = self.stop - self.start
        else:
            self.duration = time.time() - self.start

        if p:
            print(f"{self.name} : {self.duration}s")

        return self.duration
