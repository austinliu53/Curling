import pygame

class GhostStone:

    def __init__(this, radius, x, y, color):
        this.radius = radius
        this.x = x
        this.y = y
        this.color = color
    
    def draw(this, drawSurface):
        pygame.draw.circle(drawSurface, this.color, (this.x, this.y), this.radius)