import pygame
import Car
import TrafficLight
pygame.init()
#the intersection
background = pygame.image.load("assets/intersection.png")

WINDOW_WIDTH,WINDOW_HEIGHT= background.get_width(),background.get_height()
print(WINDOW_WIDTH,WINDOW_HEIGHT)
display = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Traffic Simulation")

running = True
c = Car.Car(WINDOW_WIDTH,WINDOW_HEIGHT,0.1,'N')
traffic_light_south = TrafficLight.TrafficLight(WINDOW_WIDTH,WINDOW_HEIGHT,'S')
traffic_light_north = TrafficLight.TrafficLight(WINDOW_WIDTH,WINDOW_HEIGHT,'N')
traffic_light_east = TrafficLight.TrafficLight(WINDOW_WIDTH,WINDOW_HEIGHT,'E')
traffic_light_west = TrafficLight.TrafficLight(WINDOW_WIDTH,WINDOW_HEIGHT,'W')

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    # draw the game

    display.blit(background, (0, 0))
    c.draw(display)
    c.update()
    traffic_light_north.draw(display)
    traffic_light_south.draw(display)
    traffic_light_east.draw(display)
    traffic_light_west.draw(display)
    pygame.display.update()
pygame.quit()