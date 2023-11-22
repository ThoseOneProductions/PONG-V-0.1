import pygame
import sys
import random


# Game constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 80
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize Pygame and font
pygame.init()
pygame.font.init()
pygame.mixer.init()  # Added for sound
font = pygame.font.Font(None, 72)

# Load sounds
paddle_hit_sound = pygame.mixer.Sound(r'PONG2023-V1/hit.wav')

# Load background music and play it
pygame.mixer.music.load(r'PONG2023-V1/goodlife.mp3')
pygame.mixer.music.play(-1)  # -1 makes it loop forever

# Load score sound effect
score_sound = pygame.mixer.Sound(r'PONG2023-V1/oof_2.wav')




# Load ball image
brother_face = pygame.image.load(r'PONG2023-V1/Mistiko_Ball_1.png')
brother_face = pygame.transform.scale(brother_face, (BALL_RADIUS * 4, BALL_RADIUS * 4))

# Game objects
ball = pygame.Rect(WIDTH // 3, HEIGHT // 3, BALL_RADIUS * 3, BALL_RADIUS * 3)
paddle1 = pygame.Rect(0, HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(WIDTH - PADDLE_WIDTH, HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Scores
score_left = 0
score_right = 0

# Physics
ball_dx = ball_dy = -3
paddle1_dy = paddle2_dy = 4

# Game states
MAIN_MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
state = MAIN_MENU

# Volume control
volume = 0.5
is_dragging = False

# Pygame screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if WIDTH - 130 <= event.pos[0] <= WIDTH - 30 and HEIGHT - 30 <= event.pos[1] <= HEIGHT - 10:
                is_dragging = True  # Start dragging

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_dragging = False  # Stop dragging

        elif event.type == pygame.MOUSEMOTION and is_dragging:
            if WIDTH - 130 <= event.pos[0] <= WIDTH - 30:
                volume = (event.pos[0] - (WIDTH - 130)) / 100
                pygame.mixer.music.set_volume(volume)

        # Event handler to switch between states
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == MAIN_MENU:
                    state = PLAYING
                elif state == PLAYING:
                    state = PAUSED
                elif state == PAUSED:
                    state = PLAYING

    if state == PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1.y -= paddle1_dy
        if keys[pygame.K_s]:
            paddle1.y += paddle1_dy
        if keys[pygame.K_UP]:
            paddle2.y -= paddle2_dy
        if keys[pygame.K_DOWN]:
            paddle2.y += paddle2_dy

        # Update ball and paddle positions
        ball.x += ball_dx
        ball.y += ball_dy
        if paddle1.top < 0:
            paddle1.top = 0
        if paddle1.bottom > HEIGHT:
            paddle1.bottom = HEIGHT
        if paddle2.top < 0:
            paddle2.top = 0
        if paddle2.bottom > HEIGHT:
            paddle2.bottom = HEIGHT

        if ball.top < 0 or ball.bottom > HEIGHT:
            ball_dy *= -1

        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_dx *= -1
            paddle_hit_sound.play()

        if ball.left < 0:
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_dx *= -1
            score_right += 1
            score_sound.play()

        if ball.right > WIDTH:
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_dx *= -1
            score_left += 1
            score_sound.play()

        if ball.colliderect(paddle1):
            ball_dx = abs(ball_dx)
        elif ball.colliderect(paddle2):
            ball_dx = -abs(ball_dx)

        if paddle1.bottom > HEIGHT:
            paddle1.bottom = HEIGHT
        if paddle1.top < 0:
            paddle1.top = 0
        if paddle2.bottom > HEIGHT:
            paddle2.bottom = HEIGHT
        if paddle2.top < 0:
            paddle2.top = 0

    screen.fill(BLACK)  # Clear the screen at the start of each frame

    if state == MAIN_MENU:
        title_surface = font.render("PONG 2023", True, YELLOW)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 2 - title_surface.get_height() // 2))
        start_surface = font.render("Press SPACEBAR to start", True, WHITE)
        screen.blit(start_surface, (WIDTH // 2 - start_surface.get_width() // 2, HEIGHT // 2 + title_surface.get_height() // 2 + 50))

    # Render the game objects (paddles, ball, scores)
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    
    # Draw the image instead of the ball
    screen.blit(brother_face, ball.topleft)

    # Draw scores
    score_left_surface = font.render(str(score_left), True, WHITE)
    score_right_surface = font.render(str(score_right), True, WHITE)
    screen.blit(score_left_surface, (WIDTH // 2 - 100, 50))
    screen.blit(score_right_surface, (WIDTH // 2 + 50, 50))

    # Volume slider
    pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH - 130, HEIGHT - 30, 100, 20))
    pygame.draw.rect(screen, RED, pygame.Rect(WIDTH - 130, HEIGHT - 30, int(volume * 100), 20))

    pygame.display.flip()
    clock.tick(FPS)
