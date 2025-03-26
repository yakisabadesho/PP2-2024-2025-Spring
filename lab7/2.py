import pygame
import os
from mutagen.mp3 import MP3

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((576,762), pygame.SHOWN)
done = False
white = (255,255,255)
path = "C:/Users/yakisoba/Desktop/WORKSPACE"
gamestate = "menu"
font = pygame.font.SysFont("timesnewroman", 12)
selection = 0
song_list = [f for f in os.listdir(path) if f.endswith("mp3")]
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and selection != num_elements - 1 :
            selection += 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and selection != 0:
            selection -= 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and gamestate == "menu":
            gamestate = "song"
    screen.fill(white)
    y = 8
    top = 0
    num_elements = 0
    if gamestate == "menu":
        for filename in os.listdir(path):
            if filename.endswith(".mp3"):
                hour = 0
                minute = 0
                second = 0
                file = MP3(os.path.join(path, filename))
                pygame.draw.rect(screen, (128,128,128),(0,top,576,30), 2)
                length = int(file.info.length)
                hour = (length//3600)
                minute = (length%3600)//60
                second = length % 60
                screen.blit(font.render(f"{str(filename)} | {(hour)}:{(minute)}:{(second)}", True, (0, 0, 0)), (5, y))
                y += 28
                top += 28
                num_elements += 1
                pygame.draw.rect(screen,(255,0,0),(0,selection * 28,576,30), 3)
    if gamestate == "song":
        placeholder = 0
    pygame.display.flip()
    clock.tick(60)