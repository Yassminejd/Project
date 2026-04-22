from pygame import *

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

# Player properties
ZombiePosx = SCREEN_WIDTH // 2 
ZombiePosy = SCREEN_HEIGHT // 2 
ZombieSpeed = 7


CopPosx = 100
CopPosy = 100
CopSpeed = 7
obsPosx = 200
obsPosy = 200
obsSpeed = 5
obs2Posx = 400
obs2Posy = 400
obs2Speed = 5
obs3Posx =700
obs3Posy = 700
obs3Speed = 5





game = True



while game:
    #detect if game ended
    for e in event.get():
        if e.type == QUIT:
            game = False

    #detect keys
    keys = key.get_pressed()
    if keys[K_LEFT] and ZombiePosx > 0:
        ZombiePosx -= ZombieSpeed
    if keys[K_RIGHT] and ZombiePosx < SCREEN_WIDTH - ZombieSize[0]:
        ZombiePosx += ZombieSpeed
    if keys[K_UP] and ZombiePosy > 0:
        ZombiePosy -= ZombieSpeed
    if keys[K_DOWN] and ZombiePosy < SCREEN_HEIGHT - ZombieSize[1]:
        ZombiePosy += ZombieSpeed
        
     
    obsPosx += obsSpeed
    if obsPosx <= 0 or obsPosx >= SCREEN_WIDTH - 150:
        obsSpeed *= -1
    obs2Posy += obs2Speed
    if obs2Posy <= 0 or obs2Posy >= SCREEN_HEIGHT - 150:
        obs2Speed *= -1
    obs3Posy += obs3Speed
    if obs3Posy <= 0 or obs3Posy >= SCREEN_HEIGHT - 150:
        obs3Speed *= -1

    window.blit(background, (0, 0))
    window.blit(Zombie, (ZombiePosx, ZombiePosy))
    window.blit(Cop, (CopPosx, CopPosy))
    window.blit(obs, (obsPosx, obsPosy))
    window.blit(obs2, (obs2Posx, obs2Posy))
    # add the obstacles
    display.update()

