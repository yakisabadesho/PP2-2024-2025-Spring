import pygame
import random

pygame.init()
white = (255, 255, 255)
red = (255, 0, 0)
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
snake = [(300, 200)]
direction = (1, 0)
apple = (random.randrange(0, 600, 20), random.randrange(0, 400, 20))
done = False
gamestate = "signin"
font = pygame.font.SysFont("docker", 72)
small_font = pygame.font.SysFont("docker", 28)
sign_text = ''
signbox_active = False
input_box = pygame.Rect(200, 150,215, 30)
black = (0,0,0)
lightblue = (173, 216, 230)
signbox_color = black
color = (0,0,0)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0,1):
                direction = (0,-1)
            elif event.key == pygame.K_DOWN and direction != (0,-1):
                direction = (0,1)
            elif event.key == pygame.K_LEFT and direction != (1,0):
                direction = (-1,0)
            elif event.key == pygame.K_RIGHT and direction != (-1,0):
                direction = (1,0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and gamestate == "gameover": # lets you restart after you failed
            snake = [(600 // 2, 400 // 2)]
            direction = (1, 0)
            apple = (random.randrange(0, 600, 20), random.randrange(0, 400, 20))
            gamestate = "game"

        if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
            if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                signbox_active = not signbox_active
            else:
                signbox_active = False
                # Change the current color of the input box.
                
        if event.type == pygame.KEYDOWN and gamestate == 'signin':
            if signbox_active:
                if event.key == pygame.K_RETURN:
                    if sign_text == 'soba':
                        gamestate = "game"
                elif event.key == pygame.K_BACKSPACE:
                    sign_text = sign_text[:-1]
                else:
                    sign_text += event.unicode

    if gamestate == "game":
        screen.fill(white)
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0] * 20, head_y + direction[1] * 20)
    
        if (new_head in snake or new_head[0] < 0 or new_head[0] >= 600 or new_head[1] < 0 or new_head[1] >= 400):
            gamestate = "gameover"
            continue
        snake.insert(0, new_head)
        if new_head == apple: #checks for apples
            apple = (random.randrange(0, 600, 20), random.randrange(0, 400, 20))
        else:
            snake.pop()

        pygame.draw.rect(screen, (255, 0, 0), (apple[0], apple[1], 20, 20)) # apples
        for i, segment in enumerate(snake): # drawing the snake
            if i == 0:
                color = (0, 200, 0)
            else:
                color = (0, 255, 0) 
            pygame.draw.rect(screen, color, (segment[0], segment[1], 20, 20))
    if gamestate == "gameover":
        screen.fill(red)
        screen.blit(font.render("GAME OVER", True, (255,255,255)), (150, 100))
        screen.blit(small_font.render("Press SPACE to restart", True, (255,255,255)), (195, 180)) # Prompt to restart
    if gamestate == "signin":
        screen.fill(white)
        screen.blit(small_font.render("username", True, (0,0,0)), (260,120))
        txt_surface = small_font.render(sign_text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, signbox_color, input_box, 3)
        if signbox_active:
            signbox_color = lightblue
        else:
            signbox_color = black
    pygame.display.flip()
    clock.tick(10)

