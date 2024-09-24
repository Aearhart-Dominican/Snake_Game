# Pygame Setup
import pygame
import random 
import time

pygame.init()


# Constants
# The rough pixel value of the space consumed by the window and computer headers
DISPLAY_HEADER = 80

# Pulls screen width and adjusts to be a multiple of ten pixels
if pygame.display.Info().current_w % 10 == 0:
    SCREEN_WIDTH = pygame.display.Info().current_w
else:
    SCREEN_WIDTH = pygame.display.Info().current_w \
                   - pygame.display.Info().current_w % 10

# Pulls screen height and adjusts to be a multiple of ten pixels then adds space for header
if pygame.display.Info().current_h % 10 == 0:
    SCREEN_HEIGHT = pygame.display.Info().current_h \
                    - DISPLAY_HEADER
else:
    SCREEN_HEIGHT = pygame.display.Info().current_h \
                    - pygame.display.Info().current_h % 10 \
                    - DISPLAY_HEADER

# Calculates the average size of the screen
SCREEN_AVG = (SCREEN_HEIGHT + SCREEN_WIDTH) // 2

# Stores the center cordinates of the screen in a list
MIDDLE = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Variables
# Colors
BLK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

background_color = (250, 200, 150)
homescreen_color = (253, 189, 255)
options_color = (252, 189, 244)
score_color = BLK

wrap_on = (255, 20, 20)
wrap_off = (20, 255, 20)
wrap_color = wrap_off

ghost_on = (255, 20, 20)
ghost_off = (20, 255, 20)
ghost_color = ghost_off

# External Variables
clicked = False
cell_size = SCREEN_AVG // 50

# Gameloop Variables
reset = True
prev = time.time()
game_speed = .05
menu_speed = .1
food_count = 1
player_count = 1

# Score Variables
high_score = 0
score_cycle = -1
score_timer = time.time()
score_cycle_speed = 2

# Scene Toggles
play_start = True
run_snake = True
show_options = False

# Game Toggles
player_collision = True
wrap = False
ghost_mode_on = False
single_player_mode = True

# Game Options
snake_length = 3
ghost_timer = 50

# Text Size
score_font_size = SCREEN_AVG // 20
if score_font_size > 35:
    score_font_size = 35
elif score_font_size < 5:
    score_font_size = 5

title_font_size =  SCREEN_WIDTH // 10
if title_font_size > 90:
    title_font_size = 90
elif title_font_size < 10:
    title_font_size = 10

# Fonts
score_font = pygame.font.Font("./fonts/Silkscreen/slkscrb.ttf", score_font_size)
title_font = pygame.font.Font("./fonts/Silkscreen/slkscrb.ttf", title_font_size)


# Classes
# Contains the methods and variables for Ghost Mode
class Ghost():
    # Instantiate Ghost object
    def __init__(self):
        self.is_ghost = False
        self.ghost_key = pygame.K_LSHIFT
        self.ghost_time = ghost_timer
        self.ghost_rect = pygame.rect.Rect(0, 0, 0, 0)

    # Ghost Methods
    # Turns ghost mode on or off when ghost key is pressed
    def ghost(self):
        if ghost_mode_on:
            if event.key == self.ghost_key:
                if self.is_ghost:
                    self.is_ghost = False
                    self.ghostify()
                elif snake.ghost_time >= ghost_timer * .25:
                    self.is_ghost = True
                    self.ghostify()

    # Changes snake sprites to reflect ghost mode on or off                 
    def ghostify(self):
        if self.is_ghost:
            self.body = ghost_body
            self.head = ghost_head
            self.tail = ghost_tail
            self.turn = ghost_turn
        else:
            self.body = body
            self.head = head
            self.tail = tail
            self.turn = turn

    # Draws a visual representation of avaliable ghost time
    def draw_ghost_meter(self):
        ghost_meter_color = (255 - int(255 * (self.ghost_time / ghost_timer)), int(255 * (self.ghost_time / ghost_timer)), 0)

        self.ghost_rect.width = cell_size * 3 * (self.ghost_time / ghost_timer)
        pygame.draw.rect(screen, ghost_meter_color, self.ghost_rect)

