import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True
while running:
    #draw all our elements
    #update everything

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()