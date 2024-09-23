import pygame
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Define some physics constants
FRICTION_COEFFICIENT = 0.1
RESTITUTION_COEFFICIENT = 0.9

# Define some utility functions
def distance(obj1, obj2):
    return math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)

def force(obj1, obj2):
    dist = distance(obj1, obj2)
    force_magnitude = (obj1.mass * obj2.mass) / dist**2
    force_x = force_magnitude * (obj2.x - obj1.x) / dist
    force_y = force_magnitude * (obj2.y - obj1.y) / dist
    return (force_x, force_y)

class Board:
    def __init__(self, width, height, margin):
        self.width = width
        self.height = height
        self.margin = margin
    
    def draw(self):
        pygame.draw.rect(screen, BLACK, (0, 0, self.width, self.margin))
        pygame.draw.rect(screen, BLACK, (0, self.height - self.margin, self.width, self.margin))
        pygame.draw.rect(screen, BLACK, (0, 0, self.margin, self.height))
        pygame.draw.rect(screen, BLACK, (self.width - self.margin, 0, self.margin, self.height))

class Coin:
    def __init__(self, x, y, width, height, mass, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = mass
        self.color = color
        self.vx = 0
        self.vy = 0
    
    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.width / 2 < board.margin:
            self.x = board.margin + self.width / 2
            self.vx = -self.vx * RESTITUTION_COEFFICIENT
        if self.x + self.width / 2 > board.width - board.margin:
            self.x = board.width - board.margin - self.width / 2
            self.vx = -self.vx * RESTITUTION_COEFFICIENT
        if self.y - self.height / 2 < board.margin:
            self.y = board.margin + self.height / 2
            self.vy = -self.vy * RESTITUTION_COEFFICIENT
        if self.y + self.height / 2 > board.height - board.margin:
            self.y = board.height - board.margin - self.height / 2
            self.vy = -self.vy * RESTITUTION_COEFFICIENT
    
    def update_velocity(self, dv):
        self.vx += dv[0]
        self.vy += dv[1]
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > 0:
            friction_force = FRICTION_COEFFICIENT * self.mass * 9.81
            if friction_force > speed:
                self.vx = 0
                self.vy = 0
            else:
                friction_x = friction_force * self.vx / speed
                friction_y = friction_force * self.vy / speed
                self.vx -= friction_x
                self.vy -= friction_y


class Striker:
    def __init__(self, x, y, width, height, mass, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = mass
        self.color = color
        self.vx = 0
        self.vy = 0
    
    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.width / 2 < board.margin:
            self.x = board.margin + self.width / 2
            self.vx = -self.vx * RESTITUTION_COEFFICIENT
        if self.x + self.width / 2 > board.width - board.margin:
            self.x = board.width - board.margin - self.width / 2
            self.vx = -self.vx * RESTITUTION_COEFFICIENT
        if self.y - self.height / 2 < board.margin:
            self.y = board.margin + self.height / 2
            self.vy = -self.vy * RESTITUTION_COEFFICIENT
        if self.y + self.height / 2 > board.height - board.margin:
            self.y = board.height - board.margin - self.height / 2
            self.vy = -self.vy * RESTITUTION_COEFFICIENT
    
    def update_velocity(self, dv):
        self.vx += dv[0]
        self.vy += dv[1]
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > 0:
            friction_force = FRICTION_COEFFICIENT * self.mass * 9.81
            if friction_force > speed:
                self.vx = 0
                self.vy = 0
            else:
                friction_x = friction_force * self.vx / speed
                friction_y = friction_force * self.vy / speed
                self.vx -= friction_x
                self.vy -= friction_y

# Initialize pygame
pygame.init()

# Set up the display
size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Carrom")

# Set up the game
board = Board(600, 600, 20)
striker = Striker(400, 550, 30, 30, 1, BLUE)
coin1 = Coin(300, 300, 20, 20, 1, WHITE)
coin2 = Coin(250, 300, 20, 20, 1, WHITE)

# Set up the clock
clock = pygame.time.Clock()

# Game loop
done = False
while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                dv = force(striker, Coin(mouse_pos[0], mouse_pos[1], 0, 0, 1, BLACK))
                striker.update_velocity(dv)
    
    # Update game state
    striker.update_position()
    coin1.update_position()
    coin2.update_position()
    
    # Check for collisions
    if collision(striker, coin1):
        dv = collide(striker, coin1)
        striker.update_velocity(dv[0])
        coin1.update_velocity(dv[1])
    if collision(striker, coin2):
        dv = collide(striker, coin2)
        striker.update_velocity(dv[0])
        coin2.update_velocity(dv[1])
    if collision(coin1, coin2):
        dv = collide(coin1, coin2)
        coin1.update_velocity(dv[0])
        coin2.update_velocity(dv[1])
    
    # Draw board and game objects
    screen.fill(WHITE)
    board.draw()
    pygame.draw.circle(screen, striker.color, (int(striker.x), int(striker.y)), striker.width // 2)
    pygame.draw.circle(screen, coin1.color, (int(coin1.x), int(coin1.y)), coin1.width // 2)
    pygame.draw.circle(screen, coin2.color, (int(coin2.x), int(coin2.y)), coin2.width // 2)
    
    # Update screen
    pygame.display.flip()
    clock.tick(60)

# Quit pygame
pygame.quit()

