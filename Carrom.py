import pygame
import math
from finalstart_menu import start_window

# Initialize Pygame
pygame.init()
# Initial Width and Height
(width, height) = (560, 560)
coeff_friction= 0.01
drag = 1- coeff_friction
coeff_restitution= 0.85
elasticity = coeff_restitution 
gravity = (math.pi, 0.002)
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 215, 1)
WOODEN = (238, 197, 145)
# BgImg
Board = pygame.image.load("Carromboard.jpg")

# Caption and Icon
pygame.display.set_caption('Carrom Strike')
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

# BgMusic
# pygame.mixer.music.load('song.wav')
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(0.25)

# Text Font
pygame.font.init()
font = pygame.font.SysFont('comicsans', 30)


def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return angle,length



# Collision Function
def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed * (p1.mass - p2.mass) / total_mass, angle,
                                          2 * p2.speed * p2.mass / total_mass)
        (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed * (p2.mass - p1.mass) / total_mass, angle + math.pi,
                                          2 * p1.speed * p1.mass / total_mass)
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5 * (p1.size + p2.size - dist + 1)
        p1.x += math.sin(angle) * overlap   #move upword
        p1.y -= math.cos(angle) * overlap   # x- axis left
        p2.x -= math.sin(angle) * overlap   #downwrod
        p2.y += math.cos(angle) * overlap   #x-axis right


class Particle:
    def __init__(self, colour, x, y, size, mass):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.mass = mass

        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

    def strikers(self, ycor):
        (mX, mY) = pygame.mouse.get_pos()
        if mX > 470:
            self.x = 470
        elif mX < 90:
            self.x = 90
        else:
            self.x = mX
        self.y = ycor

    def bounce(self):   # for right boundry
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:  #for left boundry
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:    #for upword boundry
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:      #for downward
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity


# Screen Size
screen = pygame.display.set_mode((560, 560))

my_particles = []
# Striker
striker = Particle(YELLOW, 160, 470, 27, 47)
# All Coins
particle = Particle(BLACK, 290, 250, 15, 6)
my_particles.append(particle)
particle = Particle(BLACK, 305, 290, 15, 6)
my_particles.append(particle)
particle = Particle(BLACK, 280, 300, 15, 6)
my_particles.append(particle)
particle = Particle(BLACK, 250, 280, 15, 6)
my_particles.append(particle)
particle = Particle(BLACK, 240, 245, 15, 6)
my_particles.append(particle)
particle = Particle(BLACK, 340, 285, 15, 6)
my_particles.append(particle)
particle = Particle(BLACK, 280, 335, 15, 6)
my_particles.append(particle)

particle = Particle(RED, 280, 280, 15, 6)
my_particles.append(particle)

particle = Particle(WHITE, 260, 270, 15, 6)
my_particles.append(particle)
particle = Particle(WHITE, 270, 305, 15, 6)
my_particles.append(particle)
particle = Particle(WHITE, 275, 250, 15, 6)
my_particles.append(particle)
particle = Particle(WHITE, 330, 255, 15, 6)
my_particles.append(particle)
particle = Particle(WHITE, 300, 300, 15, 5)
my_particles.append(particle)
particle = Particle(WHITE, 300, 340, 15, 6)
my_particles.append(particle)
particle = Particle(WHITE, 320, 250, 15, 6)
my_particles.append(particle)
particle = Particle(WHITE, 360, 380, 15, 6)
my_particles.append(particle)

selected_particle = None
running = True
state = 0
count1 = 0
count2 = 0
flip = 0
start_window(width)

# Game Loop
while running:

    # Screen fill
    # screen.fill((0, 0, 0))
    screen.blit(Board, (0, 0))


    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            running = False

        if state == 0:
            if flip % 2 == 0:
                ycor = 470
            elif flip % 2 != 0:
                ycor = 90

            striker.strikers(ycor)
            # Mouse Functions
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                if mouseX > 470:         #downward baseline
                    striker.x = 470
                elif mouseX < 90:       #
                    striker.x = 90
                else:
                    striker.x = mouseX
                state = 1
                continue

        if state == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX2, mouseY2) = pygame.mouse.get_pos()
                dx = mouseX2 - striker.x
                dy = mouseY2 - striker.y
                striker.angle = 0.5 * math.pi + math.atan2(dy, dx)
                striker.speed = math.hypot(dx, dy) * 0.1
                state = 2

    striker.move()
    striker.bounce()
    if 0 < striker.speed < 0.15:
        flip += 1
        striker.speed = 0
        state = 0

    for i, particle in enumerate(my_particles):

        particle.move()
        particle.bounce()
        collide(striker, particle)
        # Potholes Disappearance Function
        if particle.x < 60 and particle.speed > 0:   #top left
            if particle.y < 60:
                my_particles.remove(particle)
                if flip % 2 == 0:
                    count1 += 5
                elif flip % 2 != 0:
                    count2 += 5
                flip -= 1

        if particle.x < 60 and particle.speed > 0:  #bottom left
            if particle.y > 500:
                my_particles.remove(particle)
                if flip % 2 == 0:
                    count1 += 5
                elif flip % 2 != 0:
                    count2 += 5
                flip -= 1

        if particle.x > 500 and particle.speed > 0:  #top right
            if particle.y < 60:
                my_particles.remove(particle)
                if flip % 2 == 0:
                    count1 += 5
                elif flip % 2 != 0:
                    count2 += 5
                flip -= 1

        if particle.x > 500 and particle.speed > 0:  #bottom right
            if particle.y > 500:
                my_particles.remove(particle)
                if flip % 2 == 0:
                    count1 += 5
                elif flip % 2 != 0:
                    count2 += 5
                flip -= 1

        # Score
        #text1 = font.render('Score A:' + str(count1), 1, (255, 0, 0))
        #text2 = font.render('Score B:' + str(count2), 1, (255, 0, 0))
#        if count1 != 0 or count2 != 0:
#            print(count1, ":", count2)
#        screen.blit(text1, (250, 500))
#        screen.blit(text2, (250, 40))

        for particle2 in my_particles[i + 1:]:
            collide(particle, particle2)
            striker.display()
            particle.display()
            if particle.speed < 0.25:
                particle.speed = 0
                
    coin_positions = [] 

    # Striker position
    # striker.strikers(470)
    #striker.display()

    # Coin position
    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i + 1:]:
            collide(particle, particle2)
        particle.display()

    # store position of coin after 0.4 sec
    if pygame.time.get_ticks() % 400 == 0:
        coin_positions.append((particle.x, particle.y))
    print(coin_positions)

    pygame.display.flip()
# Exit Message
if count1 > count2:
    Con = font.render("Congratulations A", 1, (0, 0, 0))
else:
    Con = font.render("Congratulations B", 1, (0, 0, 0))
screen.blit(Con, (190, 280))
pygame.display.update()
