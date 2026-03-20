import pygame

BLACK = (0, 0, 0)
class GhostStone:

    def __init__(this, stone, vector):
        this.stone = stone
        this.x = this.stone.x
        this.y = this.stone.y
        this.radius = stone.radius
        this.vector = vector

        this.stone.plane.ghostStones.append(this)
    
    def draw(this, drawSurface):
        pygame.draw.circle(drawSurface, BLACK, (this.x, this.y), this.radius, width=2)