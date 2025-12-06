from os.path import join
import os
import random
import pygame

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super().__init__()
        car_folder_path = join("assets", "cars")

        car_categories = os.listdir(car_folder_path)

        chosen_category = random.choice(car_categories)

        chosen_folder_path = join(car_folder_path, chosen_category)
        car_images = os.listdir(chosen_folder_path)

        chosen_image = random.choice(car_images)

        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load(join(chosen_folder_path, chosen_image)).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 1)

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

    def draw(self, surface):
        surface.blit(self.image, self.rect)