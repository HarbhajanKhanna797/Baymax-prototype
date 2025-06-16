import time

class ManualTimer:
    def __init__(self):
        self.start_time = None
        self.total_elapsed = 0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def pause(self):
        if self.running:
            self.total_elapsed += time.time() - self.start_time
            self.running = False

    def resume(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def get_elapsed_time(self):
        if self.running:
            return self.total_elapsed + (time.time() - self.start_time)
        return self.total_elapsed

    def reset(self):
        self.start_time = None
        self.total_elapsed = 0
        self.running = False
