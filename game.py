from pygame import *
import math 
from random import randint 

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
Size = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Made the icons even larger (400x400 pixels)
IconSize = (300, 300)

window = display.set_mode(Size)
display.set_caption('Catch Me If You Can')

background = transform.scale(image.load('Background.png'), Size)

ZombieSize = (150, 200)
CopSize = (200, 200)

Zombie = transform.scale(image.load('Zombie.png'), ZombieSize)
Cop = transform.scale(image.load('Cop.png'), CopSize)
obs = transform.scale(image.load('obs.png'), (100, 100))
obs2 = transform.scale(image.load('obs2.png'), (70, 70))
obss = transform.scale(image.load('obs.png'), (100, 100))

healthImg = transform.scale(image.load('health.png'), IconSize)
moneyImg = transform.scale(image.load('money.png'), IconSize)
scoreImg = transform.scale(image.load('score.png'), IconSize)
gunsImg = transform.scale(image.load('guns.png'), IconSize)

mouse.set_visible(False)

# Player properties (Using float/center tracking makes movement smoother)
ZombiePosx = SCREEN_WIDTH // 2 
ZombiePosy = SCREEN_HEIGHT // 2 
ZombieSpeed = 7
angle = 0

# Enemy properties
CopPosx = 100
CopPosy = 100
CopSpeed = 3 

obsPosx = 200
obsPosy = 200
obsSpeed = 5
obs2Posx = 400
obs2Posy = 400
obs2Speed = 5
obssPosx = 200
obssPosy = 600   
obssSpeed = 5

game = True
clock = time.Clock() 

while game:
    clock.tick(60)

    for e in event.get():
        if e.type == QUIT:
            game = False

    # 1. Input & Player Movement
    keys = key.get_pressed()
    if keys[K_LEFT] and ZombiePosx > 0:
        ZombiePosx -= ZombieSpeed
        angle = -180
    if keys[K_RIGHT] and ZombiePosx < SCREEN_WIDTH - ZombieSize[0]:
        ZombiePosx += ZombieSpeed
        angle = 0
    if keys[K_UP] and ZombiePosy > 0:
        ZombiePosy -= ZombieSpeed
        angle = 90
    if keys[K_DOWN] and ZombiePosy < SCREEN_HEIGHT - ZombieSize[1]:
        ZombiePosy += ZombieSpeed
        angle = -90
        
    # 2. Cop chasing logic
    dx = ZombiePosx - CopPosx
    dy = ZombiePosy - CopPosy
    
    rad_angle = math.atan2(-dy, dx)
    cop_angle = math.degrees(rad_angle)

    if CopPosx < ZombiePosx:
        CopPosx += CopSpeed
    elif CopPosx > ZombiePosx:
        CopPosx -= CopSpeed

    if CopPosy < ZombiePosy:
        CopPosy += CopSpeed
    elif CopPosy > ZombiePosy:
        CopPosy -= CopSpeed

    # 3. Obstacle movement
    obsPosx += obsSpeed
    if obsPosx <= 0 or obsPosx >= SCREEN_WIDTH - 100: # Adjusted bounding box limit
        obsSpeed *= -1
    obs2Posy += obs2Speed
    if obs2Posy <= 0 or obs2Posy >= SCREEN_HEIGHT - 70: # Adjusted bounding box limit
        obs2Speed *= -1
    
    obssPosx += obssSpeed
    if obssPosx <= 0 or obssPosx >= SCREEN_WIDTH - 100:
        obssSpeed *= -1

    # 4. Setup rectangles BEFORE drawing to detect screen shake status
    Zombie_rect = Zombie.get_rect(topleft=(ZombiePosx, ZombiePosy))
    Cop_rect = Cop.get_rect(topleft=(CopPosx, CopPosy))
    obs_rect = obs.get_rect(topleft=(obsPosx, obsPosy))
    obs2_rect = obs2.get_rect(topleft=(obs2Posx, obs2Posy)) 
    obss_rect = obss.get_rect(topleft=(obssPosx, obssPosy))

    is_colliding = (Zombie_rect.colliderect(Cop_rect) or 
                    Zombie_rect.colliderect(obs_rect) or 
                    Zombie_rect.colliderect(obs2_rect) or 
                    Zombie_rect.colliderect(obss_rect))

    # 5. Drawing Section
    # Calculate screen shake offset up front
    shake_x = randint(-5, 5) if is_colliding else 0
    shake_y = randint(-5, 5) if is_colliding else 0

    window.blit(background, (shake_x, shake_y))
    
    # Rotate characters properly around their center points
    rotated_zombie = transform.rotate(Zombie, angle)
    zombie_rot_rect = rotated_zombie.get_rect(center=Zombie_rect.center)
    window.blit(rotated_zombie, zombie_rot_rect)
    
    rotated_cop = transform.rotate(Cop, cop_angle)
    cop_rot_rect = rotated_cop.get_rect(center=Cop_rect.center)
    window.blit(rotated_cop, cop_rot_rect)

    # Draw Obstacles & UI
    window.blit(obs, (obsPosx, obsPosy))
    window.blit(obs2, (obs2Posx, obs2Posy))
    window.blit(obss, (obssPosx, obssPosy))
    
    # Aligned tightly on the same side (bottom-left)
    padding = 10
    window.blit(healthImg, (10, SCREEN_HEIGHT - IconSize[1] - 5))
    window.blit(gunsImg, (10 + (IconSize[0] + padding), SCREEN_HEIGHT - IconSize[1] - 5))
    window.blit(moneyImg, (10 + 2 * (IconSize[0] + padding), SCREEN_HEIGHT - IconSize[1] - 5))
    window.blit(scoreImg, (10 + 3 * (IconSize[0] + padding), SCREEN_HEIGHT - IconSize[1] - 5))
    
    # Apply full-screen red flash damage effect
    if is_colliding:
        red = Surface(Size, SRCALPHA)
        red.fill((255, 0, 0, 80))
        window.blit(red, (0, 0))
        
        if Zombie_rect.colliderect(Cop_rect):
            print('caught!')
        else:
            print('hit by an obstacle')
    
    display.update()