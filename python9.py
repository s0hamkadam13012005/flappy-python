import pygame, random, sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Ball - Multi Level")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Colors
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
BLACK = (0, 0, 0)

# Player setup
player = pygame.Rect(WIDTH//2 - 50, HEIGHT - 30, 100, 20)

# Ball setup
ball = pygame.Rect(random.randint(0, WIDTH-20), 0, 20, 20)
ball_speed = 5

score = 0
level = 1
game_over = False

def reset():
    global score, level, ball_speed, game_over
    score = 0
    level = 1
    ball_speed = 5
    ball.x = random.randint(0, WIDTH-20)
    ball.y = 0
    game_over = False

while True:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not game_over:
        # Move player
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 7
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += 7

        # Move ball
        ball.y += ball_speed
        if ball.y > HEIGHT:
            game_over = True

        # Collision
        if player.colliderect(ball):
            score += 1
            ball.x = random.randint(0, WIDTH-20)
            ball.y = 0

            # Level up every 5 points
            if score % 5 == 0:
                level += 1
                ball_speed += 2

        # Draw
        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.ellipse(screen, RED, ball)
        score_text = font.render(f"Score: {score}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

    else:
        # Game over screen
        over_text = font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to Restart", True, BLACK)
        final_score = font.render(f"Final Score: {score}  Level: {level}", True, BLACK)
        screen.blit(over_text, (WIDTH//2 - 100, HEIGHT//2 - 60))
        screen.blit(final_score, (WIDTH//2 - 150, HEIGHT//2 - 20))
        screen.blit(restart_text, (WIDTH//2 - 150, HEIGHT//2 + 20))

        if keys[pygame.K_r]:
            reset()

    pygame.display.flip()
    clock.tick(30)
