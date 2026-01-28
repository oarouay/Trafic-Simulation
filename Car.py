from os.path import join
import os
import random
import pygame
import time
import math


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super().__init__()
        car_folder_path = join("assets", "cars")

        car_categories = os.listdir(car_folder_path)

        chosen_category = random.choice(car_categories)
        chosen_folder_path = join(car_folder_path, chosen_category)
        car_images = os.listdir(chosen_folder_path)

        chosen_image = random.choice(car_images)
        self.original_speed = speed
        self.speed = speed
        self.base_speed = speed
        self.direction = direction
        self.image = pygame.image.load(join(chosen_folder_path, chosen_image)).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 1)

        self.is_police = "police" in chosen_image.lower()
        self.is_ambulance = "ambulance" in chosen_image.lower()
        self.is_emergency = self.is_police or self.is_ambulance

        # Initialize siren variables for all cars (but only use for police)
        self.siren_sound = None
        self.siren_playing = False

        if self.is_emergency:
            print(f"{'Police' if self.is_police else 'Ambulance'} vehicle detected!")
            # Initialize emergency light animation variables
            self.light_time = 0
            self.light_pulse = 0

            # Load siren sound
            try:
                siren_path = join("assets", "sound", "siren", "police-siren.mp3")  # or .wav
                self.siren_sound = pygame.mixer.Sound(siren_path)
                self.siren_sound.set_volume(0.3)
                # Automatically start playing the siren
                self.siren_sound.play(loops=-1)
                self.siren_playing = True
                print("Siren playing!")
            except Exception as e:
                print(f"Siren sound not found: {e}")
                self.siren_sound = None

        self.last_honk_time = 0
        sound_folder_path = join("assets", "sound", "horns")

        horns_list = os.listdir(sound_folder_path)
        chosen_horn = random.choice(horns_list)

        self.horn_sound = pygame.mixer.Sound(join(sound_folder_path, chosen_horn))
        self.horn_sound.set_volume(0.5)  # Adjust volume

        if direction == "S":
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_frect(center=(x / 2 - 25, 0))
        if direction == "N":
            self.image = pygame.transform.rotate(self.image, 0)
            self.rect = self.image.get_frect(center=(x / 2 + 25, y))
        elif direction == "E":
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_frect(center=(0, y / 2 + 25))
        elif direction == "W":
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_frect(center=(x, y / 2 - 25))

    def apply_environment(self, env):
        # emergency vehicles: reduce less
        emergency_bonus = 0.15 if self.is_emergency else 0.0
        factor = min(1.0, env.speed_factor + emergency_bonus)

        # only change "normal driving" speed, keep stop() working
        self.original_speed = self.base_speed * factor
        if self.speed > 0:  # if moving, update current speed too
            self.speed = self.original_speed

    def update(self):
        if self.direction == "N":
            self.rect.y -= self.speed
        elif self.direction == "S":
            self.rect.y += self.speed
        elif self.direction == "E":
            self.rect.x += self.speed
        elif self.direction == "W":
            self.rect.x -= self.speed

        # Update police light animation
        if self.is_emergency:
            self.light_time += 1
            self.light_pulse = abs(math.sin(self.light_time * 0.1)) * 0.5 + 0.5

    def stop(self):
        self.speed = 0

    def resume(self):
        self.speed = self.original_speed

    def stop_siren(self):
        """Stop playing the police siren"""
        if self.is_emergency and self.siren_sound and self.siren_playing:
            self.siren_sound.stop()
            self.siren_playing = False

    def draw_glowing_light(self, surface, color, center, radius, glow_intensity=1.0):
        """Draw a glowing light effect with multiple layered circles"""
        # Create a temporary surface with per-pixel alpha
        glow_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)

        # Draw multiple circles with decreasing opacity for glow effect
        for i in range(5, 0, -1):
            current_radius = radius * i / 2
            alpha = int((255 / (i + 1)) * glow_intensity)
            glow_color = (*color, alpha)
            pygame.draw.circle(glow_surface, glow_color,
                               (radius * 2, radius * 2), int(current_radius))

        # Blit the glow surface onto the main surface
        surface.blit(glow_surface,
                     (center[0] - radius * 2, center[1] - radius * 2))

    def draw(self, surface, env=None):
        surface.blit(self.image, self.rect)

        if env is not None:
            self.draw_headlights(surface, env)

        surface.blit(self.image, self.rect)
        # Draw emergency lights if this is a police car or ambulance
        if self.is_emergency:
            # Calculate light positions based on car direction
            light_offset = 38

            if self.direction == "N":
                left_light = (self.rect.centerx - 8, self.rect.top + light_offset)
                right_light = (self.rect.centerx + 8, self.rect.top + light_offset)
            elif self.direction == "S":
                left_light = (self.rect.centerx + 8, self.rect.bottom - light_offset)
                right_light = (self.rect.centerx - 8, self.rect.bottom - light_offset)
            elif self.direction == "E":
                left_light = (self.rect.right - light_offset, self.rect.centery - 8)
                right_light = (self.rect.right - light_offset, self.rect.centery + 8)
            elif self.direction == "W":
                left_light = (self.rect.left + light_offset, self.rect.centery + 8)
                right_light = (self.rect.left + light_offset, self.rect.centery - 8)

            # Determine light colors based on vehicle type
            if self.is_ambulance:
                # Ambulance: red and white lights
                light_color_1 = (255, 0, 0)  # Red
                light_color_2 = (255, 255, 255)  # White
            else:
                # Police: red and blue lights
                light_color_1 = (0, 100, 255)  # Blue
                light_color_2 = (255, 0, 0)  # Red

            # Alternate between lights
            if int(self.light_time / 15) % 2 == 0:
                self.draw_glowing_light(surface, light_color_1, left_light, 8, self.light_pulse)
            else:
                self.draw_glowing_light(surface, light_color_2, right_light, 8, self.light_pulse)

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

    def draw_headlights(self, surface, env):
        """
        Soft, transparent headlights.
        Turn on when raining/foggy or at dusk/night.
        """
        if env is None:
            return

        # --- When to turn on headlights ---
        rain = getattr(env, "rain", 0.0)
        fog = getattr(env, "fog", 0.0)
        time_of_day = getattr(env, "time_of_day", "day")
        visibility = getattr(env, "visibility", 1.0)

        headlights_on = (rain >= 0.15) or (fog >= 0.15) or (time_of_day in ("dusk", "night"))
        if not headlights_on:
            return

        # --- Shape parameters ---
        base_len = 120
        length = int(base_len * (0.55 + 0.75 * max(0.2, visibility)))  # shorter when foggy
        width = 80

        # --- Intensity (alpha) ---
        strength = 0.35 + 0.55 * min(1.0, rain + fog)
        if time_of_day == "night":
            strength += 0.25
        alpha = int(140 * min(1.0, strength))
        alpha = int(alpha * (0.6 + 0.4 * max(0.2, visibility)))  # dim a bit in heavy fog

        # Transparent overlay for soft blending
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))

        cx, cy = self.rect.centerx, self.rect.centery

        # --- Compute cone points based on direction ---
        if self.direction == "N":
            start = (cx, self.rect.top)
            p1 = (cx - width // 2, self.rect.top - length)
            p2 = (cx + width // 2, self.rect.top - length)
        elif self.direction == "S":
            start = (cx, self.rect.bottom)
            p1 = (cx - width // 2, self.rect.bottom + length)
            p2 = (cx + width // 2, self.rect.bottom + length)
        elif self.direction == "E":
            start = (self.rect.right, cy)
            p1 = (self.rect.right + length, cy - width // 2)
            p2 = (self.rect.right + length, cy + width // 2)
        else:  # "W"
            start = (self.rect.left, cy)
            p1 = (self.rect.left - length, cy - width // 2)
            p2 = (self.rect.left - length, cy + width // 2)

        # --- Draw a soft main cone (transparent) ---
        pygame.draw.polygon(overlay, (255, 245, 210, alpha), [start, p1, p2])

        # --- Inner brighter cone ---
        inner_w = int(width * 0.55)
        inner_len = int(length * 0.65)
        inner_alpha = int(alpha * 0.7)

        if self.direction == "N":
            ip1 = (cx - inner_w // 2, self.rect.top - inner_len)
            ip2 = (cx + inner_w // 2, self.rect.top - inner_len)
            istart = (cx, self.rect.top)
        elif self.direction == "S":
            ip1 = (cx - inner_w // 2, self.rect.bottom + inner_len)
            ip2 = (cx + inner_w // 2, self.rect.bottom + inner_len)
            istart = (cx, self.rect.bottom)
        elif self.direction == "E":
            ip1 = (self.rect.right + inner_len, cy - inner_w // 2)
            ip2 = (self.rect.right + inner_len, cy + inner_w // 2)
            istart = (self.rect.right, cy)
        else:
            ip1 = (self.rect.left - inner_len, cy - inner_w // 2)
            ip2 = (self.rect.left - inner_len, cy + inner_w // 2)
            istart = (self.rect.left, cy)

        pygame.draw.polygon(overlay, (255, 255, 235, inner_alpha), [istart, ip1, ip2])

        # --- Glow around the headlight source (softens the "triangle" look) ---
        pygame.draw.circle(overlay, (255, 255, 220, int(alpha * 0.7)), start, 10)
        pygame.draw.circle(overlay, (255, 255, 220, int(alpha * 0.35)), start, 18)

        # IMPORTANT: normal alpha blit (NO BLEND_RGBA_ADD)
        surface.blit(overlay, (0, 0))

    def horn(self, cooldown=2.0):
        """Play horn sound with adjustable cooldown"""
        current_time = time.time()

        if self.horn_sound and current_time - self.last_honk_time >= cooldown:
            self.horn_sound.set_volume(0.2)
            self.horn_sound.play()
            self.last_honk_time = current_time
            return True
        return False