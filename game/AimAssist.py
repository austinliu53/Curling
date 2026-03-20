import pygame

BLACK = (0, 0, 0)

class AimAssist:

    def __init__(this, x: float, y: float, radius: float):
        this.x = x
        this.y = y
        this.radius = radius
    
    def draw(this, drawSurface):
        pygame.draw.circle(drawSurface, BLACK, (this.x, this.y), this.radius, width=2)