# Player/Snake class inherits Ghost
class Snake(Ghost):

    # Initialize snake object
    def __init__(self):
        self.snake_pos = [[0, 0, 0, 0]]
        self.name = "Unnamed Snake"
        self.direction = 1
        self.inputdelay = False
        self.up_key = pygame.K_w
        self.down_key = pygame.K_s
        self.left_key = pygame.K_a
        self.right_key = pygame.K_d
        self.game_over = False
        self.score = 0
        self.body = body
        self.head = head
        self.tail = tail
        self.turn = turn
        Ghost.__init__(self)

    # Snake Methods
    # populate snake_pos
    def spawn_snake(self, x, y, len):
        self.add_head(cell_align(x),
                      cell_align(y))

        # Add Body based on passed length
        for i in range(1, len):
            self.add_segment()
            i += 1

    # render snake_pos list
    def draw_snake(self):

        # flag for first segment
        head_drawn = False

        # initialize last rotation
        last_rotation = self.snake_pos[0][3]

        # Render Snake
        for segment in self.snake_pos:

            # Render Snake Body

            # If head is already drawn, draw body
            if head_drawn:

                # If tail, draw tail
                if segment[2] == 3:
                    screen.blit(pygame.transform.rotate(self.tail, self.snake_pos[-2][3]), 
                               (segment[0],
                                segment[1]))
                
                # If same rotation as last piece, draw body
                elif last_rotation == segment[3]:
                    screen.blit(pygame.transform.rotate(self.body, segment[3]), 
                               (segment[0],
                                segment[1]))
                    
                # Draw turn segment based on angle
                else:
                    match segment[3]:
                        case 0:
                            if segment[3] - last_rotation == -90:
                                orient = 180
                            else:
                                orient = 270

                        case 270:
                            if segment[3] - last_rotation == 270:
                                orient = 180
                            else:
                                orient = 270

                        case 180:
                            if segment[3] - last_rotation > 0:
                                orient = 270
                            else:
                                orient = 180

                        case 90:
                            if segment[3] - last_rotation > 0:
                                orient = 270
                            else:
                                orient = 180

                    screen.blit(pygame.transform.rotate(self.turn, (segment[3] + orient) % 360), 
                               (segment[0],
                                segment[1]))

            # Render Snake Head
            elif head_drawn == False:
                screen.blit(pygame.transform.rotate(self.head, segment[3]), 
                           (segment[0],
                            segment[1]))
                head_drawn = True

            # Updates last rotation
            last_rotation = segment[3]

    # set snake head pos
    def add_head(self, cord1, cord2):
        self.snake_pos[0] = [cord1, cord2, 0, 0]

    # append segment to snake
    def add_segment(self):
        # Prime new Segment
        newSegment = list(self.snake_pos[-1])

        # Get snake directions
        match self.snake_pos[-1][3]:
            case 0:
                newSegment[1] += cell_size
            case 180:
                newSegment[1] -= cell_size
            case 270:
                newSegment[0] -= cell_size
            case 90:
                newSegment[0] += cell_size

        # Sets sets old tail to body
        if self.snake_pos[-1][2] == 3:
            self.snake_pos[-1][2] = 2
        
        # Sets new segment to tail
        newSegment[2] = 3

        # Add Segment
        self.snake_pos.append(newSegment)

    # read user input to set direction
    def set_direction(self):

        # Check for first input only
        if self.inputdelay == False:
            # Read key to determine direction and block illegal moves
            if event.key == self.up_key:
                if self.direction !=2:
                    self.direction = 1
                    self.inputdelay = True
            elif event.key == self.down_key:
                if self.direction !=1:
                    self.direction = 2
                    self.inputdelay = True
            elif event.key == self.right_key:
                if self.direction != 4:
                    self.direction = 3
                    self.inputdelay = True
            elif event.key == self.left_key:
                if self.direction != 3:
                    self.direction = 4
                    self.inputdelay = True

    # moves head in direction, moves segments to follow
    def move_snake(self):
            
            # Set tail to body segment to avoid visual issues
            self.snake_pos[-1][2] = 2

            # Shift all segments to next segment in snake_pos
            self.snake_pos = self.snake_pos[-1:] + self.snake_pos[:-1]

            # Move snake head in direction
            if self.direction == 1:
                self.snake_pos[0][0] = self.snake_pos[1][0]
                self.snake_pos[0][1] = self.snake_pos[1][1] - cell_size
                self.snake_pos[0][3] = 0
            elif self.direction == 2:
                self.snake_pos[0][0] = self.snake_pos[1][0]
                self.snake_pos[0][1] = self.snake_pos[1][1] + cell_size
                self.snake_pos[0][3] = 180
            elif self.direction == 3:
                self.snake_pos[0][1] = self.snake_pos[1][1]
                self.snake_pos[0][0] = self.snake_pos[1][0] + cell_size
                self.snake_pos[0][3] = 270
            elif self.direction == 4:
                self.snake_pos[0][1] = self.snake_pos[1][1]
                self.snake_pos[0][0] = self.snake_pos[1][0] - cell_size
                self.snake_pos[0][3] = 90

            # Set final segment to tail
            self.snake_pos[-1][2] = 3

            # Allow New Inputs
            self.inputdelay = False
            # Check if Snake lost
            self.check_game_over()

    # check game over condition and return flag
    def check_game_over(self):
    
        # Check for active ghosting
        if self.is_ghost == False:
            # Check for if players can collide
            if player_collision:
                # Get snakes head position
                head = [self.snake_pos[0][0], self.snake_pos[0][1]]

                # Check if snake head collides with any snake segment
                for snake in players:
                    head_count = 0
                    for segment in snake.snake_pos:
                        if head == [segment[0], segment[1]] and head_count > 0 and snake.is_ghost == False:
                            # Snake hit something
                            self.game_over = True
                        head_count += 1
            else:
                # Check if snake collides with itself
                head_count = 0
                for segment in self.snake_pos:
                    if [self.snake_pos[0][0], self.snake_pos[0][1]] == [segment[0], segment[1]] and head_count > 0:
                        # Snake hit itself
                        self.game_over = True
                    head_count += 1

        # Check if Snake will wrap window
        if wrap:
            # Set head to mirrored x, y position
            if self.snake_pos[0][0] < 0:
                self.snake_pos[0][0] += cell_align(SCREEN_WIDTH) + cell_size
            elif self.snake_pos[0][0] >= cell_align(SCREEN_WIDTH) + cell_size:
                self.snake_pos[0][0] -= cell_align(SCREEN_WIDTH) + cell_size
            elif self.snake_pos[0][1] < 0:
                self.snake_pos[0][1] += cell_align(SCREEN_HEIGHT) + cell_size
            elif self.snake_pos[0][1] >= cell_align(SCREEN_HEIGHT) + cell_size:
                self.snake_pos[0][1] -= cell_align(SCREEN_HEIGHT) + cell_size
        else:
            if self.snake_pos[0][0] < 0 \
               or self.snake_pos[0][0] > cell_align(SCREEN_WIDTH) \
               or self.snake_pos[0][1] < 0 \
               or self.snake_pos[0][1] > cell_align(SCREEN_HEIGHT):
                    # Snake hit a border
                    self.game_over = True

