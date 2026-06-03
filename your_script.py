from pygame import *
import math
from random import randint 
import json
import os

# --- JSON High Score Systems ---
HIGH_SCORE_FILE = "highscore.json"

def load_high_score():
    """Loads the high score from a JSON file, or returns 0 if it doesn't exist."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                data = json.load(f)
                return data.get("highscore", 0)
        except Exception as e:
            print(f"Error loading high score: {e}")
            return 0
    return 0

def save_high_score(current_score):
    """Saves the high score to a JSON file if the current score is higher."""
    global high_score
    if current_score > high_score:
        high_score = current_score
    
    try:
        data = {"highscore": high_score}
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving high score: {e}")

# Initialize high score from file immediately
high_score = load_high_score()

# Initialize pygame fonts
font.init()
font_large = font.SysFont('Arial', 60, bold=True)
font_small = font.SysFont('Arial', 30, bold=True)

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
Size = (SCREEN_WIDTH, SCREEN_HEIGHT)
IconSize = (100, 100) 

window = display.set_mode(Size)
display.set_caption('Catch Me If You Can')

def load_safely(filename, size, color_fallback):
    """Safely loads an image. If the file is missing, returns a colored box fallback so the game doesn't crash."""
    try:
        return transform.scale(image.load(filename), size)
    except Exception as e:
        print(f"Warning: Could not load '{filename}'. Using placeholder box instead. Details: {e}")
        fallback = Surface(size)
        fallback.fill(color_fallback)
        return fallback

# Load and scale assets safely (with color fallbacks if files are missing)
background = load_safely('Background.png', Size, (30, 30, 30))

ZombieSize = (150, 200)
CopSize = (200, 200)

Zombie = load_safely('Zombie.png', ZombieSize, (0, 200, 0))
Cop = load_safely('Cop.png', CopSize, (0, 0, 255))
obs = load_safely('obs.png', (100, 100), (255, 0, 0))
obs2 = load_safely('obs2.png', (70, 70), (255, 100, 0))
obss = load_safely('obs.png', (100, 100), (255, 0, 0))

coinImg = load_safely('money.png', (50, 50), (255, 215, 0)) 

healthImg = load_safely('health.png', IconSize, (255, 50, 50))
moneyImg = load_safely('money.png', IconSize, (255, 215, 0))
scoreImg = load_safely('score.png', IconSize, (0, 255, 100))

mouse.set_visible(False)

def reset_game():
    """Resets all game variables for a fresh start."""
    global ZombiePosx, ZombiePosy, ZombieSpeed, angle
    global CopPosx, CopPosy, CopSpeed
    global obsPosx, obsPosy, obsSpeed, obs2Posx, obs2Posy, obs2Speed, obssPosx, obssPosy, obssSpeed
    global health, money, score, game_state, coin_rect
    
    # Player
    ZombiePosx = SCREEN_WIDTH // 2 
    ZombiePosy = SCREEN_HEIGHT // 2 
    ZombieSpeed = 8
    angle = 0

    # Enemy
    CopPosx = 100
    CopPosy = 100
    CopSpeed = 4

    # Obstacles
    obsPosx, obsPosy, obsSpeed = 200, 200, 6
    obs2Posx, obs2Posy, obs2Speed = 400, 400, 6
    obssPosx, obssPosy, obssSpeed = 200, 600, 6

    # Gameplay Mechanics
    health = 100
    money = 0
    score = 0
    game_state = "PLAY" 
    
    # Spawn first coin
    coin_rect = coinImg.get_rect(topleft=(randint(100, SCREEN_WIDTH-100), randint(100, SCREEN_HEIGHT-200)))

# Run reset to set initial variables
reset_game()

game = True
clock = time.Clock() 

