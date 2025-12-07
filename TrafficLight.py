import pygame
from os.path import join
import time

class TrafficLight(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, initial_state="red"):
        super().__init__()
        self.last_change_time = time.time()
        self.x=x
        self.y=y
        self.direction = direction
        self.images = {
            'red': pygame.image.load(join('assets','trafficlight', 'REDtraffic.png')).convert_alpha(),
            'yellow': pygame.image.load(join('assets','trafficlight', 'YELLOWtraffic.png')).convert_alpha(),
            'green': pygame.image.load(join('assets','trafficlight', 'GREENtraffic.png')).convert_alpha()
        }
        for color in self.images:
            self.images[color] = pygame.transform.scale_by(self.images[color], 0.07)

        self.current_color = initial_state
        self.image = self.images[self.current_color]
        self._preload_images()

    def _preload_images(self):
        if self.direction == "N":
            for color in self.images:
                self.images[color] = pygame.transform.rotate(self.images[color], 180)
            # Update current image after rotation
            self.image = self.images[self.current_color]
            # Set position
            self.rect = self.image.get_frect(center=(self.x / 2 - 65, self.y / 2 - 127))



        elif self.direction == "S":
            # Update current image after rotation
            self.image = self.images[self.current_color]
            # Set position
            self.rect = self.image.get_frect(center=(self.x / 2 + 65, self.y / 2 + 127))




        elif self.direction == "E":
            for color in self.images:
                self.images[color] = pygame.transform.rotate(self.images[color], -90)
            # Update current image after rotation
            self.image = self.images[self.current_color]
            # Set position
            self.rect = self.image.get_frect(center=(self.x / 2 -120, self.y / 2 +65))



        elif self.direction == "W":
            for color in self.images:
                self.images[color] = pygame.transform.rotate(self.images[color], 90)
            # Update current image after rotation
            self.image = self.images[self.current_color]
            # Set position
            self.rect = self.image.get_frect(center=(self.x / 2 + 120, self.y / 2 - 70))
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def change_color(self, color):
        if color in self.images:
            self.current_color = color
            self.image = self.images[color]
        else:
            print(f"Warning: Unknown traffic light color '{color}'")

    def get_color(self):
        return self.current_color