# Food info and generation methods
class Food:
    # Food initialization
    def __init__(self):
        self.food = [0, 0]
        self.new_food = True

    # Food Methods
    # Create a new food object
    def make_food(self):
        if self.new_food:
            self.new_food = False
            self.food[0] = cell_size * random.randint(0, int(SCREEN_WIDTH / cell_size) - 1)
            self.food[1] = cell_size * random.randint(0, int(SCREEN_HEIGHT / cell_size) - 1)
    
    # Draws food sprite on screen
    def draw_food(self):
        screen.blit(apple, (self.food[0], self.food[1]))
        
    # Check if snake head collides with food and moves food    
    def food_eaten(self, snake):
        if self.food[0] == snake.snake_pos[0][0] and self.food[1] == snake.snake_pos[0][1]:
            self.new_food = True
            snake.add_segment()
            snake.score += 1
    

# Setup Functions

def draw_screen(color):
    screen.fill(color)

# Adjust integer to be a multiple of cell size
def cell_align(int):
    int = int // cell_size * cell_size

    return int

# Create a sprite with transparent background
def make_img(link):
    img = pygame.image.load(link).convert()
    img.set_colorkey(BLK)
    return img

# Generate text as an array of [renderd text, rectangle centered around text]
def make_text(text, font_size, x, y, color = BLK, font = "./fonts/Silkscreen/slkscr.ttf"):
    text_info = []

    text_font = pygame.font.Font(font, font_size)
    text_rend = text_font.render(text, True, color)
    text_rect = text_rend.get_rect(center = (x, y))
    text_info = [text_rend, text_rect]

    return text_info

