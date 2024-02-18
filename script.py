import sys
import pygame
import random
import time

# Constants
GAME_FPS = 150
WIDTH, HEIGHT = 1000, 700
JUMPING_HEIGHT = 20
MAX_ACCELERATION = 13
VEL_X = 3
VEL_Y = JUMPING_HEIGHT
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GAMEPLAY_SOUND_LENGTH = 31
SHELVES_COUNT = 500

# Images
BODY_IMAGE = pygame.image.load("Assets/body.png")
BACKGROUND = pygame.image.load("Assets/background.png")
BRICK_IMAGE = pygame.image.load("Assets/brick_block.png")
SHELF_BRICK_IMAGE = pygame.image.load("Assets/shelf_brick.png")
pause_image = pygame.image.load("Assets/pause.png")
resume_image = pygame.image.load("Assets/Resume.png")
nis = pygame.image.load("Assets/nis.png")
nis2 = pygame.image.load("Assets/2nis.png")
nis5 = pygame.image.load("Assets/5nis.png")
nis10 = pygame.image.load("Assets/10nis.png")

# Walls settings
WALLS_Y = -128
WALL_WIDTH = 128
WALLS_ROLLING_SPEED = 2
RIGHT_WALL_BOUND = WIDTH - WALL_WIDTH
LEFT_WALL_BOUND = WALL_WIDTH

# Background settings
BACKGROUND_WIDTH = WIDTH - 2 * WALL_WIDTH
BACKGROUND_ROLLING_SPEED = 1
BACKGROUND_Y = HEIGHT - BACKGROUND.get_height()
background_y = BACKGROUND_Y

# Booleans
jumping = False
falling = False
standing = False
rolling_down = False
new_movement = False
current_direction = None
current_standing_shelf = None

# Colors
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SCORE_COLOR = (255, 255, 255)

# Score Constants
SCORE_FONT = pygame.font.SysFont("Arial", 36)
SCORE_INCREMENT = 10

# Time display constants
TIME_FONT = pygame.font.SysFont("Arial", 24)

class Shelf:
    def __init__(self, number):
        self.number = number
        self.image = None
        self.width = random.randint(4, 7) * 32
        self.x = random.randint(LEFT_WALL_BOUND, RIGHT_WALL_BOUND - self.width)
        self.y = - number * 130 + HEIGHT - 25
        self.rect = pygame.Rect(self.x, self.y, self.width, 32)


class Body:
    def __init__(self):
        self.size = 64
        self.x = WIDTH / 2 - self.size / 2
        self.y = HEIGHT - 25 - self.size
        self.vel_y = 0
        self.acceleration = 0
        self.jumpable = self.vel_y <= 0
        self.score = 0
        self.jumps_left = 2  # Allow two jumps


total_shelves_list = []
for num in range(0, SHELVES_COUNT + 1):
    new_shelf = Shelf(num)
    if num % 50 == 0:
        new_shelf.width = BACKGROUND_WIDTH
        new_shelf.rect.width = BACKGROUND_WIDTH
        new_shelf.x = WALL_WIDTH
        new_shelf.rect.x = WALL_WIDTH
    total_shelves_list.append(new_shelf)

class Body:
    def __init__(self):
        self.size = 64
        self.x = WIDTH / 2 - self.size / 2
        self.y = HEIGHT - 25 - self.size
        self.vel_y = 0
        self.acceleration = 0
        self.jumpable = self.vel_y <= 0
        self.score = 0
        self.jumps_left = 2  # Allow two jumps

# Function to generate coins
def generate_coins():
    for shelf in total_shelves_list:
        if shelf.number % 20 == 0:  # Adjust the frequency of coin appearance
            # Randomly select coin value
            coin_value = random.choice([2, 2, 5, 5, 5, 10])  # Adjust the probability of coin values
            # Randomly select x-coordinate within the shelf
            coin_x = random.randint(shelf.rect.x, shelf.rect.x + shelf.width - 32)
            # Ensure coin y-coordinate is within visible area
            coin_y = max(0, shelf.rect.y - 32)  # Adjust the vertical position as needed
            # Create a new coin object and add it to the list
            coins.append(Coin(coin_value, coin_x, coin_y))

class Coin:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.image = None  # Load appropriate image based on value

    def draw(self):
        # Draw the coin on the screen
        WIN.blit(self.image, (self.x, self.y))
        
# Sounds
JUMPING_SOUND = pygame.mixer.Sound("Assets/jumping_sound.wav")
GAMEPLAY_SOUND = pygame.mixer.Sound("Assets/gameplay_sound.wav")
HOORAY_SOUND = pygame.mixer.Sound("Assets/hooray_sound.wav")


