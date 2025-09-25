import pygame
import sys
pygame.init()

width , height = 800 , 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Collision detection")

white = (225,225,225)
red = (225,0,0)
blue = (0,0,225)
black = (0,0,0)

ball  = pygame.Rect(250,200,20,20)
ball_speed = [3,3]

paddle = pygame.Rect(250,550,100,20)
paddle_speed = 5

score = 0
level = 1
next_level = 5

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)


running = True
while running:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left>0:
        paddle.x -=paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < width:
        paddle.x += paddle_speed
        
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]
    
    if ball.left <= 0 or ball.right >= width: # remember or in this line im forgetting it
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = - ball_speed[1]
        
    if ball.colliderect(paddle) and ball_speed[1] > 0:
        ball_speed[1] = -ball_speed[1]
        score += 1
        
    if score >= next_level:
        level += 1
        
        ball_speed[0] *= 1.2
        ball_speed[1] *= 1.2
        next_level += 5

    
        
    if ball.bottom >= height:
        running = False
        print("Game Over")
        
    score_text = font.render(f"Score: {score}  Level: {level}", True, black)
    
    screen.blit(score_text, (10, 10))
        
            
            
    pygame.draw.ellipse(screen,red,ball)   
    pygame.draw.rect(screen,blue,paddle)    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
sys.exit()

