import pygame
import sys

width , height = 800 , 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Collision detection")

white = (225,225,225)
red = (225,0,0)
blue = (0,0,225)

ball  = pygame.Rect(250,200,20,20)
ball_speed = [3,3]

paddle = pygame.Rect(250,550,100,20)
paddle_speed = 5

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        
    
        
            
            
    pygame.draw.ellipse(screen,red,ball)   
    pygame.draw.rect(screen,blue,paddle)    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
sys.exit()