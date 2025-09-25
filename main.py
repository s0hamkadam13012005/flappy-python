import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()

# Load flap sound (must be .wav)
flap_sound = pygame.mixer.Sound(os.path.join("sounds", "wing.wav"))
flap_sound.set_volume(1.0)  # max volume

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Python")

radius = 15
wallW = 90
pipe_img = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")).convert_alpha()
)
bg_img = pygame.transform.scale(
    pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (WIDTH, HEIGHT)
)


class Ball:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.vel = 0
        self.gravity = 0.5
        self.lift = -8

    def jump(self):
        self.vel = self.lift
        flap_sound.play()  # 🔊 play sound here

    def move(self):
        self.vel += self.gravity
        self.y += self.vel
        if self.y > HEIGHT - radius:
            self.y = HEIGHT - radius
            self.vel = 0
        if self.y < radius:
            self.y = radius
            self.vel = 0

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 0), (self.x, int(self.y)), radius)


class Wall:
    GAP = 150

    def __init__(self):
        self.x = WIDTH
        self.h = random.randint(50, HEIGHT - self.GAP - 50)
        self.y = 0
        self.passed = False

    def move(self):
        self.x -= 5

    def draw(self, win):
        # Top pipe
        win.blit(pipe_img, (self.x, self.y - pipe_img.get_height() + self.h))
        # Bottom pipe
        win.blit(pipe_img, (self.x, self.h + self.GAP))

    def collide(self, ball):
        if ball.y - radius < self.h or ball.y + radius > self.h + self.GAP:
            if self.x < ball.x < self.x + wallW:
                return True
        return False


def draw_window(win, ball, walls, score):
    win.blit(bg_img, (0, 0))
    ball.draw(win)
    for wall in walls:
        wall.draw(win)
    score_text = pygame.font.SysFont("comicsans", 40).render(str(score), 1, (255, 255, 255))
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    pygame.display.update()


def main():
    ball = Ball()
    walls = []
    clock = pygame.time.Clock()
    score = 0
    gameStarted = False

    run = True
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            gameStarted = True
            ball.jump()  # 🔊 sound plays inside jump()

        if gameStarted:
            ball.move()
            add_wall = False
            rem = []
            for wall in walls:
                wall.move()
                if wall.collide(ball):
                    run = False
                if not wall.passed and wall.x + wallW < ball.x:
                    wall.passed = True
                    score += 1
                if wall.x + wallW < 0:
                    rem.append(wall)
            if len(walls) == 0 or walls[-1].x < WIDTH - 200:
                walls.append(Wall())
            for r in rem:
                walls.remove(r)

        draw_window(win, ball, walls, score)


main()
