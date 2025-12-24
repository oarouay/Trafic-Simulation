from os.path import join
import os
import random
import pygame
import time


class Pedestrian(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        """
        Initialize a pedestrian sprite

        Args:
            x: Screen width
            y: Screen height
            speed: Movement speed of the pedestrian
            direction: Direction of movement ('N', 'S', 'E', 'W')
        """
        super().__init__()
        self.original_speed = speed
        self.speed = speed
        self.direction = direction
        self.animation_state = 'idle'  # idle, left_foot, right_foot
        self.animation_timer = 0
        self.animation_speed = 10  # frames between animation changes

        # Load pedestrian images
        pedestrian_folder_path = join("assets", "pedestrians")

        self.images = {
            'idle': pygame.image.load(join(pedestrian_folder_path, 'idle.png')).convert_alpha(),
            'left_foot': pygame.image.load(join(pedestrian_folder_path, 'left_foot.png')).convert_alpha(),
            'right_foot': pygame.image.load(join(pedestrian_folder_path, 'right_foot.png')).convert_alpha()
        }

        # Scale all images
        for state in self.images:
            self.images[state] = pygame.transform.scale_by(self.images[state], 0.045)

        # Set initial image and rotation based on direction
        self._setup_direction(x, y)

    def _setup_direction(self, x, y):
        """Setup pedestrian position and rotation based on direction"""
        # Offset to position pedestrians on the crosswalk (right side of the road)
        crosswalk_offset = x * 0.11  # Adjust this value based on your road width

        if self.direction == "S":
            # Moving down - position on right side of vertical road
            for state in self.images:
                self.images[state] = pygame.transform.rotate(self.images[state], 180)
            self.image = self.images[self.animation_state]
            self.rect = self.image.get_frect(center=(x / 2 + crosswalk_offset, 0))

        elif self.direction == "N":
            # Moving up - position on right side of vertical road
            for state in self.images:
                self.images[state] = pygame.transform.rotate(self.images[state], 0)
            self.image = self.images[self.animation_state]
            self.rect = self.image.get_frect(center=(x / 2 - crosswalk_offset, y))

        elif self.direction == "E":
            # Moving right - position on right side of horizontal road
            for state in self.images:
                self.images[state] = pygame.transform.rotate(self.images[state], -90)
            self.image = self.images[self.animation_state]
            self.rect = self.image.get_frect(center=(0, y / 2 + crosswalk_offset))

        elif self.direction == "W":
            # Moving left - position on right side of horizontal road
            for state in self.images:
                self.images[state] = pygame.transform.rotate(self.images[state], 90)
            self.image = self.images[self.animation_state]
            self.rect = self.image.get_frect(center=(x, y / 2 - crosswalk_offset))

    def update(self):
        """Update pedestrian position and animation"""
        # Update animation
        self._update_animation()

        # Update position based on direction
        if self.direction == "N":
            self.rect.y -= self.speed
        elif self.direction == "S":
            self.rect.y += self.speed
        elif self.direction == "E":
            self.rect.x += self.speed
        elif self.direction == "W":
            self.rect.x -= self.speed

    def _update_animation(self):
        """Handle animation state transitions"""
        if self.speed == 0:
            # Pedestrian is stopped, show idle animation
            self.animation_state = 'idle'
        else:
            # Pedestrian is moving, cycle through walking animations
            self.animation_timer += 1

            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0

                if self.animation_state == 'idle':
                    self.animation_state = 'left_foot'
                elif self.animation_state == 'left_foot':
                    self.animation_state = 'right_foot'
                elif self.animation_state == 'right_foot':
                    self.animation_state = 'left_foot'

        # Update the displayed image
        self.image = self.images[self.animation_state]

    def stop(self):
        """Stop the pedestrian"""
        self.speed = 0

    def resume(self):
        """Resume pedestrian movement"""
        self.speed = self.original_speed

    def draw(self, surface):
        """Draw pedestrian on surface"""
        surface.blit(self.image, self.rect)

    def check_stop_line(self, stop_line_rect):
        """Check if the pedestrian intersects with a stop line (crosswalk)"""
        if self.direction == "N":
            pedestrian_point = self.rect.midtop
        elif self.direction == "S":
            pedestrian_point = self.rect.midbottom
        elif self.direction == "E":
            pedestrian_point = self.rect.midright
        elif self.direction == "W":
            pedestrian_point = self.rect.midleft

        return stop_line_rect.collidepoint(pedestrian_point)

    def will_collide_soon(self, other_entity, look_ahead_distance=20):
        """Check if pedestrian will collide with another entity soon"""
        future_rect = self.rect.copy()

        if self.direction == "N":
            future_rect.y -= look_ahead_distance
        elif self.direction == "S":
            future_rect.y += look_ahead_distance
        elif self.direction == "E":
            future_rect.x += look_ahead_distance
        elif self.direction == "W":
            future_rect.x -= look_ahead_distance

        return future_rect.colliderect(other_entity.rect)

    def get_animation_state(self):
        """Return current animation state"""
        return self.animation_state