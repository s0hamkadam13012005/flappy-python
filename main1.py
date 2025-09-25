import pygame
import sys
import random
import os
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Python")

radius = 15
wallW = 90
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (WIDTH, HEIGHT))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha(), (WIDTH, 50))

font = pygame.font.SysFont("Arial", 35)   # for score display

# ---------------- Wall ----------------
class Wall:
    GAP = 190
    VEL = 4

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.opositY = self.y + self.h + self.GAP
        self.opositH = HEIGHT - (self.y + self.h + self.GAP)
        self.image = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha(), (wallW, self.h)), 
            180
        )
        self.op_image = pygame.transform.scale(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha(), (wallW, self.opositH))
        self.top = self.h - self.image.get_height()
        self.bottom = self.h + self.GAP
        self.passed = False
    
    def draw(self, win):
        win.blit(self.op_image, (self.x, self.opositY))
        win.blit(self.image, (self.x, self.y))

    def move(self, lastWall):
        self.x -= self.VEL
        if self.x + self.w + self.GAP <= 0:
            self.__init__(lastWall.x + random.randint(250, 400), 0, wallW, random.randint(60, HEIGHT - 65 - Wall.GAP))

# ---------------- Bird ----------------
class Ball:
    VEL = 10
    y_vel = 0
    GRAVITY = 0.8
    anim = 0
    count = 0
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.image = bird_images[0]
    def move(self):
        if self.y_vel <= 8:
            self.y_vel += self.GRAVITY
        self.y += self.y_vel 
    def animate(self):
        if self.anim >= 19:
            self.anim = 0
            self.count = (self.count + 1) % len(bird_images)
            self.image = bird_images[self.count]
        else:
            self.anim += 1
    def jump(self):
        self.y_vel = -self.VEL 
    def collide(self, walls):
        # bottom hit
        if self.y + self.image.get_height() >= HEIGHT - 30:
            return True
        for wall in walls:
            bird_mask = pygame.mask.from_surface(self.image)
            top_mask = pygame.mask.from_surface(wall.image)
            bottom_mask = pygame.mask.from_surface(wall.op_image)
            top_offset = (wall.x - self.x, wall.top - round(self.y))
            bottom_offset = (wall.x - self.x, wall.bottom - round(self.y))
            if bird_mask.overlap(top_mask, top_offset) or bird_mask.overlap(bottom_mask, bottom_offset):
                return True
        return False
    def draw(self, win):
        self.animate()
        rotated_image = pygame.transform.rotate(self.image, -self.y_vel * 3)
        new_rect = rotated_image.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

# ---------------- Helper funcs ----------------
def generateWalls():
    walls = []
    for i in range(5):
        walls.append(Wall(WIDTH + i * 400 - wallW, 0, wallW, random.randint(60, HEIGHT - 65 - Wall.GAP)))
    return walls

def gameLogic(ball, walls, score):
    ball.move()
    for wall in walls:
        wall.move(max(walls, key=lambda w: w.x))
        if not wall.passed and wall.x + wall.w < ball.x:
            wall.passed = True
            score += 1
    return score

def draw(win, ball, walls, score, level):
    win.blit(bg_img, (0, 0))
    win.blit(base_img, (0, HEIGHT - 30))
    ball.draw(win)
    for wall in walls:
        wall.draw(win)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 200, 0))
    win.blit(score_text, (10, 10))
    win.blit(level_text, (10, 50))
    pygame.display.flip()

def showGameOver(win, score):
    win.blit(bg_img, (0,0))
    text = font.render("GAME OVER", True, (255,0,0))
    score_text = font.render(f"Final Score: {score}", True, (255,255,255))
    restart_text = font.render("Press R to Restart or ESC to Quit", True, (200,200,200))
    win.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 60))
    win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    win.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
    pygame.display.flip()

# ---------------- Main ----------------
def main():
    clock = pygame.time.Clock()
    run_game = True

    while run_game:
        ball = Ball(100, HEIGHT // 2, radius, "red")
        walls = generateWalls()
        score = 0
        level = 1
        Wall.VEL = 4
        Wall.GAP = 190
        gameStarted = False
        running = True

        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_SPACE]:
                gameStarted = True
                ball.jump()

            if not gameStarted:
                draw(win, ball, walls, score, level)
                continue

            # game logic
            score = gameLogic(ball, walls, score)

            # level up
            if score > 0 and score % 5 == 0:
                level = score // 5 + 1
                Wall.VEL = 4 + level
                Wall.GAP = max(120, 190 - (level*10))

            # collision
            if ball.collide(walls):
                running = False
                break

            # draw
            draw(win, ball, walls, score, level)

        # game over screen
        showGameOver(win, score)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                waiting = False   # restart loop
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
