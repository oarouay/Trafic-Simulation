from os.path import join
import os
import random
import pygame
import time

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super().__init__()
        car_folder_path = join("assets", "cars")

        car_categories = os.listdir(car_folder_path)

        chosen_category = random.choice(car_categories)

        chosen_folder_path = join(car_folder_path, chosen_category)
        car_images = os.listdir(chosen_folder_path)

        chosen_image = random.choice(car_images)
        self.original_speed=speed
        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load(join(chosen_folder_path, chosen_image)).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 1)




        self.last_honk_time = 0
        sound_folder_path = join("assets", "sound", "horns")

        horns_list = os.listdir(sound_folder_path)
        chosen_horn = random.choice(horns_list)

        self.horn_sound = pygame.mixer.Sound(join(sound_folder_path, chosen_horn))
        self.horn_sound.set_volume(0.5)  # Adjust volume

        if direction == "S":
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_frect(center=(x / 2-25, 0))
        if direction == "N":
            self.image = pygame.transform.rotate(self.image, 0)
            self.rect = self.image.get_frect(center=(x/2+25, y))
        elif direction == "E":
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_frect(center=(0, y/2+25))
        elif direction == "W":
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_frect(center=(x, y/2-25))


    def update(self):

        if self.direction == "N":
            self.rect.y -= self.speed
        elif self.direction == "S":
            self.rect.y += self.speed
        elif self.direction == "E":
            self.rect.x += self.speed
        elif self.direction == "W":
            self.rect.x -= self.speed

    def stop(self):
        self.speed = 0

    def resume(self):
        self.speed = self.original_speed
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_stop_line(self, stop_line_rect):
        """Check if the front of the car intersects with a stop line"""
        if self.direction == "N":
            car_point = self.rect.midtop
        elif self.direction == "S":
            car_point = self.rect.midbottom
        elif self.direction == "E":
            car_point = self.rect.midright
        elif self.direction == "W":
            car_point = self.rect.midleft

        return stop_line_rect.collidepoint(car_point)


    def will_collide_soon(self, other_car, look_ahead_distance=20):
        """Check if this car will collide with another car soon"""
        # Create a "future position" rectangle based on direction
        future_rect = self.rect.copy()

        if self.direction == "N":
            future_rect.y -= look_ahead_distance
        elif self.direction == "S":
            future_rect.y += look_ahead_distance
        elif self.direction == "E":
            future_rect.x += look_ahead_distance
        elif self.direction == "W":
            future_rect.x -= look_ahead_distance

        # Check if future position would collide with other car
        return future_rect.colliderect(other_car.rect)

    def horn(self, cooldown=2.0):
        """Play horn sound with adjustable cooldown"""
        current_time = time.time()

        if self.horn_sound and current_time - self.last_honk_time >= cooldown:
            self.horn_sound.set_volume(0.2)
            self.horn_sound.play()
            self.last_honk_time = current_time
            return True
        return False
