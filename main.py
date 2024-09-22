import pygame
import random
import math

pygame.init()

# INITIALISE WINDOW PROPERTIES
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# PADDLE PROPERTIES
paddle_width = 20
paddle_height = 200
paddle1_y = (screen_height / 2) - (paddle_height / 2)
paddle1_x = 50
paddle2_y = (screen_height / 2) - (paddle_height / 2)
paddle2_x = screen_width - paddle_width - 50
paddle_speed = 10

# BALL PROPERTIES
ball_width = 20
ball_height = 20
ball_y = (screen_height / 2) - (ball_height / 2)
ball_x = (screen_width / 2) - (ball_width / 2)
ball_speed = 15

# SCORE VARIABLES
score1 = 0
score2 = 0

# FONT SETTINGS
font = pygame.font.Font(None, 74)

# Function to calculate a new random angle
def randomize_angle():
    return ((random.random() * 20) - 10) * (math.pi / 180)  # Random angle between -10 to 10 degrees

# Function to calculate new ball speed vector based on current speed and angle
def update_ball_speed_vector(angle):
    ball_xSpeed = math.cos(angle) * ball_speed
    ball_ySpeed = math.sin(angle) * ball_speed
    return [ball_xSpeed, ball_ySpeed]

# Set initial ball angle and speed
ball_angle = randomize_angle()
ball_speed_Vector = update_ball_speed_vector(ball_angle)

# Function to reset the ball to the center after scoring
def reset_ball():
    global ball_x, ball_y, ball_speed_Vector
    ball_x = (screen_width / 2) - (ball_width / 2)
    ball_y = (screen_height / 2) - (ball_height / 2)
    ball_angle = randomize_angle()
    ball_speed_Vector = update_ball_speed_vector(ball_angle)
    pygame.time.delay(500)

# Function to add randomness to the ball's angle when it hits the paddle
# Add a random variation between -10 and 10 degrees to horizontal
def add_randomness_to_angle(current_angle):
    angle_variation = random.uniform(-10, 10) * (math.pi / 180)
    return current_angle + angle_variation

running = True
while running:
    # 'FRAME RATE' SORT OF
    pygame.time.delay(20)

    # ALLOWS THE WINDOW TO BE CLOSED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # PADDLE KEYBOARD CONTROLS
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < screen_height - paddle_height:
        paddle1_y += paddle_speed
    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2_y < screen_height - paddle_height:
        paddle2_y += paddle_speed

    # UPDATE BALL POSITION
    ball_x += ball_speed_Vector[0]
    ball_y += ball_speed_Vector[1]

    # Ball hits the top or bottom of the screen
    if ball_y <= 0 or ball_y >= screen_height - ball_height:
        ball_speed_Vector[1] = -ball_speed_Vector[1]  # Reverse y-direction

    # Ball hits the left paddle
    if paddle1_x < ball_x < paddle1_x + paddle_width:
        if paddle1_y < ball_y < paddle1_y + paddle_height:
            current_angle = math.atan2(ball_speed_Vector[1], -ball_speed_Vector[0])
            current_angle = add_randomness_to_angle(current_angle)
            ball_speed_Vector = update_ball_speed_vector(current_angle)

    # Ball hits the right paddle
    if paddle2_x < ball_x + ball_width < paddle2_x + paddle_width:
        if paddle2_y < ball_y < paddle2_y + paddle_height:
            current_angle = math.atan2(ball_speed_Vector[1], -ball_speed_Vector[0])
            current_angle = add_randomness_to_angle(current_angle)
            ball_speed_Vector = update_ball_speed_vector(current_angle)

    # Ball hits the left or right edge (scoring and ball reset logic)
    if ball_x <= 0:
        score2 += 1  # Player 2 scores
        reset_ball()
    if ball_x >= screen_width - ball_width:
        score1 += 1  # Player 1 scores
        reset_ball()

    # SETS THE SCREEN BACKGROUND TO BLACK
    screen.fill((0, 0, 0))

    # DRAWS THE ELEMENTS
    pygame.draw.rect(screen, (255, 255, 255), (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, (255, 255, 255), (paddle2_x, paddle2_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, (255, 255, 255), (ball_x, ball_y, ball_width, ball_height))

    # DISPLAY SCORE
    score_text1 = font.render(str(score1), True, (255, 255, 255))
    score_text2 = font.render(str(score2), True, (255, 255, 255))
    screen.blit(score_text1, (screen_width // 4, 50))
    screen.blit(score_text2, (screen_width - screen_width // 4, 50))

    pygame.display.update()

pygame.quit()
