"""Adapted from Peter Collinridge project. Simple model of particles in 2D.
This one follows the 'sun.'"""

import math
import random
import pygame, sys, os
from pygame.locals import *

#   Set up Pygame variables
pygame.init()
BG_colour = (0,0,0)
particle_colour = (200,200,200)

# originally (480, 360)
(width, height) = (480, 360)
center = [width/2, height/2]
screen = pygame.display.set_mode((width, height))

# initial version in copied version had 170
number_of_particles = 170
particles = []

# vectors are defined in this case by andle and length
# e.g. vactor1 = [angle1, length1]
def combineVectors(vector1, vector2):
    """ Adds together two vectors given as an angle plus a magnitude (length)"""

    x1  = math.sin(vector1[0]) * vector1[1]
    y1  = math.cos(vector1[0]) * vector1[1]
    x2 = x1 + math.sin(vector2[0]) * vector2[1]
    y2 = y1 + math.cos(vector2[0]) * vector2[1]
    
    angle = 0.5*math.pi - math.atan2(y2, x2)
    length  = math.hypot(x2, y2)
    return [angle, length]

class Particle():
    def __init__(self, x, y, mass=1):
        self.x = x
        self.y = y
        self.mass = mass
        self.findRadius()

        self.speed = 0
        self.angle = 0

    def findRadius(self):
        self.radius = 0.4 * self.mass ** (1.0/3.0)
        self.size = int(self.radius)
        if self.size < 2:
            self.colour = (100+self.mass, 100+self.mass, 100+self.mass)
        else:
            self.colour = (255,255, 0)

    def move(self):
        """ Moves the particle based on its speed and direction """
 
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed


    def attract(self, other):
        """" Particles attract one another based on their distance and masses"""
        
        dx = (self.x - other.x) * 2
        dy = (self.y - other.y) * 2

        dist  = math.hypot(dx, dy)
        if dist == 0:
            dist = 0.000001
        force = 0.1 * self.mass * other.mass / dist**2
        theta = 0.5 * math.pi - math.atan2(dy, dx)    
        
        if dist < self.radius + other.radius:
            total_mass = self.mass + other.mass

            self.x = (self.x * self.mass + other.x * other.mass) / total_mass
            self.y = (self.y * self.mass + other.y * other.mass) / total_mass
            self.speed = self.speed * self.mass / total_mass
            other.speed = other.speed * other.mass / total_mass

            (self.angle,  self.speed)  = combineVectors((self.angle,  self.speed), (other.angle, other.speed))

            self.mass = total_mass
            self.findRadius()
            return other
        else:
            (self.angle,  self.speed)  = combineVectors((self.angle,  self.speed),  (theta+math.pi, force/self.mass))
            (other.angle, other.speed) = combineVectors((other.angle, other.speed), (theta, force/other.mass))



for p in range(number_of_particles):
    mass = random.randint(1, 4)
    #mass = 1
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    particles.append(Particle(x, y, mass))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(), sys.exit(0)

    screen.fill(BG_colour)

    for i in range(number_of_particles):
        j = i+1

        while j < number_of_particles:
            collide = particles[i].attract(particles[j])

            if collide != None:
                particles.remove(collide)
                number_of_particles -= 1
            else:
                j += 1

    for p in particles:
        p.move()

        # generally only one mass will be very large
        if p.mass >= 140:
            dx = (p.x - center[0])
            dy = (p.y - center[1])
            dist  = math.hypot(dx, dy)
            
            # adjusts towards center
            if int(dist) > center[0] or int(dist) > center[1]:
                for p in particles:
                    p.x = p.x - 2*dx
                    p.y = p.y - 2*dy
            # eliminate the particles that fly away
            elif int(dist) > 20*width or int(dist) > 20*height:
                particles.remove(p)
                
        # draws each particle
        if p.size < 2:
            pygame.draw.rect(screen, p.colour, (int(p.x), int(p.y), 2, 2))

        else:         
            pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)),
                               p.size + 1, 0)
        

    pygame.display.flip()

for p in particles:
    dx = math.sin(p.angle) * p.speed
    dy = math.cos(p.angle) * p.speed
    print("(%d, %d)\t(dx=%f, dy=%f)\tmass = %d" % (p.x, p.y, dx, dy, p.mass))
