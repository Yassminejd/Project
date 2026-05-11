from pygame import *
import math # FIX 1: Added this

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
Size = (SCREEN_WIDTH, SCREEN_HEIGHT)

window = display.set_mode(Size)
display.set_caption('Catch Me If You Can')

background = transform.scale(image.load('Background.png'), Size)

ZombieSize  = (150, 200 )
CopSize = (200, 200)

Zombie = transform.scale(image.load('Zombie.png'), ZombieSize)
Cop = transform.scale( image.load('Cop.png') , CopSize )
obs = transform.scale(image.load('obs.png'),(100,100))
obs2 = transform.scale(image.load('obs2.png'),(70,70))
obss = transform.scale(image.load('obs.png'),(100,100))

# Player properties
ZombiePosx = SCREEN_WIDTH // 2 
ZombiePosy = SCREEN_HEIGHT // 2 
ZombieSpeed = 7

# Enemy properties
CopPosx = 100
CopPosy = 100
CopSpeed = 3 # FIX 2: Set a slower speed here

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
angle = 0
clock = time.Clock() # FIX 3: Initialize the clock

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

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
        
    # Cop chasing logic
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

    # Obstacle movement
    obsPosx += obsSpeed
    if obsPosx <= 0 or obsPosx >= SCREEN_WIDTH - 150:
        obsSpeed *= -1
    obs2Posy += obs2Speed
    if obs2Posy <= 0 or obs2Posy >= SCREEN_HEIGHT - 150:
        obs2Speed *= -1
    
    obssPosx += obssSpeed
    if obssPosx <= 0 or obssPosx >= SCREEN_WIDTH - 100:
        obssSpeed *= -1

    # Drawing
    window.blit(background, (0, 0))
    window.blit(transform.rotate(Zombie, angle), (ZombiePosx, ZombiePosy))
    window.blit(obs, (obsPosx, obsPosy))
    window.blit(obs2, (obs2Posx, obs2Posy))
    window.blit(obss, (obssPosx, obssPosy))
    
    # Cop Rotation and Blit
    rotated_cop = transform.rotate(Cop, cop_angle)
    window.blit(rotated_cop, (CopPosx, CopPosy))

    Zombie_rect = Zombie.get_rect(topleft=(ZombiePosx,ZombiePosy))
    Cop_rect = Cop.get_rect(topleft=(CopPosx,CopPosy))
    obss_rect = obss.get_rect(topleft=(obssPosx,obssPosy))
    obs_rect = obs.get_rect(topleft=(obsPosx,obsPosy))

    if Zombie_rect.colliderect(Cop_rect):
        print('caught!')
    if Zombie_rect.colliderect(obs_rect):
        print('hit by the obstacle')
    if Zombie_rect.colliderect(obss_rect):
        print('hit by the obstacle')
    
    










    display.update()