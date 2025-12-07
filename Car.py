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
        self.original_speed=speed
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

    def check_car_ahead(self, other_car, safe_distance=20):
        """Check if there's another car ahead using front/back collision points"""
        # Only check cars moving in the same direction
        if self.direction != other_car.direction:
            return False

        # Check based on direction
        if self.direction == "N":
            # My front is midtop, other car's back is midbottom
            my_front = self.rect.midtop
            other_back = other_car.rect.midbottom

            # Check if other car is ahead and in same lane
            if (other_back[1] < my_front[1] and  # Other car is above me
                    abs(other_back[0] - my_front[0]) < 30 and  # Same lane (x-axis)
                    my_front[1] - other_back[1] < safe_distance):  # Within safe distance
                return True

        elif self.direction == "S":
            # My front is midbottom, other car's back is midtop
            my_front = self.rect.midbottom
            other_back = other_car.rect.midtop

            # Check if other car is ahead and in same lane
            if (other_back[1] > my_front[1] and  # Other car is below me
                    abs(other_back[0] - my_front[0]) < 30 and  # Same lane
                    other_back[1] - my_front[1] < safe_distance):
                return True

        elif self.direction == "E":
            # My front is midright, other car's back is midleft
            my_front = self.rect.midright
            other_back = other_car.rect.midleft

            # Check if other car is ahead and in same lane
            if (other_back[0] > my_front[0] and  # Other car is to my right
                    abs(other_back[1] - my_front[1]) < 30 and  # Same lane (y-axis)
                    other_back[0] - my_front[0] < safe_distance):
                return True

        elif self.direction == "W":
            # My front is midleft, other car's back is midright
            my_front = self.rect.midleft
            other_back = other_car.rect.midright

            # Check if other car is ahead and in same lane
            if (other_back[0] < my_front[0] and  # Other car is to my left
                    abs(other_back[1] - my_front[1]) < 30 and  # Same lane
                    my_front[0] - other_back[0] < safe_distance):
                return True

        return False