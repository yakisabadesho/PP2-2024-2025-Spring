import pygame, sys
import os
import random, time


pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("C:/Users/yakisoba/Desktop/WORKSPACE/lab8-9/background.wav")  # BGM
pygame.mixer.music.set_volume(1)
crash_sound = pygame.mixer.Sound("C:/Users/yakisoba/Desktop/WORKSPACE/lab8-9/crash.wav")

font = pygame.font.SysFont("docker", 72)
small_font = pygame.font.SysFont("docker", 28)
done = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400,600), pygame.SHOWN)
pygame.display.set_caption("Racer")
white = (255,255,255)
red = (255, 0, 23)
score = 0
background = pygame.image.load("C:/Users/yakisoba/Desktop/WORKSPACE/lab8-9/AnimatedStreet.png")
coin_png = pygame.image.load("C:/Users/yakisoba/Desktop/WORKSPACE/lab8-9/coin.png")

class Enemy(pygame.sprite.Sprite): #Hostile cars
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Users/yakisoba/Desktop/WORKSPACE/lab8-9/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 400-40), 0)
    def move(self):
        global score
        global spawnpos
        self.rect.move_ip(0,speed)
        if (self.rect.bottom > 900):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
            score += 1
        spawnpos = self.rect.center
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite): #Player character
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("C:/Users/yakisoba/Desktop/WORKSPACE/lab8-9/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
 
    def update(self):
        pressed = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed[pygame.K_LEFT] and pressed[pygame.K_LSHIFT]:
                self.rect.move_ip(-10, 0)
        if self.rect.right < 400:        
            if pressed[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)
            if pressed[pygame.K_RIGHT] and pressed[pygame.K_LSHIFT]:
                self.rect.move_ip(10,0)
    def draw(self, surface):
        surface.blit(self.image, self.rect)  

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.respawn()
        
    def respawn(self): #Respawns coins after picking them up
        global coinsize
        coinsize = random.randint(15, 60)
        self.image = pygame.transform.scale(coin_png, (coinsize, coinsize))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 370), 0)
    def move(self):
        self.rect.move_ip(0,speed)
        if (self.rect.bottom > 900):
            self.respawn() 
    def draw(self, surface):
        surface.blit(self.image, self.rect)

P1 = Player()
E1 = Enemy()
C1 = Coin()

spawnpos = 0

coinsize = 0

coin_score = 0

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

gamestate = "game" # Flag to determine if it should display the gameplay or the game over screen
coin_number = 0
speed = 2
y = 0
mode = "vincible"

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and gamestate == "gameover": # Lets you restart after you crashed and resets the values
            gamestate = "game"
            speed = 2 
            score = 0 
            coin_score = 0
            coin_number = 0
            E1.rect.center = (random.randint(30, 370), 0) 
            P1.rect.center = (160, 520)
            C1.rect.center = (random.randint(30, 370), 0)
            spawnpos = E1.rect.center
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LALT and gamestate == "game": # Turns invincibility on and off
            if mode == "vincible":
                mode = "invincible"
            elif mode == "invincible":
                mode = 'vincible'

    if gamestate == "game":
        if not pygame.mixer.music.get_busy(): 
            pygame.mixer.music.play(-1)
        P1.update() # Lets the player move
        E1.move() # Moves the cars
        C1.move() # Moves the coins

        screen.blit(background, (0,y)) # Moving background
        screen.blit(background, (0,y-600))
        if y > 600:
            y = 0
        else:
            y += speed
        print(y, speed,coinsize) # Debug

        P1.draw(screen)
        E1.draw(screen)
        C1.draw(screen)

        screen.blit(font.render(str(score), True, (0,0,0)), (10,10)) # Cars passed score
        screen.blit(font.render(str(coin_score), True, (255,215,0)), (300, 10))
        
        if pygame.sprite.spritecollideany(P1, enemies) and mode != "invincible": # Sends the player to the gameover screen
            gamestate = "gameover"
            crash_sound.play()
        if pygame.sprite.spritecollideany(P1, coins): # Picking up the coins
            C1.respawn()
            coin_number += 1
            coin_score += coinsize/10
            if coin_number % 3 == 0: # Increases the speed every time the player earns 5 coins
                speed += 1
    
    if gamestate == "gameover": # Game over screen
        pygame.mixer.music.stop()
        screen.fill(red)
        screen.blit(font.render("GAME OVER", True, (255,255,255)), (50, 260))
        screen.blit(small_font.render("Press SPACE to restart", True, (255,255,255)), (95, 320)) # Prompt to restart
        screen.blit(small_font.render(f"Score: {score} | Coin score: {coin_score}", True, (255,255,255)), (100, 230)) #Displays score and money earned



    pygame.display.flip()
    clock.tick(60) #fps limit