def Move(direction):
    if direction == "Left":
        if body.x - body.acceleration >= LEFT_WALL_BOUND:
            body.x -= body.acceleration
        else:
            body.x = LEFT_WALL_BOUND
    else:
        if body.x + body.acceleration <= RIGHT_WALL_BOUND - body.size:
            body.x += body.acceleration
        else:
            body.x = RIGHT_WALL_BOUND - body.size
    body.acceleration -= 1


def HandleMovement(keys_pressed):
    global body, new_movement, current_direction
    if keys_pressed[pygame.K_LEFT] and body.x > LEFT_WALL_BOUND:
        current_direction = "Left"
        if body.acceleration + 3 <= MAX_ACCELERATION:
            body.acceleration += 3
        else:
            body.acceleration = MAX_ACCELERATION
    if keys_pressed[pygame.K_RIGHT] and body.x < RIGHT_WALL_BOUND:
        current_direction = "Right"
        if body.acceleration + 3 <= MAX_ACCELERATION:
            body.acceleration += 3
        else:
            body.acceleration = MAX_ACCELERATION


def DrawWindow(paused):
    global WALLS_Y
    font = pygame.font.SysFont("Arial", 26)
    HandleBackground()
    for shelf in total_shelves_list:
        for x in range(shelf.rect.x, shelf.rect.x + shelf.width, 32):
            WIN.blit(SHELF_BRICK_IMAGE, (x, shelf.rect.y))
            if shelf.number % 10 == 0 and shelf.number != 0:
                shelf_number = pygame.Rect(shelf.rect.x + shelf.rect.width / 2 - 16, shelf.rect.y,
                                           16 * len(str(shelf.number)), 25)
                pygame.draw.rect(WIN, GRAY, shelf_number)
                txt = font.render(str(shelf.number), True, BLACK)
                WIN.blit(txt, (shelf.rect.x + shelf.rect.width / 2 - 16, shelf.rect.y))

    for y in range(WALLS_Y, HEIGHT, 108):
        WIN.blit(BRICK_IMAGE, (0, y))
        WIN.blit(BRICK_IMAGE, (WIDTH - WALL_WIDTH, y))
    WIN.blit(BODY_IMAGE, (body.x, body.y))
    DrawScore()
    DrawTime(paused)  # Draw elapsed time
    DrawPauseButton(paused)  # Draw pause button
    pygame.display.update()


def OnShelf():
    global jumping, standing, falling, BACKGROUND_ROLLING_SPEED, current_standing_shelf
    if body.vel_y <= 0:
        for shelf in total_shelves_list:
            if body.y <= shelf.rect.y - body.size <= body.y - body.vel_y:
                if body.x + body.size * 2 / 3 >= shelf.rect.x and body.x + body.size * 1 / 3 <= shelf.rect.x + shelf.width:
                    body.y = shelf.rect.y - body.size
                    if current_standing_shelf != shelf.number and shelf.number % 50 == 0 and shelf.number != 0:
                        BACKGROUND_ROLLING_SPEED += 1
                        current_standing_shelf = shelf.number
                    if shelf.number % 100 == 0 and shelf.number != 0:
                        HOORAY_SOUND.play()
                    if shelf.number == SHELVES_COUNT:
                        GameOver()
                    return True
    else:
        jumping, standing, falling = False, False, True


def ScreenRollDown():
    global background_y, WALLS_Y
    for shelf in total_shelves_list:
        shelf.rect.y += 1
    body.y += 1
    background_y += 0.5
    if background_y == BACKGROUND_Y + 164:
        background_y = BACKGROUND_Y
    WALLS_Y += WALLS_ROLLING_SPEED
    if WALLS_Y == 0:
        WALLS_Y = -108


def GameOver():
    global game_over, end_time
    game_over = True
    end_time = time.time()  # Record the end time when the game is over
    pygame.mixer.pause()


def CheckIfTouchingFloor():
    global standing, falling
    if body.y > HEIGHT - body.size:
        if not rolling_down:
            body.y = HEIGHT - body.size
            standing, falling = True, False
        else:
            GameOver()


def HandleBackground():
    if body.y >= total_shelves_list[500].rect.y:
        WIN.blit(BACKGROUND, (32, background_y))


def DrawScore():
    score_text = SCORE_FONT.render("Score: " + str(body.score), True, BLACK)  # Change color to black
    WIN.blit(score_text, (10, 10))


