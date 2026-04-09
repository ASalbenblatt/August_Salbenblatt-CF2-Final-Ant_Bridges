from constants import *

vector = tuple[float, float]

def add (vec1: vector, vec2: vector) -> vector:
    return (vec1[0] + vec2[0], vec1[1] + vec2[1])

def subtract (vec1: vector, vec2: vector) -> vector:
    return (vec1[0] - vec2[0], vec1[1] - vec2[1])

def dot (vec1: vector, vec2: vector) -> float:
    return (vec1[0] * vec2[0]) + (vec1[1] * vec2[1])

def scaleBy (vec1: vector, scalar: float) -> vector:
    return (vec1[0] * scalar, vec1[1] * scalar)

def magnitude (vec: vector) -> float:
    return sqrt(vec[0]**2 + vec[1]**2)

def projectOnto (vec1: vector, vec2: vector) -> vector:
    return scaleBy(vec2, (dot(vec1, vec2)/(magnitude(vec2)**2)))

def normalPoint (fromVec: vector, toVec: vector) -> vector:
    fullPoint: vector = subtract(toVec, fromVec)
    return scaleBy(fullPoint, 1/magnitude(fullPoint))

def distanceBetween (vec1: vector, vec2: vector) -> float:
    return magnitude(subtract(vec1, vec2))