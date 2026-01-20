from os.path import join
import pygame
import sys
import Car
import Pedestrian
import TrafficLight
import TrafficLightController
import random
import time
from Button import Button

pygame.init()
pygame.mixer.init()

# Global display and font settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Traffic Simulation")

# Load background for menu
BG = pygame.image.load(join('assets', 'background.png'))
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

LAST_STATS = None


def get_font(size):
    """Load and return a font of specified size"""
    return pygame.font.Font(join('assets', 'fonts', 'font.ttf'), size)
def spawn_random_car(window_width, window_height):
    """Spawn a car from a random direction with random speed"""
    direction = random.choice(['N', 'S', 'E', 'W'])
    speed = random.uniform(1, 3.0)
    return Car.Car(window_width, window_height, speed, direction)
def spawn_test_pedestrian(window_width, window_height):
    """Spawn a test pedestrian"""
    direction = random.choice(['N', 'S', 'E', 'W'])
    speed = random.uniform(0.5, 1.5)
    return Pedestrian.Pedestrian(window_width, window_height, speed, direction)
def is_spawn_position_clear(new_car, existing_cars, min_distance=100):
    """Check if spawn position has enough space"""
    for car in existing_cars:
        if car.direction != new_car.direction:
            continue

        if new_car.direction in ["N", "S"]:
            distance = abs(car.rect.centery - new_car.rect.centery)
        else:
            distance = abs(car.rect.centerx - new_car.rect.centerx)

        if distance < min_distance:
            return False

    return True
def is_entity_off_screen(entity, window_width, window_height):
    """Check if an entity (car or pedestrian) has left the screen"""
    return (entity.rect.right < 0 or entity.rect.left > window_width or
            entity.rect.bottom < 0 or entity.rect.top > window_height)
def initialize_simulation(window_width, window_height):
    """Initialize all simulation components"""
    # Traffic lights
    traffic_light_south = TrafficLight.TrafficLight(window_width, window_height, 'S')
    traffic_light_north = TrafficLight.TrafficLight(window_width, window_height, 'N')
    traffic_light_east = TrafficLight.TrafficLight(window_width, window_height, 'E')
    traffic_light_west = TrafficLight.TrafficLight(window_width, window_height, 'W')

    # Load line image
    line_image = pygame.image.load(join('assets', 'line.png'))

    line_north = line_image.get_frect(center=(window_width / 2, window_height / 2 + 100))
    line_south = line_image.get_frect(center=(window_width / 2, window_height / 2 - 100))

    line_image_vertical = pygame.transform.rotate(line_image, 90)
    line_east = line_image_vertical.get_frect(center=(window_width / 2 - 90, window_height / 2))
    line_west = line_image_vertical.get_frect(center=(window_width / 2 + 90, window_height / 2))

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

    return {
        'traffic_lights': traffic_lights,
        'stop_lines': stop_lines,
        'controller': controller,
        'line_image': line_image,
        'line_image_vertical': line_image_vertical,
        'line_north': line_north,
        'line_south': line_south,
        'line_east': line_east,
        'line_west': line_west,
        'traffic_light_north': traffic_light_north,
        'traffic_light_south': traffic_light_south,
        'traffic_light_east': traffic_light_east,
        'traffic_light_west': traffic_light_west
    }
