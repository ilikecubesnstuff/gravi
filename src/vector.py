# Imports
from math import sqrt

class Vector:

    # Constructor
    def __init__(self, vec):
        self.x = vec[0]
        self.y = vec[1]

    # Mathematical Operations
    def __add__(self, other):
        return Vector([self.x + other.x, self.y + other.y])

    def __sub__(self, other):
        return Vector([self.x - other.x, self.y - other.y])

    def __mul__(self, other):
        return Vector([self.x * other, self.y * other])

    def __truediv__(self, other):
        return Vector([self.x / other, self.y / other])

    def __round__(self):
        return Vector([round(self.x), round(self.y)])

    def __abs__(self):
        return sqrt(self.x**2 + self.y**2)

    # Conversion
    def __str__(self):
        return str(self.x)+","+str(self.y)

    def list(self):
        return [self.x, self.y]
