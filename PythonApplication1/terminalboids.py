import pygame
import pygame.freetype
import numpy as np
import math
from dataclasses import dataclass

WIDTH = 800
HEIGHT = 600
BOID_SIZE = 5
BOID_COLOR = (255, 255, 255)
BACK_COLOR = (0, 0, 0)

@dataclass
class Boid:
    position: np.ndarray
    velocity: np.ndarray

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def limit(v, max_length):
    if np.linalg.norm(v) > max_length:
        return normalize(v) * max_length
    return v

def boid_update(boid, boids, attraction_point, repulsion_point):
    separation = np.zeros(2)
    alignment = np.zeros(2)
    cohesion = np.zeros(2)

    separation_count = 0
    alignment_count = 0
    cohesion_count = 0

    for other in boids:
        if other is boid: continue

        diff = boid.position - other.position
        dist = np.linalg.norm(diff)

        # Separation
        if dist < 50:
            separation += diff
            separation_count += 1

        # Alignment
        if dist < 100:
            alignment += other.velocity
            alignment_count += 1

        # Cohesion
        if dist < 100:
            cohesion += other.position
            cohesion_count += 1

    if separation_count > 0:
        separation /= separation_count
        separation = normalize(separation)
        separation *= 2

    if alignment_count > 0:
        alignment /= alignment_count
        alignment = normalize(alignment)

    if cohesion_count > 0:
        cohesion /= cohesion_count
        cohesion = boid.position - cohesion
        cohesion = normalize(cohesion)
    
    # Attraction to left click
    if attraction_point is not None:
        diff = attraction_point - boid.position
        dist = np.linalg.norm(diff)
        if dist > 0:
            attraction = diff / dist * (100 - dist) / 100
            attraction *= 5  # increase the strength of attraction
        else:
            attraction = np.zeros(2)
    else:
        attraction = np.zeros(2)

    # Repulsion from right click
    if repulsion_point is not None:
        diff = boid.position - repulsion_point
        dist = np.linalg.norm(diff)
        if dist < 100:
            repulsion = diff / dist * (100 - dist) / 100
            repulsion *= 5  # increase the strength of repulsion
        else:
            repulsion = np.zeros(2)
    else:
        repulsion = np.zeros(2)

    boid.velocity += separation + alignment + cohesion + attraction - repulsion
    boid.velocity = limit(boid.velocity, 2)


    boid.position += boid.velocity

    if boid.position[0] < 0: boid.position[0] += WIDTH
    if boid.position[0] > WIDTH: boid.position[0] -= WIDTH
    if boid.position[1] < 0: boid.position[1] += HEIGHT
    if boid.position[1] > HEIGHT: boid.position[1] -= HEIGHT


def draw_boid(screen, boid):
    pygame.draw.circle(screen, BOID_COLOR, boid.position.astype(int), BOID_SIZE)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    boids = [Boid(np.random.rand(2) * [WIDTH, HEIGHT], (np.random.rand(2) - 0.5) / 10.0) for _ in range(100)]
    
    attraction_point = None
    repulsion_point = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    attraction_point = np.array(event.pos)
                elif event.button == 3:  # Right click
                    repulsion_point = np.array(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    attraction_point = None
                elif event.button == 3:  # Right click
                    repulsion_point = None

        for boid in boids:
            boid_update(boid, boids, attraction_point, repulsion_point)
            draw_boid(screen, boid)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
