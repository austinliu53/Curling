import pygame

class GhostStone:

    def __init__(this, radius, x, y, color):
        this.radius = radius
        this.x = x
        this.y = y
        this.color = color
    
    def draw(this, drawSurface):

        print(this.color)
        transSurface = pygame.Surface((2 * this.radius, 2 * this.radius), pygame.SRCALPHA)
        pygame.draw.circle(transSurface, this.color, (this.x, this.y), this.radius)

        
        drawSurface.blit(transSurface, (this.x - this.radius, this.y - this.radius))