import pygame
import math
import Constants
import Stone
import Plane

BLACK = (0, 0, 0)
class Vector:
    def __init__(this, x : float, y :float, xVector : float, yVector : float, stone : Stone, plane : Plane):
        this.x = x
        this.y = y
        this.xVector = xVector
        this.yVector = yVector
        this.stone = stone
        plane.addVector(this)

    def updateToStone(this):
        this.x = this.stone.x
        this.y = this.stone.y
        this.xVector = this.stone.xVel
        this.yVector = this.stone.yVel

    def draw(this, drawSurface):
        # Calculate the angle

        angle = math.atan2(this.xVector, this.yVector)

        if (this.xVector == 0 and this.yVector == 0):
            return
        # Find the two other points of the arrow. 
        
        arrowEnd = (
            this.x + this.xVector * Constants.ARROW_FACTOR, 
            this.y + this.yVector * Constants.ARROW_FACTOR
        )   

        point1 = (
            -math.sin(angle + math.pi/4) * Constants.ARROW_POINT_LENGTH + arrowEnd[0], 
            -math.cos(angle + math.pi/4) * Constants.ARROW_POINT_LENGTH + arrowEnd[1]
        )

        point2 = (
            -math.sin(angle - math.pi/4) * Constants.ARROW_POINT_LENGTH + arrowEnd[0], 
            -math.cos(angle - math.pi/4) * Constants.ARROW_POINT_LENGTH + arrowEnd[1]
        )

        # The shaft of the arrow
        pygame.draw.line(drawSurface, BLACK, (this.x, this.y), arrowEnd)

        # The "point" of the arrow
        pygame.draw.line(drawSurface, BLACK, arrowEnd, point1)
        pygame.draw.line(drawSurface, BLACK, arrowEnd, point2)

