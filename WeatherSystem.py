# WeatherSystem.py
import random
import time
from Environment import EnvironmentState

class WeatherSystem:
    def __init__(self, change_interval=25, transition_sec=10.0, clear_prob=0.40):
        """
        change_interval = seconds between weather target changes
        transition_sec  = how long it takes to reach new targets (smooth)
        clear_prob      = probability to go back to clear weather
        """
        self.env = EnvironmentState()
        self.env.recompute()

        self.last_change = time.time()
        self.change_interval = change_interval

        self.transition_sec = transition_sec
        self.clear_prob = clear_prob

        # targets (for smooth transitions)
        self.target_rain = 0.0
        self.target_fog = 0.0
        self.target_time = "day"

    def randomize_targets(self):
        # ✅ 40% chance: clear weather
        if random.random() < self.clear_prob:
            self.target_rain = 0.0
            self.target_fog = 0.0
            # sometimes change time even in clear weather
            if random.random() < 0.15:
                self.target_time = random.choice(["day", "dusk", "night"])
            else:
                self.target_time = self.env.time_of_day
            return

        # otherwise: random weather (mild most of the time)
        if random.random() < 0.25:
            self.target_time = random.choice(["day", "dusk", "night"])

        def mild_intensity():
            # mostly low, sometimes heavy
            if random.random() < 0.15:
                return random.uniform(0.6, 1.0)
            return random.uniform(0.0, 0.5)

        self.target_rain = mild_intensity()

        # fog more likely at dusk/night
        if self.target_time in ("dusk", "night"):
            self.target_fog = min(1.0, mild_intensity() + random.uniform(0.1, 0.3))
        else:
            self.target_fog = mild_intensity()

    def _approach(self, current, target, dt, rate_per_sec):
        if current < target:
            return min(target, current + rate_per_sec * dt)
        if current > target:
            return max(target, current - rate_per_sec * dt)
        return current

    def update(self, dt):
        now = time.time()

        # every X seconds, choose new target weather
        if now - self.last_change >= self.change_interval:
            self.randomize_targets()
            self.last_change = now

        # smooth transitions based on time (not FPS)
        rate = 1.0 / max(0.001, self.transition_sec)

        self.env.rain = self._approach(self.env.rain, self.target_rain, dt, rate)
        self.env.fog  = self._approach(self.env.fog,  self.target_fog,  dt, rate)

        # time_of_day changes when weather is close to target (feels natural)
        if abs(self.env.rain - self.target_rain) < 0.05 and abs(self.env.fog - self.target_fog) < 0.05:
            self.env.time_of_day = self.target_time

        self.env.recompute()
        return self.env
