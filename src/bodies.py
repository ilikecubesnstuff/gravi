# Imports
from math import ceil
from vector import Vector

class StaticBody:

    # Constructor
    def __init__(self, mass, pos):
        self.mass = mass
        self.radius = ceil(4*mass**(1/3))
        self.pos = Vector(pos)

    # Methods
    def __str__(self):
        return str(self.mass)+","+str(self.pos)

    def increase_mass(self, mass):
        self.mass += mass
        self.radius = ceil(4*mass**(1/3))

    def dist(self, other):
        return abs(other.pos - self.pos)


class DynamicBody(StaticBody):

    # Constructor
    def __init__(self, mass, pos, vel):
        StaticBody.__init__(self, mass, pos)
        self.vel = Vector(vel)
        self.acc = Vector([0, 0])

    # Methods
    def __str__(self):
        return str(self.mass)+","+str(self.pos)+","+str(self.vel)
