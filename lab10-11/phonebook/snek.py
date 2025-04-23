import pygame
import sys
import copy
import random
import time
import psycopg2

db = psycopg2.connect(dbname='phonebook', user='postgres', password='admin', host='localhost')
current = db.cursor()

print("Enter your name")
name = input()

current.execute("SELECT player_score, player_level FROM Scores WHERE player_name = %s", (name,))
player_data = current.fetchone()

new_player = True

if player_data:
    score = int(player_data[0])
    level = int(player_data[1])
    speed = 10 + (level * 3)  # Adjust speed based on level
    print(f"Welcome back, {name}. Starting at level {level} with score {score}")
    new_player = False
else:
    print(f"New player - {name}.")
    new_player = True


sql="""
    CREATE TABLE IF NOT EXISTS Scores(
        player_name VARCHAR,
        player_score VARCHAR,
        player_level VARCHAR
    );
"""
current.execute(sql)

pygame.init()

if new_player:
    score = 0
    level = 0
    speed = 10
scale = 10

food_x = 10
food_y = 10

screen = pygame.display.set_mode((500, 500), pygame.SHOWN)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

white = (255, 255, 255)
snake_body_color = (0, 255, 0) 
food_color = (255, 0, 0)
snake_head = (0, 200, 0)
font_color = (0, 0, 0)
defeat_color = (255, 0, 0)


class Snake:
    def __init__(self, x_start, y_start):
        self.x = x_start
        self.y = y_start
        self.w = 10
        self.h = 10
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def reset(self):
        self.x = 500 / 2 - scale
        self.y = 500 / 2 - scale
        self.w = 10
        self.h = 10
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def show(self):
        for i in range(self.length):
            if not i == 0:
                pygame.draw.rect(screen, snake_body_color, (self.history[i][0], self.history[i][1], self.w, self.h))
            else:
                pygame.draw.rect(screen, snake_head, (self.history[i][0], self.history[i][1], self.w, self.h))

    def check_eaten(self):
        if abs(self.history[0][0] - food_x) < scale and abs(self.history[0][1] - food_y) < scale:
            return True

    def level(self):
        global level
        if self.length % 5 == 0:
            return True

    def grow(self):
        self.length += 1
        self.history.append(self.history[self.length - 2])

    def death(self):
        i = self.length - 1
        while i > 0:
            if abs(self.history[0][0] - self.history[i][0]) < self.w and abs(
                    self.history[0][1] - self.history[i][1]) < self.h and self.length > 2:
                return True
            i -= 1

    def update(self):
        i = self.length - 1
        while i > 0:
            self.history[i] = copy.deepcopy(self.history[i - 1])
            i -= 1
        self.history[0][0] += self.x_dir * scale
        self.history[0][1] += self.y_dir * scale


class Food:
    def new_location(self):
        global food_x, food_y
        food_x = random.randrange(1, int(500 / scale) - 1) * scale
        food_y = random.randrange(1, int(500 / scale) - 1) * scale

    def show(self):
        pygame.draw.rect(screen, food_color, (food_x, food_y, scale, scale))



def show_score():
    font = pygame.font.SysFont("docker", 20)
    text = font.render("Score: " + str(score), True, font_color)
    screen.blit(text, (scale, scale))


def show_level():
    font = pygame.font.SysFont("docker", 20)
    text = font.render("Level: " + str(level), True, font_color)
    screen.blit(text, (90 - scale, scale))

def show_name():
    font = pygame.font.SysFont("docker", 20)
    text = font.render("Player: " + name, True, font_color)
    screen.blit(text, (350 - scale, scale))




def snake_game():
    global score
    global level
    global speed

    snake = Snake(500 / 2, 500 / 2)
    food = Food()
    food.new_location()

    def defeat(score):
        try:
            current.execute("SELECT player_name FROM Scores WHERE player_name = %s", (name,))
            exists = current.fetchone()
            
            if exists:
                # Update both score and level for existing player
                current.execute("UPDATE Scores SET player_score = %s, player_level = %s WHERE player_name = %s", 
                              (score, level, name))
            else:
                # Insert new record with score and level
                current.execute("INSERT INTO Scores VALUES(%s, %s, %s)", (name, score, level))
            
            db.commit()
        except Exception as e:
            print("Error saving score:", e)
        
        screen.fill(white)
        font1 = pygame.font.SysFont("docker", 100)
        text1 = font1.render("Game Over", True, defeat_color)
        screen.blit(text1, (50, 200))
        pygame.display.update()
        time.sleep(3)
        return True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if snake.y_dir == 0:
                    if event.key == pygame.K_UP:
                        snake.x_dir = 0
                        snake.y_dir = -1
                    if event.key == pygame.K_DOWN:
                        snake.x_dir = 0
                        snake.y_dir = 1

                if snake.x_dir == 0:
                    if event.key == pygame.K_LEFT:
                        snake.x_dir = -1
                        snake.y_dir = 0
                    if event.key == pygame.K_RIGHT:
                        snake.x_dir = 1
                        snake.y_dir = 0

        screen.fill(white)

        snake.show()
        snake.update()
        food.show()
        show_score()
        show_level()
        show_name()

        if snake.check_eaten():
            food.new_location()
            score += random.randint(1, 5)
            snake.grow()
        if snake.level():
            food.new_location()
            level += 1
            speed = 10 + (level * 3) 
            snake.grow()
        if snake.death():
            if defeat(score):
                score = 0
                level = 0
                speed = 10
                snake.reset()
                continue
        if (snake.history[0][0] >= 500 or snake.history[0][0] < 0 or
            snake.history[0][1] >= 500 or snake.history[0][1] < 0):
            if defeat(score):
                score = 0
                level = 0
                speed = 10
                snake.reset()
                continue
        pygame.display.update()
        clock.tick(speed)

if __name__ == "__main__":
    snake_game()
