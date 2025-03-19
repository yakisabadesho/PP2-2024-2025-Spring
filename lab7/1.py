import pygame
import datetime
import os
import math

image_library = {}

def rotate(image, pivot, r):
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(r) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
    origin = (pivot[0] + min_box[0], pivot[1] - max_box[1])
    return origin

def get_image(path):
    global image_library
    image = image_library.get(path)
    if image == None:
        canonicalized_path = path.replace("/", os.sep).replace("\\",os.sep)
        image = pygame.image.load(canonicalized_path)
        image_library[path] = image
    return image

# C:/Users/yakisoba/Desktop/WORKSPACE

pygame.init()
offset = (100, 0)
ha = 0
ma = 0
font = pygame.font.SysFont("timesnewroman", 36)
orig_hour_png = pygame.transform.scale(get_image("C:/Users/yakisoba/Desktop/WORKSPACE/hour.png"), (20, 95))
hour_png = pygame.transform.rotate(orig_hour_png, 220)
face_png = get_image("C:/Users/yakisoba/Desktop/WORKSPACE/face.png")
orig_minute_png = pygame.transform.scale(get_image("C:/Users/yakisoba/Desktop/WORKSPACE/minute.png"), (24,120))
minute_png = pygame.transform.rotate(orig_minute_png, 220)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024,576), pygame.SHOWN)
done = False
white = (255,255,255)
pivot = (525, 291)
while not done:
    now = datetime.datetime.now().time()
    hour = now.hour % 12
    minute = now.minute
    second = now.second
    microsecond = now.microsecond
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(white)
    rot_hour_png = pygame.transform.rotate(hour_png, ha)
    rot_minute_png = pygame.transform.rotate(minute_png, ma)
    origin_h = rotate(hour_png, pivot, ha)
    origin_m = rotate(minute_png, pivot, ma)

    screen.blit(face_png, (345, 110))
    screen.blit(rot_hour_png, origin_h) # 514 209
    screen.blit(rot_minute_png, origin_m) # 511 180
    ha = 139 - (int(30 * hour)+ int((1/2) * minute)) - int(second * ((1/2)/60)) 
    print(ha)
    ma = 139 - (6 * minute) - int(6/60 * second)
    pygame.draw.circle(screen, (0, 0, 0), pivot, 12)
    mousepos = pygame.mouse.get_pos()
    screen.blit(font.render(str(mousepos), True, (0,0,0)), (50, 50))
    pygame.display.flip()
    clock.tick(60)    