import pygame
import sys

pygame.init()

# Window size
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball with Gravity")

# Clock for FPS control
clock = pygame.time.Clock()

# Ball properties
ball_x = width // 2
ball_y = 50
ball_radius = 20
ball_velocity_y = 0

# Physics constants
gravity = 0.5
bounce_factor = -0.8
ground_y = height - ball_radius

running = True
while running:
    # Fill background (light gray)
    screen.fill((225, 225, 225))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics update
    ball_velocity_y += gravity
    ball_y += ball_velocity_y

    # Collision with ground
    if ball_y >= ground_y:
        ball_y = ground_y
        ball_velocity_y *= bounce_factor
        if abs(ball_velocity_y) < 1:
            ball_velocity_y = 0

    # Draw ball
    pygame.draw.circle(screen, (255, 0, 0), (int(ball_x), int(ball_y)), ball_radius)

    # Refresh screen
    pygame.display.flip()
    clock.tick(60)

# Quit safely
pygame.quit()
sys.exit()
