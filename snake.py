# Pygame Setup
import pygame, random

pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Variables
bgColor = (250, 200, 150)
cell_size = 10
bodyOuter = (100, 100, 200)
bodyInner = (50, 175, 25)
headColor = (70,200, 25)
update_snake = 0
foodColor = (200, 20, 15)
score = 0
font = pygame.font.SysFont(None, 40)
score_color = (0, 0, 0)
gameOver = False
againRect = pygame.Rect(SCREEN_WIDTH // 2 -80, SCREEN_HEIGHT // 2, 160, 50)
clicked = False
highScore = 0

# 1 for up, 2 for down, 3 for right, 4 for left
direction = 1 


# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Functions
def draw_screen():
    screen.fill(bgColor)

def draw_snake():

    head = 1

    for x in snake_pos:
        if head == 0:
            pygame.draw.rect(screen, bodyOuter, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, bodyInner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))

        elif head == 1:
            pygame.draw.rect(screen, bodyOuter, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, headColor, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
            head = 0

def set_direction():
    global direction

    if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != 2:
        direction = 1
    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != 1:
        direction = 2
    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != 4:
        direction = 3
    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != 3:
        direction = 4

def move_snake():
        global snake_pos
        snake_pos = snake_pos[-1:] + snake_pos[:-1]

        if direction == 1:
            snake_pos[0][0] = snake_pos[1][0]
            snake_pos[0][1] = snake_pos[1][1] - cell_size
        elif direction == 2:
            snake_pos[0][0] = snake_pos[1][0]
            snake_pos[0][1] = snake_pos[1][1] + cell_size
        elif direction == 3:
            snake_pos[0][1] = snake_pos[1][1]
            snake_pos[0][0] = snake_pos[1][0] + cell_size
        elif direction == 4:
            snake_pos[0][1] = snake_pos[1][1]
            snake_pos[0][0] = snake_pos[1][0] - cell_size

def draw_score():
    score_txt = "Score: " + str(score)
    score_img = font.render(score_txt, True, score_color)
    screen.blit(score_img, (0,25))

    highScore_txt = "High Score: " + str(highScore)
    highScore_img = font.render(highScore_txt, True, score_color)
    screen.blit(highScore_img, (0,0))

def check_gameOver(gameOver):
    
    # has snake hit itself
    head_count = 0
    for segment in snake_pos:
        if snake_pos[0] == segment and head_count > 0:
            gameOver = True
        head_count += 1

    # wall collision
    if snake_pos[0][0] < 0 or snake_pos[0][0] > SCREEN_WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] > SCREEN_HEIGHT:
        gameOver = True

    return gameOver

def draw_gameover():
    over_txt = "Game Over"
    over_img = font.render(over_txt, True, score_color)
    pygame.draw.rect(screen, (200, 0, 10), (SCREEN_WIDTH // 2 -80, SCREEN_HEIGHT // 2 - 60, 160, 50))
    screen.blit(over_img, (SCREEN_WIDTH // 2 -80, SCREEN_HEIGHT // 2 - 50))

    again_txt = "Play Again?"
    again_img = font.render(again_txt, True, score_color)
    pygame.draw.rect(screen, (10, 200, 10), againRect)
    screen.blit(again_img, (SCREEN_WIDTH // 2 -80, SCREEN_HEIGHT // 2 + 10))
    
def reset():
    global score
    global direction
    global update_snake 
    global gameOver
    global food
    global newFood
    global newSegment
    global snake_pos

    score = 0
    direction = 1
    update_snake = 0
    gameOver = False
    food = [0, 0]
    newFood = True
    newSegment = [0, 0]

    snake_pos = [[int(SCREEN_WIDTH) / 2, SCREEN_HEIGHT / 2]]
    snake_pos.append([int(SCREEN_WIDTH) / 2, SCREEN_HEIGHT / 2 + cell_size])
    snake_pos.append([int(SCREEN_WIDTH) / 2, SCREEN_HEIGHT / 2 + cell_size * 2])
    snake_pos.append([int(SCREEN_WIDTH) / 2, SCREEN_HEIGHT / 2 + cell_size * 3])

# Snake
snake_pos = [[int(SCREEN_WIDTH) / 2, SCREEN_HEIGHT / 2]]
snake_pos.append([int(SCREEN_WIDTH) / 2, SCREEN_HEIGHT / 2 + cell_size])
snake_pos.append([int(SCREEN_WIDTH) / 2, SCREEN_HEIGHT / 2 + cell_size * 2])
snake_pos.append([int(SCREEN_WIDTH) / 2, SCREEN_HEIGHT / 2 + cell_size * 3])

# Food
food = [0, 0]
newFood = True
newSegment = [0, 0]


running = True
while running:

    draw_screen()
    draw_score()

    for event in pygame.event.get():

        # Exit condition
        if event.type == pygame.QUIT:
            running = False

        # key press -> move snake
        elif event.type == pygame.KEYDOWN:
            set_direction()
            if event.key == pygame.K_r:
                reset()

    # Food
    if newFood:
        newFood = False
        food[0] = cell_size * random.randint(0, int(SCREEN_WIDTH / cell_size) - 1)
        food[1] = cell_size * random.randint(0, int(SCREEN_HEIGHT / cell_size) - 1)
    
    pygame.draw.rect(screen, foodColor, (food[0], food[1], cell_size, cell_size))

    # Food collision
    if snake_pos[0] == food:
        newFood = True
        score += 1

        # increase snake size
        newSegment = list(snake_pos[-1])
        if direction == 1:
            newSegment[1] += cell_size
        elif direction == 2:
            newSegment[1] -= cell_size
        elif direction == 3:
            newSegment[0] -= cell_size
        elif direction == 4:
            newSegment[0] += cell_size

        snake_pos.append(newSegment)

    if score > highScore:
        highScore = score

    if gameOver == False:
        # Snake
        if update_snake > 99:
            update_snake = 0
            move_snake()

        gameOver = check_gameOver(gameOver)

    elif gameOver:
        draw_gameover()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()
            if againRect.collidepoint(pos):
                reset()


    draw_snake()


    # Refresh screen
    pygame.display.update()

    update_snake += 1

# End program
pygame.quit()