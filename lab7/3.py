import pygame
import os
import datetime

pygame.init()

done = False
white = (255,255,255)
screen = pygame.display.set_mode((1024,576), pygame.SHOWN)
clock = pygame.time.Clock()
x, y = 512, 288
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 20
    if pressed[pygame.K_DOWN]: y += 20
    if pressed[pygame.K_LEFT]: x -= 20
    if pressed[pygame.K_RIGHT]: x += 20 

    if x > 999: x = 999
    if x < 25: x = 25
    if y < 25: y = 25
    if y > 551: y = 551
    screen.fill(white)
    pygame.draw.circle(screen, (255,0,0), (x, y), 25)

    pygame.display.flip()
    clock.tick(60)