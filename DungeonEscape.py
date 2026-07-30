
# -----------------
# library 
# -----------------
import pgzrun # function: imports pgzrun module
import random  # Not in use
import time
from pygame import Rect

# -----------------
# Constants (Each of these is actually just a variable in Python.)
# -----------------
WIDTH = 640
HEIGHT = 360

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (200,0,0)
GREEN = (0, 150, 0)
BLUE = (30, 144, 255)
GOBLIN_GREEN = (0,150,0)

PLAYER_SPEED = 3

# -----------------
# Game State Section - ensure reset() is updated with any changes ()
# -----------------
score = 0
game_time = 0
game_over = False
start_time = time.time()
health_remaining = 50
last_hit_time = 0
has_key = False
current_map = (0,0)

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
    old_x = player.x
    old_y = player.y

    if keyboard.a:
        player.x -= PLAYER_SPEED

    if keyboard.d:
        player.x += PLAYER_SPEED

    if keyboard.w:
        player.y -= PLAYER_SPEED

    if keyboard.s:
        player.y += PLAYER_SPEED

    check_wall_collisions(old_x, old_y)

def reset_game(): # Reset all variables to their initial values. Ensure that this is updated.
    global score
    global game_duration
    global game_time
    global game_over
    global start_time
    global health_remaining
    global last_hit_time
    global has_key

    score = 0
    game_duration = 600
    game_time = 0
    game_over = False
    start_time = time.time()
    health_remaining = 100
    last_hit_time = 0
    has_key = False

def keep_player_on_screen():
    player.x = max(0, min(player.x, WIDTH - player.width))
    player.y = max(32, min(player.y, HEIGHT - player.height)) # 32px for UI

def check_wall_collisions(old_x, old_y):
    
    for obstacle in get_current_room().obstacles:

        if player.colliderect(obstacle):
            player.x = old_x
            player.y = old_y

def get_current_room(): # stores current room
    if current_map == (0,0):
        return room_00

    if current_map == (1,0):
        return room_01

def check_collisions():
    global game_over
    global health_remaining 
    global last_hit_time
    global has_key
    
    if player.colliderect(key):
        has_key = True
        
    if player.colliderect(monster):
        if (time.time() - last_hit_time) > 1: # damage cooldown 1 second
        
            health_remaining -= 10 # How do I handle different sources of damage with different values
            last_hit_time = time.time()
    
    for door in get_current_room().doors:
        if player.colliderect(door.rect):
            print("Touching door")

        if door.locked and has_key:
            if keyboard.f:
                door.unlock()
                print("door unlocked")

        elif not door.locked:
            if keyboard.f:
                print("door opened")
            
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
        screen.draw.text(
            "Press 'r' to restart",
            center=(WIDTH // 2, (HEIGHT // 2) + 30),
            color="white",
            fontsize=30
        )
        return

    # World
    # Door
    for door in get_current_room().doors:
        screen.draw.filled_rect(
            door.rect,
            door.get_colour()
    )

        # Enemies
    screen.draw.filled_rect(monster, (GOBLIN_GREEN))
    if has_key == False:
        screen.draw.filled_rect(key, (YELLOW)) # If the player doesn't have the key draw it

    # Draw walls
    for obstacle in get_current_room().obstacles:
        screen.draw.filled_rect(obstacle, WHITE)

    # Player
    screen.draw.filled_rect(player, (BLUE))
    
    # UI
    # Draw the score
    screen.draw.text(
        f"Score: {score}",
        (10, 10),
        color="white",
        fontsize=30
    )

    # Shows coordinates of current map/room
    screen.draw.text(
    f"Map: {current_map}",
    (500, 40),
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
        (120, 10),
        color="green",
        fontsize=30
    )

    # key possession
    screen.draw.text(
        f"Key: {has_key}",
        (300, 10),
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
        if keyboard.r:
            reset_game()
        return

    move_player()
    check_collisions()
    hunt()
    keep_player_on_screen()

class Door:

    def __init__(self, position, destination_map, destination_position):
        self.rect = Rect(position, (32,32))
        self.locked = True
        self.destination_map = destination_map
        self.destination_position = destination_position
        self.open = False


    def unlock(self):
        self.locked = False


    def get_colour(self):
        if self.locked:
            return RED
        else:
            return GREEN

class Room: # Each room is a map tile i.e. (0, 0) "container"

    def __init__(self):
        self.obstacles = []
        self.doors = []
        # self.enemies = []
        # self.items = []    

# -----------------
# Doors
# -----------------

door_00 = Door(
    position=(320,32),
    destination_map=(1,0),
    destination_position=(320,300),
)

door_01 = Door(
    position=(352,320),
    destination_map=(0,0),
    destination_position=(320,32),
)


# -----------------
# Rooms
# -----------------

room_00 = Room()

room_00.obstacles.append(
    Rect((0,32),(64,328))
)

room_00.obstacles.append(
    Rect((576,32),(64,328))
)

room_00.doors.append(door_00)


room_01 = Room()

room_01.obstacles.append(
    Rect((0,32),(640,64))
)

room_01.obstacles.append(
    Rect((0,320),(640,352))
)

room_01.doors.append(door_01)
# -----------------
# Start the game
# -----------------

pgzrun.go()