# Game Functions
# makes a decending list of items
def gen_text_list(textlist, size, x, y, color = BLK, font = "./fonts/Silkscreen/slkscr.ttf"):
    new_textlist = []

    # Create text and coordinates start
    text_font = pygame.font.Font(font, size)
    text_rend = text_font.render(textlist[0], True, color)
    text_rect = text_rend.get_rect(center = (x, y))
    new_textlist.append([text_rend, text_rect])

    textlist.remove(textlist[0])

    # Create the rest of the text off of start coordinates
    for text in textlist:
        text_font = pygame.font.Font(font, size)
        text_rend = text_font.render(text, True, color)
        text_rect = text_rend.get_rect(center = (x, new_textlist[-1][1].y + new_textlist[-1][1].height * 2))
        new_textlist.append([text_rend, text_rect])
    
    return new_textlist

# Creates a list of instructions and coordinates for the home screen to auto populate
def gen_instructions(textlist):
    # Text details
    font = "./fonts/Silkscreen/slkscr.ttf"
    size_ratio = 3
    new_instructions = []

    # Create text and coordinates start
    text_font = pygame.font.Font(font, title_font_size // size_ratio)
    text_rend = text_font.render(textlist[0], True, title_font_size)
    text_rect = text_rend.get_rect(center = (SCREEN_WIDTH // 2, title_rect.bottom + title_rect.height // 3))
    new_instructions.append([text_rend, text_rect])

    textlist.remove(textlist[0])

    # Create the rest of instructions off of start coordinates
    for text in textlist:
        text_font = pygame.font.Font(font, title_font_size // size_ratio)
        text_rend = text_font.render(text, True, title_font_size)
        text_rect = text_rend.get_rect(center = (SCREEN_WIDTH // 2, new_instructions[-1][1].y + new_instructions[-1][1].height * 2))
        new_instructions.append([text_rend, text_rect])
    
    return new_instructions

# Creates new Snakes based on player count
def gen_players(player_count):

    players = []

    # Generate snake and segments with regard to other snakes
    for i in range(player_count):
        # Make new Snake object and add to list
        players.append(Snake())
        # Create new snakes head position based on amount of snakes
        x = cell_align(((SCREEN_WIDTH // (player_count * 2)) * (i + i + 1)))

        # Create player name based on number of snakes
        players[-1].name = "Player " + str(i + 1)
        # Populate new snake's snake pos list
        players[-1].spawn_snake(x, SCREEN_HEIGHT // 2, snake_length)

        # Sets the position and size of each snakes ghost mode meter
        if ghost_mode_on:
            players[-1].ghost_rect = pygame.rect.Rect(players[-1].snake_pos[0][0],
                                                      SCREEN_HEIGHT - cell_size * 2,
                                                      cell_size * 3,
                                                      cell_size // 2)
            players[-1].ghost_rect.center = (players[-1].snake_pos[0][0] + cell_size // 2, SCREEN_HEIGHT - cell_size)

    # Assign Player 2 controls
    if len(players) > 1:
        players[1].up_key = pygame.K_UP
        players[1].down_key = pygame.K_DOWN
        players[1].left_key = pygame.K_LEFT
        players[1].right_key = pygame.K_RIGHT
        players[1].ghost_key = pygame.K_RSHIFT

    return players

# Creates new Food based on food count
def gen_food(food_count):

    food = []

    for i in range(food_count):
        food.append(Food())
    
    return food

# Displays the score of the current selected player and the High Score onto screen
def draw_score():
    if len(players) > 0:
        score_display = score_font.render(f"{players[score_cycle].name}'s Score: {players[score_cycle].score}", True, (score_color))
    else:
        score_display = score_font.render("Score: 0", True, (score_color))

    screen.blit(score_display, (0, 0))
    screen.blit(high_score_display, (0, score_font_size))

# Displays the GAME OVER text and Play Again? option on screen
def draw_gameover():
    gameover =  make_text("GAME OVER", title_font_size * 2, MIDDLE[0], int(SCREEN_HEIGHT * .25))
    screen.blit(gameover[0], gameover[1])

    pygame.draw.rect(screen, (200, 200, 200), play[1])
    screen.blit(play[0], play[1])

# Function Dependent Variables
# Score Text
high_score_display = score_font.render(f"High Score: {high_score}", True, (score_color))

# Homescreen Text
home_title = title_font.render("Python Snake", True, title_font_size)
title_rect = home_title.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 10))

instructions = gen_instructions(["Press Any Key To Start",
                                 "Press H for Home",
                                 "Press R for Restart",
                                 "Press L or Esc to Leave"])

options = make_text("Options", title_font_size // 3, int(SCREEN_WIDTH * .9), SCREEN_HEIGHT - 2 * cell_size)

# Gamemode Text
inf_mode = make_text("Infinite Mode", title_font_size // 2, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
ghost_mode = make_text("Ghost Mode", title_font_size // 2, SCREEN_WIDTH // 4 * 3, SCREEN_HEIGHT // 2)

# Game Over Text
play =  make_text("Play Again?", int(title_font_size * .75), MIDDLE[0], MIDDLE[1])

# Option Screen Text
options_title = make_text("Options", title_font_size, MIDDLE[0], 2 * cell_size)
controls_title = make_text("Controls", int(title_font_size * .7), MIDDLE[0], 22 * cell_size)
selector = make_text("X", title_font_size // 2, int(SCREEN_WIDTH * .3) - cell_size, 18 * cell_size)
back = make_text("Back", title_font_size // 3, int(SCREEN_WIDTH * .9), SCREEN_HEIGHT - 2 * cell_size)

# Food option and increment text
food_text = make_text("Food Count", title_font_size // 2, MIDDLE[0], 6 * cell_size)
food_count_add = make_text(">", title_font_size // 3, MIDDLE[0] + 2 * cell_size, 7.5 * cell_size)
food_count_subtract = make_text("<", title_font_size // 3, MIDDLE[0] - 2 * cell_size, 7.5 * cell_size)
food_count_add_big = make_text(">>", title_font_size // 3, MIDDLE[0] + 4 * cell_size, 7.5 * cell_size)
food_count_subtract_big = make_text("<<", title_font_size // 3, MIDDLE[0] - 4 * cell_size, 7.5 * cell_size)

# Collision Text
player_collision_text = make_text("Player Collision", title_font_size // 2, MIDDLE[0], 12 * cell_size)

# Player Amount Text
single_player = make_text("Single Player", title_font_size // 2, int(SCREEN_WIDTH * .3), 17 * cell_size)
two_player = make_text("Two Player", title_font_size // 2, int(SCREEN_WIDTH * .7), 17 * cell_size)

# Player Control List
player_one_controls = [f"PLAYER 1", f"Up: W", f"Down: S", f"Left: A", f"Right: D", f"Ghost: LShift"]
player_one_controls_text = gen_text_list(player_one_controls, title_font_size // 3, int(SCREEN_WIDTH * .3), 24 * cell_size)
player_two_controls = [f"PLAYER 2", f"Up: Up Arrow", f"Down: Down Arrow", f"Left: Left Arrow", f"Right: Right Arrow", f"Ghost: RShift"]
player_two_controls_text = gen_text_list(player_two_controls, title_font_size // 3, int(SCREEN_WIDTH * .7), 24 * cell_size)

# Sprite Initialization
body = pygame.transform.scale(make_img("./sprites/body.png"), (cell_size, cell_size))
head = pygame.transform.scale(make_img("./sprites/head.png"), (cell_size, cell_size))
tail = pygame.transform.scale(make_img("./sprites/tail.png"), (cell_size, cell_size))
turn = pygame.transform.scale(make_img("./sprites/turn.png"), (cell_size, cell_size))

ghost_body = pygame.transform.scale(make_img("./sprites/ghost_body.png"), (cell_size, cell_size))
ghost_head = pygame.transform.scale(make_img("./sprites/ghost_head.png"), (cell_size, cell_size))
ghost_tail = pygame.transform.scale(make_img("./sprites/ghost_tail.png"), (cell_size, cell_size))
ghost_turn = pygame.transform.scale(make_img("./sprites/ghost_turn.png"), (cell_size, cell_size))

apple = pygame.transform.scale(make_img("./sprites/Abble.png"), (cell_size, cell_size))

# Game Condition
running = True

# Game Loop
while running:
    
    # Homescreen Display
    while play_start:
        # Limits Loop Executions for efficiency
        if time.time() - prev > game_speed:
            prev = time.time()
                
            draw_screen(homescreen_color)

            # Display Title
            screen.blit(home_title, title_rect)

            # Display Game Options
            pygame.draw.rect(screen, wrap_color, inf_mode[1])
            screen.blit(inf_mode[0], inf_mode[1])
            pygame.draw.rect(screen, ghost_color, ghost_mode[1])
            screen.blit(ghost_mode[0], ghost_mode[1])

            screen.blit(options[0], options[1])

            # Display Game Instructions
            for instrution in instructions:
                screen.blit(instrution[0], instrution[1])

            # Event Handler
            for event in pygame.event.get():

                # Allow close window with exit button
                if event.type == pygame.QUIT:
                    play_start = False
                    run_snake = False
                    running = False
                
                # Start game on key press
                if event.type == pygame.KEYDOWN:
                    play_start = False
                    run_snake = True

                    # Exit game from homescreen
                    if event.key == pygame.K_l or event.key == pygame.K_ESCAPE:
                        run_snake = False
                        running = False

                    if event.key == pygame.K_o:
                        play_start = False
                        show_options = True
                        run_snake = False

                # Check for mouse click
                if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                    clicked = True
                if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                    clicked = False
                    # Get mouse position
                    pos = pygame.mouse.get_pos()
                    # Check if mouse clicked on game option and toggle it
                    if inf_mode[1].collidepoint(pos):
                        if wrap:
                            wrap = False
                            wrap_color = wrap_off
                        else:
                            wrap = True
                            wrap_color = wrap_on
                    if ghost_mode[1].collidepoint(pos):
                        if ghost_mode_on:
                            ghost_mode_on = False
                            ghost_color = ghost_off
                        else:
                            ghost_mode_on = True
                            ghost_color = ghost_on
                    if options[1].collidepoint(pos):
                        play_start = False
                        show_options = True
                        run_snake = False

            pygame.display.update()

    # Options Screen
    while show_options:
        # Limits Loop Executions for efficiency
        if time.time() - prev > game_speed:
            prev = time.time()

            draw_screen(options_color)
            # Display Page Headers
            screen.blit(options_title[0], options_title[1])
            screen.blit(controls_title[0], controls_title[1])
            screen.blit(back[0], back[1])

            # Display Options
            # Food add and subtract text, controls, and outlines
            screen.blit(food_text[0], food_text[1])
            food_count_text = make_text(str(food_count), title_font_size // 3, MIDDLE[0], 7.5 * cell_size)
            screen.blit(food_count_text[0], food_count_text[1])
            pygame.draw.rect(screen, BLK, food_count_add[1], 2)
            screen.blit(food_count_add[0], food_count_add[1])
            pygame.draw.rect(screen, BLK, food_count_subtract[1], 2)
            screen.blit(food_count_subtract[0], food_count_subtract[1])
            pygame.draw.rect(screen, BLK, food_count_add_big[1], 2)
            screen.blit(food_count_add_big[0], food_count_add_big[1])
            pygame.draw.rect(screen, BLK, food_count_subtract_big[1], 2)
            screen.blit(food_count_subtract_big[0], food_count_subtract_big[1])

            # Collsion Text and Selector
            screen.blit(player_collision_text[0], player_collision_text[1])
            if player_collision:
                selector[1].center = (MIDDLE[0] - cell_size * 12, 12 * cell_size)
                screen.blit(selector[0], selector[1])

            # Player Amount Options
            screen.blit(single_player[0], single_player[1])
            screen.blit(two_player[0], two_player[1])

            # Player Mode Selector
            if single_player_mode:
                selector[1].center = (int(SCREEN_WIDTH * .3) - cell_size * 11, 17 * cell_size)
                screen.blit(selector[0], selector[1])
            else:
                selector[1].center = (int(SCREEN_WIDTH * .7) - cell_size * 9, 17 * cell_size)
                screen.blit(selector[0], selector[1])
            
            # Player Controls
            for control in player_one_controls_text:
                screen.blit(control[0], control[1])
            for control in player_two_controls_text:
                screen.blit(control[0], control[1])

            # Event Handler
            for event in pygame.event.get():

                # Allow close window with exit button
                if event.type == pygame.QUIT:
                    show_options = False
                    play_start = False
                    run_snake = False
                    running = False
                
                # Start game on key press
                if event.type == pygame.KEYDOWN:

                    # Exit game from homescreen
                    if event.key == pygame.K_l:
                        play_start = False
                        show_options = False
                        run_snake = False
                        running = False

                    if  event.key == pygame.K_ESCAPE or event.key == pygame.K_DELETE or event.key == pygame.K_b:
                        show_options = False
                        run_snake = False
                        play_start = True

                # Check for mouse click
                if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                    clicked = True
                if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                    clicked = False
                    # Get mouse position
                    pos = pygame.mouse.get_pos()
                    # Check if mouse clicked on game option and toggle it
                    if back[1].collidepoint(pos):
                        play_start = True
                        show_options = False
                        run_snake = False

                    # Add or Subract Food Value
                    if food_count_add[1].collidepoint(pos):
                        food_count += 1
                    if food_count_add_big[1].collidepoint(pos):
                        food_count += 5
                    if food_count_subtract[1].collidepoint(pos):
                        if food_count > 1:
                            food_count -= 1
                    if food_count_subtract_big[1].collidepoint(pos):
                        if food_count > 5:
                            food_count -= 5

                    # Turn on and off Collision
                    if player_collision_text[1].collidepoint(pos):
                        if player_collision:
                            player_collision = False
                        else:
                            player_collision = True

                    # Turn On Single or Two Player
                    if single_player[1].collidepoint(pos):
                        single_player_mode = True
                        player_count = 1
                    if two_player[1].collidepoint(pos):
                        single_player_mode = False
                        player_count = 2

            pygame.display.update()

    # Snake Game Loop
    while run_snake:
        # Snake Update Timer (removes FPS Dependence)
        if time.time() - prev > game_speed:
            prev = time.time()

            # Reset Variables for Quick Restart
            if reset:
                players = gen_players(player_count)
                food = gen_food(food_count)
                reset = False

            draw_screen(background_color)
        
            # Render Snakes and update High Score
            for snake in players:
                # Update High Score
                if snake.score > high_score:
                    high_score = snake.score
                    high_score_display = score_font.render(f"High Score {snake.name}: {high_score}", True, (score_color))

                # Draw Ghost mode meters for snakes
                if ghost_mode_on:
                    snake.draw_ghost_meter()

                snake.draw_snake()

            # Event Handler
            for event in pygame.event.get():

                # Allow close window with exit button
                if event.type == pygame.QUIT:
                    run_snake = False
                    running = False
                
                # Read Key Presses
                if event.type == pygame.KEYDOWN:

                    for snake in players:
                        # Set Snake directions
                        snake.set_direction()

                        # Set Ghost Mode if snake's ghost key is pressed
                        snake.ghost()
                        
                    # Initiate Reset
                    if event.key == pygame.K_r:
                        reset = True 
                    
                    # Return to Homescreen
                    if event.key == pygame.K_h:
                        reset = True 
                        play_start = True
                        run_snake = False
                    
                    # Leave Game
                    if event.key == pygame.K_l or event.key == pygame.K_ESCAPE:
                        run_snake = False
                        running = False 

                # Check for mouse click
                if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                    clicked = True
                if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                    clicked = False
                    # Get mouse position
                    pos = pygame.mouse.get_pos()
                    # Check for clicked Play Again and restart
                    if play[1].collidepoint(pos) and players[0].game_over:
                        reset = True
                            
            # Moves All Snakes
            for snake in players:
                # Checks for Game Over Condition
                if snake.game_over:
                    if len(players) > 1:
                        players.remove(snake)

                else:
                    snake.move_snake()
                    
                    # Lowers or refills Ghost Meter based on use
                    if ghost_mode_on:
                        if snake.is_ghost:
                            if snake.ghost_time > 0:
                                snake.ghost_time -= 1
                            else:
                                snake.is_ghost = False
                                snake.ghostify()
                        elif snake.ghost_time < ghost_timer:
                            snake.ghost_time += 1

            # Updates Score to Display next Player
            if len(players) > 1:
                if time.time() - score_timer > score_cycle_speed:
                    score_timer = time.time()
                    score_cycle = (score_cycle + 1) % len(players)
            else:
                score_cycle = 0

            draw_score()

            # Food Handler
            for num in food:
                num.make_food()
                num.draw_food()

                # Check if Snake ate Food
                for snake in players:
                    num.food_eaten(snake)

            # Check for Game Over
            if len(players) < 2 and players[0].game_over:
                draw_gameover()

            # Refresh the Screen
            pygame.display.update()

# Program End
pygame.quit()