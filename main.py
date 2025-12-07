from os.path import join
import pygame
import Car
import TrafficLight
import TrafficLightController
import random
import time

pygame.init()

# the intersection
background = pygame.image.load(join('assets', 'intersection.png'))

WINDOW_WIDTH, WINDOW_HEIGHT = background.get_width(), background.get_height()
print(WINDOW_WIDTH, WINDOW_HEIGHT)
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Traffic Simulation")

running = True

# Start with empty list of cars
cars = []

# Spawn settings
last_spawn_time = time.time()
spawn_interval = random.uniform(1, 3)  # Spawn every 1-3 seconds

# Traffic lights
traffic_light_south = TrafficLight.TrafficLight(WINDOW_WIDTH, WINDOW_HEIGHT, 'S')
traffic_light_north = TrafficLight.TrafficLight(WINDOW_WIDTH, WINDOW_HEIGHT, 'N')
traffic_light_east = TrafficLight.TrafficLight(WINDOW_WIDTH, WINDOW_HEIGHT, 'E')
traffic_light_west = TrafficLight.TrafficLight(WINDOW_WIDTH, WINDOW_HEIGHT, 'W')

# Load line image
line_image = pygame.image.load(join('assets', 'line.png'))

line_north = line_image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))
line_south = line_image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))

line_image_vertical = pygame.transform.rotate(line_image, 90)
line_east = line_image_vertical.get_frect(center=(WINDOW_WIDTH / 2 - 90, WINDOW_HEIGHT / 2))
line_west = line_image_vertical.get_frect(center=(WINDOW_WIDTH / 2 + 90, WINDOW_HEIGHT / 2))

stop_lines = {
    "N": line_north,
    "S": line_south,
    "E": line_east,
    "W": line_west
}

traffic_lights = {
    "N": traffic_light_north,
    "S": traffic_light_south,
    "E": traffic_light_east,
    "W": traffic_light_west
}

controller = TrafficLightController.TrafficLightController(
    traffic_light_north,
    traffic_light_south,
    traffic_light_east,
    traffic_light_west
)


def spawn_random_car():
    """Spawn a car from a random direction with random speed"""
    direction = random.choice(['N', 'S', 'E', 'W'])
    speed = random.uniform(0.5, 2.0)  # Random speed between 0.5 and 2.0
    return Car.Car(WINDOW_WIDTH, WINDOW_HEIGHT, speed, direction)


def is_spawn_position_clear(new_car, existing_cars, min_distance=100):
    """Check if spawn position has enough space"""
    for car in existing_cars:
        # Only check cars in the same direction
        if car.direction != new_car.direction:
            continue

        # Check distance based on direction
        if new_car.direction in ["N", "S"]:
            distance = abs(car.rect.centery - new_car.rect.centery)
        else:  # E or W
            distance = abs(car.rect.centerx - new_car.rect.centerx)

        # If too close, spawn position is not clear
        if distance < min_distance:
            return False

    return True
def is_car_off_screen(car):
    """Check if car has left the screen"""
    if car.direction == "N" and car.rect.bottom < 0:
        return True
    elif car.direction == "S" and car.rect.top > WINDOW_HEIGHT:
        return True
    elif car.direction == "E" and car.rect.left > WINDOW_WIDTH:
        return True
    elif car.direction == "W" and car.rect.right < 0:
        return True
    return False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    # Spawn new cars randomly
    current_time = time.time()
    if current_time - last_spawn_time >= spawn_interval:
        new_car = spawn_random_car()

        # Only add if spawn position is clear
        if is_spawn_position_clear(new_car, cars):
            cars.append(new_car)
            print(f"Spawned car! Total cars: {len(cars)}")
        else:
            print("Spawn blocked - car already at spawn position")

        last_spawn_time = current_time
        spawn_interval = random.uniform(1, 3)
        print(f"Spawned car! Total cars: {len(cars)}")

    # Update controller
    controller.update()

    # Update and check all cars
    for car in cars:
        # Check for cars ahead BEFORE updating
        car_ahead = False
        for other_car in cars:
            if car != other_car and car.check_car_ahead(other_car):
                car_ahead = True
                break

        # Stop if there's a car ahead
        if car_ahead:
            car.stop()
        else:
            # Check stop line
            current_stop_line = stop_lines[car.direction]
            current_traffic_light = traffic_lights[car.direction]

            if car.check_stop_line(current_stop_line):
                if current_traffic_light.get_color() == "red":
                    car.stop()
                elif current_traffic_light.get_color() == "green":
                    car.resume()
            else:
                # If not at stop line and no car ahead, resume
                car.resume()

        car.update()

    # Remove cars that have left the screen
    cars = [car for car in cars if not is_car_off_screen(car)]

    # Draw the game
    display.blit(background, (0, 0))

    display.blit(line_image, line_north)
    display.blit(line_image, line_south)
    display.blit(line_image_vertical, line_east)
    display.blit(line_image_vertical, line_west)

    # Draw all cars
    for car in cars:
        car.draw(display)

    traffic_light_north.draw(display)
    traffic_light_south.draw(display)
    traffic_light_east.draw(display)
    traffic_light_west.draw(display)

    pygame.display.update()

pygame.quit()