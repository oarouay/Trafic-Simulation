# Environment.py
from dataclasses import dataclass
import random
import pygame

@dataclass
class EnvironmentState:
    time_of_day: str = "day"   # "day", "dusk", "night"
    rain: float = 0.0          # 0..1
    fog: float = 0.0           # 0..1

    # Derived factors (updated each frame or when state changes)
    friction: float = 1.0      # lower = more slippery
    visibility: float = 1.0    # lower = less visible
    speed_factor: float = 1.0  # multiply car base speed
    caution: float = 1.0       # reaction / braking multiplier (higher = more cautious)

    def recompute(self):
        # friction drops with rain (simple model)
        self.friction = max(0.55, 1.0 - 0.35 * self.rain)

        # visibility drops with fog + night
        night_penalty = 0.35 if self.time_of_day == "night" else 0.15 if self.time_of_day == "dusk" else 0.0
        self.visibility = max(0.20, 1.0 - 0.75 * self.fog - night_penalty)

        # cars drive slower when friction is low or visibility is low
        self.speed_factor = max(0.35, 0.65 * self.friction + 0.35 * self.visibility)

        # caution increases when rainy/foggy/night
        self.caution = 1.0 + 1.2 * self.rain + 1.5 * self.fog + (0.7 if self.time_of_day == "night" else 0.3 if self.time_of_day == "dusk" else 0.0)


class WeatherRenderer:
    """Pure visuals: rain drops + fog + night tint."""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self._fog_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self._tint_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self._rain_drops = [(random.randrange(0, w), random.randrange(0, h), random.randrange(8, 18)) for _ in range(180)]

    def draw(self, screen, env: EnvironmentState):
        # Night / dusk tint
        self._tint_surface.fill((0, 0, 0, 0))
        if env.time_of_day == "dusk":
            self._tint_surface.fill((10, 5, 0, 60))
            screen.blit(self._tint_surface, (0, 0))
        elif env.time_of_day == "night":
            self._tint_surface.fill((0, 0, 20, 110))
            screen.blit(self._tint_surface, (0, 0))

        # Fog overlay (gray alpha)
        if env.fog > 0:
            self._fog_surface.fill((200, 200, 200, int(160 * env.fog)))
            screen.blit(self._fog_surface, (0, 0))

        # Rain (simple streaks)
        if env.rain > 0:
            # number of streaks scales with intensity
            count = int(len(self._rain_drops) * env.rain)
            for i in range(count):
                x, y, length = self._rain_drops[i]
                pygame.draw.line(screen, (180, 180, 255), (x, y), (x, y + length), 1)
                # move drop
                y = (y + int(10 + 18 * env.rain)) % self.h
                x = (x + 1) % self.w
                self._rain_drops[i] = (x, y, length)