def run_simulation():
    """Run the traffic simulation"""
    # Load background
    background = pygame.image.load(join('assets', 'intersection.png'))
    window_width, window_height = background.get_width(), background.get_height()

    # Create a new display for simulation
    sim_display = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Traffic Simulation - Press ESC to return to menu")

    # Initialize simulation components
    sim_data = initialize_simulation(window_width, window_height)

    # Load and scale finish button image
    finish_img = pygame.transform.scale(pygame.image.load("assets/Quit Rect.png"), (120, 50))

    # Game state
    cars = []
    pedestrians = []
    last_spawn_time = time.time()
    spawn_interval = random.uniform(1, 3)
    last_pedestrian_spawn_time = time.time()
    pedestrian_spawn_interval = random.uniform(3, 6)
    running = True
    clock = pygame.time.Clock()

    global LAST_STATS
    sim_start_time = time.time()

    cars_crossed = 0
    peds_crossed = 0

    # per-car wait tracking without editing Car.py
    car_wait = {}  # key: id(car) -> {'wait_total':0, 'stopped':False, 'stop_started':0}

    # Spawn initial test pedestrian
    test_pedestrian = spawn_test_pedestrian(window_width, window_height)
    pedestrians.append(test_pedestrian)
    print(f"Spawned test pedestrian! Direction: {test_pedestrian.direction}")

    # Main simulation loop
    while running:
        clock.tick(60)

        MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if finish button is clicked
                finish_button = Button(image=finish_img, pos=(window_width - 70, 30),
                                       text_input="FINISH", font=get_font(30), base_color="#d7fcd4",
                                       hovering_color="White")
                if finish_button.checkForInput(MOUSE_POS):
                    running = False

        # Spawn new cars randomly
        current_time = time.time()
        if current_time - last_spawn_time >= spawn_interval:
            new_car = spawn_random_car(window_width, window_height)

            if is_spawn_position_clear(new_car, cars):
                cars.append(new_car)
                car_wait[id(new_car)] = {"wait_total": 0.0, "stopped": False, "stop_started": 0.0}
                print(f"Spawned car! Total cars: {len(cars)}")
            else:
                print("Spawn blocked - car already at spawn position")

            last_spawn_time = current_time
            spawn_interval = random.uniform(1, 3)

        # Spawn new pedestrians randomly
        if current_time - last_pedestrian_spawn_time >= pedestrian_spawn_interval:
            new_pedestrian = spawn_test_pedestrian(window_width, window_height)
            pedestrians.append(new_pedestrian)
            print(f"Spawned pedestrian! Total pedestrians: {len(pedestrians)}")

            last_pedestrian_spawn_time = current_time
            pedestrian_spawn_interval = random.uniform(3, 6)

        # Update controller
        sim_data['controller'].update()

        # Update and check all cars
        # Update and check all cars
        for car in cars:
            will_crash_car = False
            will_crash_pedestrian = False

            # Check collision with other cars
            for other_car in cars:
                if car != other_car and car.will_collide_soon(other_car):
                    will_crash_car = True
                    break

            # Check collision with pedestrians
            for pedestrian in pedestrians:
                if car.will_collide_soon(pedestrian):
                    will_crash_pedestrian = True
                    break

            if will_crash_car or will_crash_pedestrian:
                car.stop()
                car.horn(3)
                st = car_wait.get(id(car))
                if st and not st["stopped"]:
                    st["stopped"] = True
                    st["stop_started"] = time.time()

            else:
                current_stop_line = sim_data['stop_lines'][car.direction]
                current_traffic_light = sim_data['traffic_lights'][car.direction]

                if car.check_stop_line(current_stop_line):
                    if current_traffic_light.get_color() == "red":
                        if not car.is_emergency:
                            car.stop()
                            st = car_wait.get(id(car))
                            if st and not st["stopped"]:
                                st["stopped"] = True
                                st["stop_started"] = time.time()

                    else:
                        car.resume()
                        st = car_wait.get(id(car))
                        if st and st["stopped"]:
                            st["wait_total"] += time.time() - st["stop_started"]
                            st["stopped"] = False
                else:
                    car.resume()
                    st = car_wait.get(id(car))
                    if st and st["stopped"]:
                        st["wait_total"] += time.time() - st["stop_started"]
                        st["stopped"] = False

            car.update()
        # Update and check all pedestrians
        for pedestrian in pedestrians:
            will_crash = False

            # Check collision with cars
            for car in cars:
                if pedestrian.will_collide_soon(car):
                    will_crash = True
                    break

            if will_crash:
                pedestrian.stop()
            else:
                pedestrian.resume()

            pedestrian.update()

        # Remove cars that have left the screen
        # In the run_simulation() function, replace the car removal line with:

        # Remove cars that have left the screen
        cars_to_remove = [car for car in cars if is_entity_off_screen(car, window_width, window_height)]
        for car in cars_to_remove:
            cars_crossed += 1

            st = car_wait.get(id(car))
            if st and st["stopped"]:
                st["wait_total"] += time.time() - st["stop_started"]
                st["stopped"] = False

            if car.is_emergency:
                car.stop_siren()
        cars = [car for car in cars if not is_entity_off_screen(car, window_width, window_height)]

        # Remove pedestrians that have left the screen
        peds_to_remove = [ped for ped in pedestrians if is_entity_off_screen(ped, window_width, window_height)]
        peds_crossed += len(peds_to_remove)
        pedestrians = [ped for ped in pedestrians if not is_entity_off_screen(ped, window_width, window_height)]

        # Draw the game
        sim_display.blit(background, (0, 0))

        sim_display.blit(sim_data['line_image'], sim_data['line_north'])
        sim_display.blit(sim_data['line_image'], sim_data['line_south'])
        sim_display.blit(sim_data['line_image_vertical'], sim_data['line_east'])
        sim_display.blit(sim_data['line_image_vertical'], sim_data['line_west'])

        # Draw all cars
        for car in cars:
            car.draw(sim_display)

        # Draw all pedestrians
        for pedestrian in pedestrians:
            pedestrian.draw(sim_display)

        sim_data['traffic_light_north'].draw(sim_display)
        sim_data['traffic_light_south'].draw(sim_display)
        sim_data['traffic_light_east'].draw(sim_display)
        sim_data['traffic_light_west'].draw(sim_display)

        # Draw finish button
        finish_button = Button(image=finish_img, pos=(window_width - 70, 30),
                               text_input="FINISH", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        finish_button.changeColor(MOUSE_POS)
        finish_button.update(sim_display)

        pygame.display.update()

    for car in cars:
        if getattr(car, "is_emergency", False):
            car.stop_siren()

    pygame.mixer.stop()  # stops any remaining sounds (sirens/horns)


    sim_time = time.time() - sim_start_time

    waits = [st["wait_total"] for st in car_wait.values()]
    avg_car_wait = sum(waits) / len(waits) if waits else 0.0

    LAST_STATS = {
        "sim_time": sim_time,
        "cars_crossed": cars_crossed,
        "peds_crossed": peds_crossed,
        "avg_car_wait": avg_car_wait
    }

    # Reset display back to menu size
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Traffic Simulation")
def show_stats():
    global LAST_STATS
    if not LAST_STATS:
        return

    clock = pygame.time.Clock()
    running = True

    while running:
        SCREEN.blit(BG, (0, 0))
        MOUSE_POS = pygame.mouse.get_pos()

        title_font = get_font(50)
        text_font = get_font(20)

        title = title_font.render("STATS", True, "White")
        SCREEN.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, 80)))

        s = LAST_STATS
        lines = [
            f"Simulation time: {s['sim_time']:.1f} s",
            f"Cars crossed: {s['cars_crossed']}",
            f"Pedestrians crossed: {s['peds_crossed']}",
            f"Average car wait: {s['avg_car_wait']:.2f} s",
        ]

        y = 160
        for line in lines:
            txt = text_font.render(line, True, "White")
            SCREEN.blit(txt, (70, y))
            y += 45

        back_button = Button(image=None, pos=(SCREEN_WIDTH / 2, 520),
                             text_input="BACK", font=get_font(50),
                             base_color="#d7fcd4", hovering_color="White")
        back_button.changeColor(MOUSE_POS)
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(MOUSE_POS):
                    running = False

        pygame.display.update()
        clock.tick(60)

def show_menu():
    """Display the main menu"""
    clock = pygame.time.Clock()
    running = True

    while running:
        MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        # Create buttons
        start_button = Button(image=None, pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50),
                              text_input="START", font=get_font(75), base_color="#d7fcd4",
                              hovering_color="White")

        stats_button = Button(image=None, pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150),
                              text_input="STATS", font=get_font(75),
                              base_color="#d7fcd4" if LAST_STATS else "#555555",
                              hovering_color="White")

        quit_button = Button(image=None, pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4",
                             hovering_color="White")

        # Draw buttons
        start_button.changeColor(MOUSE_POS)
        start_button.update(SCREEN)
        stats_button.changeColor(MOUSE_POS)
        stats_button.update(SCREEN)
        quit_button.changeColor(MOUSE_POS)
        quit_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LAST_STATS and stats_button.checkForInput(MOUSE_POS):
                    show_stats()
                if start_button.checkForInput(MOUSE_POS):
                    run_simulation()
                if quit_button.checkForInput(MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    show_menu()