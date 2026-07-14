import pgzrun
import random  # Not in use
import time
from pygame import Rect
# -----------------
# Constants
# -----------------

WIDTH = 640
HEIGHT = 360

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
RED = (200,0,0)

PLAYER_SPEED = 3

# -----------------
# Game State Section
# -----------------
score = 0
game_duration = 600
game_time = 0
game_over = False
start_time = time.time()
health_remaining = 100
last_hit_time = 0

# -----------------
# Cast draw size and colour
# -----------------
player = Rect((320, 180), (32, 32))
key = Rect((100, 100), (32, 32))
monster = Rect((180, 320), (32, 32))


# -----------------
# Helper Functions
# -----------------

def move_player():
    if keyboard.a:
        player.x -= PLAYER_SPEED

    if keyboard.d:
        player.x += PLAYER_SPEED

    if keyboard.w:
        player.y -= PLAYER_SPEED

    if keyboard.s:
        player.y += PLAYER_SPEED


def keep_player_on_screen():
    player.x = max(0, min(player.x, WIDTH - player.width))
    player.y = max(0, min(player.y, HEIGHT - player.height))


def check_collisions():
    global game_over
    global health_remaining
    global last_hit_time
    global damage_cooldown
    global player_vulerable

    if player.colliderect(monster):
        if (time.time() - last_hit_time) > 1: # damage cooldown 1 second
        
            health_remaining -= 10 # How do I handle different sources of damage with different values
            last_hit_time = time.time()

        if health_remaining <=0:
            game_over = True

def end_game():
    global game_over
    global health_remaining

    game_over = True
    if health_remaining <=0:
        game_over

def hunt(): # Moves the monster toward the player
    if monster.x < player.x: # moves monster right
        monster.x += 1
    
    if monster.x > player.x: # moves monster left
        monster.x -= 1

    if monster.y < player.y: # moves monster up
        monster.y += 1
    
    if monster.y > player.y:# moves monster down
        monster.y -= 1

  
# -----------------
# Draw
# -----------------

def draw():
    screen.clear()
    screen.fill(BLACK)

    # If the game has ended, only draw the Game Over screen
    if game_over:
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, HEIGHT // 2),
            color="white",
            fontsize=60
        )
        return

    # Draw the game objects
    screen.draw.filled_rect(player, (BLUE))
    screen.draw.filled_rect(key, (YELLOW))
    screen.draw.filled_rect(monster, (RED))

    # Draw the score
    screen.draw.text(
        f"Score: {score}",
        (10, 10),
        color="white",
        fontsize=30
    )

    # Draw the countup timer
    screen.draw.text(
        f"Time: {game_time}",
        (450, 10),
        color="white",
        fontsize=30
    )

    # Draw the health
    screen.draw.text(
        f"Health: {health_remaining}",
        (200, 10),
        color="white",
        fontsize=30
    )
    # If the game has ended, only draw the Game Over screen
   
        

# -----------------
# Update
# -----------------

def update():
    global game_time
    
    game_time = int(time.time() - start_time)

    if game_over:
        return

    move_player()
    keep_player_on_screen()
    check_collisions()
    hunt()