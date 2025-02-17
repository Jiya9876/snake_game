import pygame
from pygame.locals import *
import random

pygame.init()

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
grey = (199, 192, 192)
green = (51, 102, 0)
light_green = (102, 204, 0)  # New color when score > 10
yellow = (255, 255, 0)

# Window
win_width = 600
win_height = 400
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Snake Game")

# Snake settings
snake_block = 10
snake_speed = 10
clock = pygame.time.Clock()

# Fonts
font_style = pygame.font.SysFont("Verdana", 25)
score_font = pygame.font.SysFont("comicsans", 30)

def user_score(score):
    number = score_font.render(f"Score: {score}", True, red)
    window.blit(number, [10, 10])

def game_snake(snake_length_list, score):
    color = light_green if score > 10 else green  # Change color if score > 10
    for x in snake_length_list:
        pygame.draw.rect(window, color, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    text = font_style.render(msg, True, color)
    window.blit(text, [win_width / 16, win_height / 3])

def game_loop():
    gameOver = False
    gameClose = False
    pause = False  # Pause state
    speed = snake_speed  # Initial speed

    x1, y1 = win_width // 2, win_height // 2
    x1_change, y1_change = 0, 0

    snake_length_list = []
    snake_length = 1

    foodx = round(random.randrange(0, win_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, win_height - snake_block) / 10.0) * 10.0

    while not gameOver:
        while gameClose:
            window.fill(grey)
            message("You lost! Press P to play again or Q to quit.", red)
            user_score(snake_length - 1)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = True
                        gameClose = False
                    if event.key == pygame.K_p:
                        game_loop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFT and x1_change == 0:
                    x1_change, y1_change = -snake_block, 0
                if event.key == K_RIGHT and x1_change == 0:
                    x1_change, y1_change = snake_block, 0
                if event.key == K_UP and y1_change == 0:
                    x1_change, y1_change = 0, -snake_block
                if event.key == K_DOWN and y1_change == 0:
                    x1_change, y1_change = 0, snake_block
                if event.key == K_SPACE:
                    pause = not pause  # Toggle pause state
        
        while pause:
            message("Game Paused. Press Space to Resume", red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                    pause = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        pause = False
        
        x1 += x1_change
        y1 += y1_change

        if x1 >= win_width or x1 < 0 or y1 >= win_height or y1 < 0:
            gameClose = True

        window.fill(grey)
        pygame.draw.rect(window, yellow, [foodx, foody, snake_block, snake_block])

        snake_size = [x1, y1]
        snake_length_list.append(snake_size)
        if len(snake_length_list) > snake_length:
            del snake_length_list[0]

        # Check if snake collides with itself
        for block in snake_length_list[:-1]:
            if block == [x1, y1]:
                gameClose = True

        game_snake(snake_length_list, snake_length - 1)
        user_score(snake_length - 1)
        pygame.display.update()

        # Check if snake eats the food
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(0, win_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, win_height - snake_block) / 10.0) * 10.0
            snake_length += 1

            # Increase speed if score > 10
            if snake_length - 1 > 10:
                speed += 1

        clock.tick(speed)
    
    pygame.quit()
    quit()

game_loop()
