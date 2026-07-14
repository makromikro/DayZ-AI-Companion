import time


class DayZEventMonitor:
    def __init__(
        self,
        warning_distance=35.0,
        danger_distance=15.0,
        warning_cooldown=20.0,
    ):
        self.warning_distance = warning_distance
        self.danger_distance = danger_distance
        self.warning_cooldown = warning_cooldown

        self.last_infected_count = 0
        self.last_infected_distance = -1.0
        self.last_warning_time = 0.0

        self.threat_active = False
        self.danger_announced = False

    def check(self, state):
        """
        Inspect the latest DayZ companion state.

        Returns an event dictionary when Boris should react.
        Returns None when there is nothing new worth announcing.
        """

        if not state:
            return None

        if not state.get("alive", False):
            self.reset()
            return None

        infected_count = int(
            state.get("nearby_infected_count", 0)
        )

        infected_distance = float(
            state.get("nearest_infected_distance", -1.0)
        )

        now = time.monotonic()

        # No active infected threat.
        if infected_count <= 0 or infected_distance < 0:
            self.last_infected_count = 0
            self.last_infected_distance = -1.0
            self.threat_active = False
            self.danger_announced = False

            return None

        # Infected exist, but none are close enough to warn about.
        if infected_distance > self.warning_distance:
            self.last_infected_count = infected_count
            self.last_infected_distance = infected_distance
            self.threat_active = False
            self.danger_announced = False

            return None

        event = None

        # First infected entering warning range.
        if not self.threat_active:
            self.threat_active = True

            event = {
                "type": "infected_warning",
                "infected_count": infected_count,
                "distance": infected_distance,
                "reason": "new_threat",
            }

        # Number of infected increased.
        elif infected_count > self.last_infected_count:
            event = {
                "type": "infected_warning",
                "infected_count": infected_count,
                "distance": infected_distance,
                "reason": "count_increased",
            }

        # Infected crossed into immediate danger range.
        elif (
            infected_distance <= self.danger_distance
            and not self.danger_announced
        ):
            self.danger_announced = True

            event = {
                "type": "infected_warning",
                "infected_count": infected_count,
                "distance": infected_distance,
                "reason": "immediate_danger",
            }

        # Infected became dramatically closer.
        elif (
            self.last_infected_distance > 0
            and infected_distance
            <= self.last_infected_distance - 10.0
            and now - self.last_warning_time
            >= self.warning_cooldown
        ):
            event = {
                "type": "infected_warning",
                "infected_count": infected_count,
                "distance": infected_distance,
                "reason": "approaching",
            }

        self.last_infected_count = infected_count
        self.last_infected_distance = infected_distance

        if event:
            self.last_warning_time = now

        return event

    def reset(self):
        """
        Reset all stored threat state.
        """

        self.last_infected_count = 0
        self.last_infected_distance = -1.0
        self.last_warning_time = 0.0

        self.threat_active = False
        self.danger_announced = False