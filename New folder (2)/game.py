from pygame import *

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
Size = (SCREEN_WIDTH, SCREEN_HEIGHT)

window = display.set_mode(Size)
display.set_caption('Catch Me If You Can')

background = transform.scale(image.load('Background.png'), Size)

GuySize  = (150, 200 )
CopSize = (200, 200)

Guy = transform.scale(image.load('Guy.png'), GuySize)
Cop = transform.scale( image.load('Cop.png') , CopSize )
obs = transform.scale(image.load('obs.png'),(150, 150))
obs2 = transform.scale(image.load('obs2.png'),(150, 150))
obs3 = transform.scale(image.load('obs3.png'),(150, 150))

# Player properties
GuyPosx = SCREEN_WIDTH // 2 
GuyPosy = SCREEN_HEIGHT // 2 
GuySpeed = 1


CopPosx = 100
CopPosy = 100
CopSpeed = 1
obsPosx = 200
obsPosy = 200
obs2Posx = 400
obs2Posy = 400
obs3Posx =700
obs3Posy = 700





game = True



while game:
    #detect if game ended
    for e in event.get():
        if e.type == QUIT:
            game = False

    #detect keys
    keys = key.get_pressed()
    if keys[K_LEFT] and GuyPosx > 0:
        GuyPosx -= GuySpeed
    if keys[K_RIGHT] and GuyPosx < SCREEN_WIDTH - GuySize[0]:
        GuyPosx += GuySpeed
    if keys[K_UP] and GuyPosy > 0:
        GuyPosy -= GuySpeed
    if keys[K_DOWN] and GuyPosy < SCREEN_HEIGHT - GuySize[1]:
        GuyPosy += GuySpeed
        

    window.blit(background, (0, 0))
    window.blit(Guy, (GuyPosx, GuyPosy))
    window.blit(Cop, (CopPosx, CopPosy))
    window.blit(obs, (obsPosx, obsPosy))
    window.blit(obs2, (obs2Posx, obs2Posy))
    window.blit(obs3, (obs3Posx, obs3Posy))
    # add the obstacles
    display.update()

