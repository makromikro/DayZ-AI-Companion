import time


class Scheduler:

    def __init__(self):
        self.last_request = 0
        self.cooldown = 1.0

    def can_think(self):
        now = time.time()

        if now - self.last_request >= self.cooldown:
            self.last_request = now
            return True

        return False