while game:
    clock.tick(60)

    # Event handling
    for e in event.get():
        if e.type == QUIT:
            save_high_score(score) 
            game = False
        if e.type == KEYDOWN:
            if game_state == "GAMEOVER":
                if e.key == K_r:
                    reset_game()
                elif e.key == K_ESCAPE:
                    save_high_score(score) 
                    game = False

    if game_state == "PLAY":
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
            
        # 2. Smooth Cop chasing logic (Vector-based approach)
        dx = ZombiePosx - CopPosx
        dy = ZombiePosy - CopPosy
        distance = math.hypot(dx, dy)
        
        rad_angle = math.atan2(-dy, dx)
        cop_angle = math.degrees(rad_angle)

        if distance > 0:
            CopPosx += (dx / distance) * CopSpeed
            CopPosy += (dy / distance) * CopSpeed

        # 3. Obstacle movement
        obsPosx += obsSpeed
        if obsPosx <= 0 or obsPosx >= SCREEN_WIDTH - 100: 
            obsSpeed *= -1
            
        obs2Posy += obs2Speed
        if obs2Posy <= 0 or obs2Posy >= SCREEN_HEIGHT - 70: 
            obs2Speed *= -1
        
        obssPosx += obssSpeed
        if obssPosx <= 0 or obssPosx >= SCREEN_WIDTH - 100:
            obssSpeed *= -1

        # 4. Setup rectangles for collision
        Zombie_rect = Zombie.get_rect(topleft=(ZombiePosx, ZombiePosy))
        Cop_rect = Cop.get_rect(topleft=(CopPosx, CopPosy))
        obs_rect = obs.get_rect(topleft=(obsPosx, obsPosy))
        obs2_rect = obs2.get_rect(topleft=(obs2Posx, obs2Posy)) 
        obss_rect = obss.get_rect(topleft=(obssPosx, obssPosy))

        # Check for damage collisions
        is_colliding = (Zombie_rect.colliderect(Cop_rect) or 
                        Zombie_rect.colliderect(obs_rect) or 
                        Zombie_rect.colliderect(obs2_rect) or 
                        Zombie_rect.colliderect(obss_rect))

        if is_colliding:
            health -= 1  
            if health <= 0:
                health = 0
                game_state = "GAMEOVER"
                save_high_score(score)  

        # Check for Coin collection
        if Zombie_rect.colliderect(coin_rect):
            score += 10
            money += randint(5, 15)
            
            if score > high_score:
                high_score = score
                
            coin_rect.x = randint(100, SCREEN_WIDTH - 100)
            coin_rect.y = randint(100, SCREEN_HEIGHT - 200)

    # 5. Drawing Section
    shake_x = randint(-5, 5) if (game_state == "PLAY" and is_colliding) else 0
    shake_y = randint(-5, 5) if (game_state == "PLAY" and is_colliding) else 0

    window.blit(background, (shake_x, shake_y))
    
    if game_state == "PLAY":
        window.blit(coinImg, coin_rect)

    # Rotate and Draw Zombie
    rotated_zombie = transform.rotate(Zombie, angle)
    zombie_rot_rect = rotated_zombie.get_rect(center=Zombie_rect.center if game_state == "PLAY" else (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    window.blit(rotated_zombie, zombie_rot_rect)
    
    if game_state == "PLAY":
        # Rotate and Draw Cop
        rotated_cop = transform.rotate(Cop, cop_angle)
        cop_rot_rect = rotated_cop.get_rect(center=Cop_rect.center)
        window.blit(rotated_cop, cop_rot_rect)

        # Draw Obstacles
        window.blit(obs, (obsPosx, obsPosy))
        window.blit(obs2, (obs2Posx, obs2Posy))
        window.blit(obss, (obssPosx, obssPosy))
    
    # --- UI Drawing System ---
    padding_step = 280
    ui_y_position = SCREEN_HEIGHT - IconSize[1] - 20
    
    # 1. Health Icon + Text
    window.blit(healthImg, (20, ui_y_position))
    health_text = font_small.render(f"{health}%", True, (255, 255, 255))
    window.blit(health_text, (20 + IconSize[0] + 10, ui_y_position + 30))
    
    # 2. Money Icon + Text
    window.blit(moneyImg, (20 + padding_step, ui_y_position))
    money_text = font_small.render(f"${money}", True, (255, 215, 0))
    window.blit(money_text, (20 + padding_step + IconSize[0] + 10, ui_y_position + 30))
    
    # 3. Current Score Icon + Text
    window.blit(scoreImg, (20 + padding_step * 2, ui_y_position))
    score_text = font_small.render(f"Score: {score}", True, (0, 255, 100))
    window.blit(score_text, (20 + padding_step * 2 + IconSize[0] + 10, ui_y_position + 30))

    # 4. BEST SCORE (Reusing scoreImg asset here to prevent double-loading crashes)
    window.blit(scoreImg, (20 + padding_step * 3, ui_y_position))
    best_score_text = font_small.render(f"Best: {high_score}", True, (0, 225, 255))
    window.blit(best_score_text, (20 + padding_step * 3 + IconSize[0] + 10, ui_y_position + 30))
    
    if game_state == "PLAY" and is_colliding:
        red = Surface(Size, SRCALPHA)
        red.fill((255, 0, 0, 80))
        window.blit(red, (0, 0))
        
    # --- Game Over Screen State ---
    if game_state == "GAMEOVER":
        overlay = Surface(Size, SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        window.blit(overlay, (0, 0))
        
        text_gameover = font_large.render("GAME OVER", True, (255, 0, 0))
        text_restart = font_small.render("Press 'R' to Restart or 'ESC' to Quit", True, (255, 255, 255))
        text_final_score = font_small.render(f"Final Score: {score} | Money Gathered: ${money}", True, (255, 215, 0))
        text_high_score = font_small.render(f"All-Time High Score: {high_score}", True, (0, 255, 255))
        
        window.blit(text_gameover, (SCREEN_WIDTH // 2 - text_gameover.get_width() // 2, SCREEN_HEIGHT // 2 - 140))
        window.blit(text_final_score, (SCREEN_WIDTH // 2 - text_final_score.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        window.blit(text_high_score, (SCREEN_WIDTH // 2 - text_high_score.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        window.blit(text_restart, (SCREEN_WIDTH // 2 - text_restart.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

    display.update()

quit()