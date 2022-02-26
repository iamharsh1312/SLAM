import pygame

import env
from robots import Mouse, Roomba

environment = env.BuildEnvironment()

running = True

placed = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            environment.robot.position = pygame.mouse.get_pos()
            placed = True
        if not placed:
            continue

    if not pygame.mouse.get_focused():
        continue

    
    environment.iterate()
    environment.render_map()
    environment.update()
    
    pygame.display.update()


environment.save()
pygame.quit()