def DrawTime(paused):
    if not paused:  # Only update the timer if the game is not paused
        elapsed_time = round(time.time() - start_time, 2)
        time_text = TIME_FONT.render("Time: " + str(elapsed_time) + "s", True, BLACK)  # Change color to black
        time_rect = time_text.get_rect(midtop=(WIDTH // 2, 70))  # Adjust position below the score
        WIN.blit(time_text, time_rect)


def DrawPauseButton(paused):
    button_image = pause_image if not paused else resume_image
    button_rect = button_image.get_rect(topright=(WIDTH - 10, 10))
    WIN.blit(button_image, button_rect)
    return button_rect  # Return the rectangle of the button for collision detection


def DrawGameOverScreen():
    game_over_font = pygame.font.SysFont("Arial", 48)
    game_over_text = game_over_font.render("Game Over", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    score_text = SCORE_FONT.render("Your Score: " + str(body.score), True, BLACK)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    elapsed_time = round(end_time - start_time, 2)
    time_text = SCORE_FONT.render("Time: " + str(elapsed_time) + "s", True, BLACK)
    time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    play_again_font = pygame.font.SysFont("Arial", 36)
    play_again_text = play_again_font.render("Play Again", True, BLACK)
    play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    WIN.blit(game_over_text, game_over_rect)
    WIN.blit(score_text, score_rect)
    WIN.blit(time_text, time_rect)
    WIN.blit(play_again_text, play_again_rect)
    pygame.display.update()
    return play_again_rect


# Game control variables
game_over = False
game_started = False
start_font = pygame.font.SysFont("Arial", 48)
start_text = start_font.render("Press Space to Start", True, WHITE)
start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
body = Body()
start_time = 0  # Initialize start time variable
end_time = 0  # Initialize end time variable
game_paused = False
pause_button_rect = None  # Initialize pause button rectangle

def ResetGame():
    global body, jumping, standing, falling, rolling_down, game_started, game_over, start_time
    body = Body()
    jumping = False
    standing = False
    falling = False
    rolling_down = False
    game_started = False
    game_over = False
    start_time = 0  # Reset start time
    body.jumps_left = 2  # Reset jumps left to maximum
    pygame.mixer.unpause()
    pygame.mixer.stop()  # Stop any currently playing sounds
    pygame.mixer.Sound.play(GAMEPLAY_SOUND, loops=-1)  # Restart the gameplay sound with looping

def main():
    global body, keys_pressed, total_shelves_list, jumping, standing, falling, rolling_down, game_started, game_over, start_time, end_time
    game_running = True
    rolling_down = False
    sound_timer = 0
    game_paused = False  # Initialize game_paused variable

    while game_running:
        while game_running:
            on_ground = not rolling_down and body.y == HEIGHT - 25 - body.size
            if sound_timer % (56 * GAMEPLAY_SOUND_LENGTH) == 0:
                pygame.mixer.Sound.play(GAMEPLAY_SOUND, loops=-1)  # Restart the gameplay sound with looping
            sound_timer += 1
            if rolling_down:
                for _ in range(BACKGROUND_ROLLING_SPEED):
                    ScreenRollDown()
            if game_over:
                play_again_rect = DrawGameOverScreen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if play_again_rect.collidepoint(event.pos):
                            ResetGame()
                continue
            if not game_started:
                WIN.blit(start_text, start_rect)
                pygame.display.update()
            DrawWindow(game_paused)
            keys_pressed = pygame.key.get_pressed()
            HandleMovement(keys_pressed)
            if body.acceleration != 0:
                Move(current_direction)
            if keys_pressed[pygame.K_SPACE] and (standing or on_ground):
                if not game_started:
                    game_started = True
                    start_time = time.time()  # Record the start time when the game starts
                    continue
                if body.jumps_left > 0:
                    body.vel_y = VEL_Y
                    jumping, standing, falling = True, False, False
                    body.jumps_left -= 1
                    body.score += SCORE_INCREMENT
                    if body.score % 100 == 0:
                        HOORAY_SOUND.play()
            if jumping and body.vel_y >= 0:
                if body.vel_y == VEL_Y:
                    JUMPING_SOUND.play()
                body.y -= body.vel_y
                body.vel_y -= 1
                if body.y <= HEIGHT / 5:
                    rolling_down = True
                    for _ in range(10):
                        ScreenRollDown()
                if not body.vel_y:
                    jumping, standing, falling = False, False, True
                    body.jumps_left = 2
            if falling:
                if OnShelf():
                    jumping, standing, falling = False, True, False
                else:
                    body.y -= body.vel_y
                    body.vel_y -= 1
            CheckIfTouchingFloor()
            if standing and not OnShelf() and not on_ground:
                body.vel_y = 0
                standing, falling = False, True
            if body.acceleration == MAX_ACCELERATION - 1:
                VEL_Y = JUMPING_HEIGHT + 5
            else:
                VEL_Y = JUMPING_HEIGHT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if DrawPauseButton(game_paused).collidepoint(event.pos):  # Check if pause button clicked
                        game_paused = not game_paused  # Toggle game pause state
            if game_paused:
                continue
            pygame.time.Clock().tick(GAME_FPS)


if __name__ == "__main__":
    main()