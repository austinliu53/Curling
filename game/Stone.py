
import Constants
import Vector
import Plane
import random

import pygame
import math

BLACK = (0, 0, 0)
GREY = (127, 127, 127)

class Stone:

    def __init__(this, radius : float, x : float, y : float, xVel : float, yVel : float, color : tuple, plane : Plane, isRealStone : bool):
        this.radius = radius
        this.x = x
        this.y = y
        this.xVel = xVel
        this.yVel = yVel
        this.color = color
        this.plane = plane
        this.lastCollision = None
        this.distanceToMiddle = 0
        this.isRealStone = isRealStone

        if (this.isRealStone):
            this.vector = Vector.Vector(this.x, this.y, xVel, yVel, this)
        else:
            this.vector = None
    
    def setVelocity(this, xVel, yVel):
        this.xVel = xVel
        this.yVel = yVel

    def isOnPlane(this):
        return (
            (this.x < Constants.PLANE_X) or 
            (this.x > Constants.PLANE_X + Constants.PLANE_WIDTH) or 
            (this.y < Constants.PLANE_Y) or
            (this.y > Constants.PLANE_Y + Constants.PLANE_LENGTH)
        )

    def stoneEffectiveness(this):

        # Find the distance of the stone. The y-level
        if (this.y < Constants.CIRCLE_CENTER[1]) and (this.distanceToMiddle > Constants.BLUE_CIRCLE_RADIUS + this.radius):
            return 0
        
        backLineY = Constants.CIRCLE_CENTER[1] - Constants.BLUE_CIRCLE_RADIUS
        yToMiddle = abs(this.y - backLineY) 

        # Find the distance to the middle
        xToMiddle = abs(this.x - Constants.CIRCLE_CENTER[0])

        # Find the distance to the middle 
        # It already has a variable :)
        distancePoints = max(0, Constants.BLUE_CIRCLE_RADIUS - this.distanceToMiddle)

        # Find the possibility of it getting hit onto the house

        if (
            (this.x >= Constants.CIRCLE_CENTER[0] - Constants.BLUE_CIRCLE_RADIUS) and
            (this.x <= Constants.CIRCLE_CENTER[0] + Constants.BLUE_CIRCLE_RADIUS) and
            (this.y >= Constants.CIRCLE_CENTER[1] + Constants.BLUE_CIRCLE_RADIUS) and 
            (this.y <= 400)
            ):
            rebound = 100
        else:
            rebound = 0
        
        effectiveness = (
            max(0, Constants.PLANE_WIDTH / 2 - xToMiddle) * 0.2 + 
            max(0, Constants.PLANE_LENGTH - yToMiddle) * 0.03 + 
            rebound +
            distancePoints
            
            )
            
        return effectiveness
                                                                                                                                                                                                    

        # Find the 


    def findNewVelocities(this, stone): # -> Returns List: This vector, stone vector        
        #print(this.color)

        # The strategy here is that we imagine the other stone is staying still
        dX = this.x - stone.x
        dY = this.y - stone.y

        relVX = this.xVel - stone.xVel # This is the velocity of this stone relative to the other stone.
        relVY = this.yVel - stone.yVel

        relVelAngle = math.atan2(relVY, relVX)

        # print("dX:", dX)
        # print("dY:", dY)

        collisionAngle = math.atan2(dY, dX) # North from East

        # print("collisionAngle", collisionAngle)

        energyTransferred = abs(math.cos(collisionAngle - relVelAngle)) # percentage of energy transferred
        # print("energyTransferred", energyTransferred)

        # print("Stone 37", relVelMagnitude)

        thisRelVelocityToStone = math.sqrt(relVX ** 2 + relVY ** 2)

        # print("thisRelVelocityToStone", thisRelVelocityToStone)

        stoneNewVelocity = energyTransferred * thisRelVelocityToStone
        
        tempStoneX = stone.xVel
        tempStoneY = stone.yVel

        #print("Stone velocity", stone.xVel, stone.yVel)

        return [
            [
                stoneNewVelocity * (math.cos(collisionAngle)) + this.xVel, 
                stoneNewVelocity * (math.sin(collisionAngle)) + this.yVel
            ], 

            [
                -stoneNewVelocity * (math.cos(collisionAngle)) + tempStoneX, 
                -stoneNewVelocity * (math.sin(collisionAngle)) + tempStoneY
            ]
        ]
    
    def willThisShadow(this, x, y, radius) -> bool: # If this stone is in the effective shadow of stone.
        dX = this.x - x
        dY = this.y - y

        #print(dY, dX)

        distance = math.sqrt(dX ** 2 + dY ** 2)

        minRadius = this.radius + radius

        
        if (distance <= minRadius):
            return True
        
        if (abs(dX) <= minRadius and this.y > y) and this.stoneEffectiveness() > 25:

            if random.randint(0, int(abs(dY))) <= 50:
                if random.randint(0, len(this.plane.stones)) <= 2:
                    return True
        
        return False
    
    def isColliding(this, stone) -> bool: 
        if (stone == this):
            return False
    
        #print("Finding collision")
        dX = this.x - stone.x
        dY = this.y - stone.y

        dEuclidean = math.sqrt(dX ** 2 + dY ** 2)
        #print(dEuclidean)

        dMin = this.radius + stone.radius # minimum distance for the stones to not be touching

        if (dEuclidean > dMin):
            return False
        
        if (not type(stone) == Stone): # If this is "Aim assist"
            return True
        
        #print(dEuclidean, dMin)

        if (this.lastCollision != stone): # If this is a valid collision
            
            if (stone.lastCollision == this): 
                this.lastCollision = stone
                
                return False
            
        else:
            return False
        
        return True

    def findCollision(this, stones):

        for stone in stones:

            if (this.isColliding(stone)):

                newVelocities = this.findNewVelocities(stone)

                this.setVelocity(
                    newVelocities[0][0],
                    newVelocities[0][1]
                )
                
                stone.setVelocity(
                    newVelocities[1][0],
                    newVelocities[1][1]
                )

                # Mark last collision to be this
                this.lastCollision = stone
                stone.lastCollision = this

    def draw(this, drawSurface):

        if (this.isRealStone):
            pygame.draw.circle(drawSurface, GREY, (this.x, this.y), this.radius)
            pygame.draw.circle(drawSurface, this.color, (this.x, this.y), this.radius - 2)


        else:
            pygame.draw.circle(drawSurface, this.color, (this.x, this.y), this.radius, 2)
            font = pygame.font.SysFont("Helvetica", 10)
            fontSurface = font.render(str(math.floor(this.stoneEffectiveness())), True, BLACK)
            drawSurface.blit(fontSurface, (this.x - this.radius/2, this.y - this.radius/2))
        #pygame.draw.aaline(drawSurface, BLACK, (this.x, this.y), (this.x + this.xVel * 4, this.y + this.yVel * 4))
    
    def ghostCopy(this):
        stone = Stone(this.radius, this.x, this.y, this.xVel, this.yVel, this.color, this.plane, False)
        return stone

    def equals(this, stone):
        #i heart cp
        return stone.radius == this.radius and stone.x == this.x and stone.y == this.y and stone.xVel == this.xVel and stone.yVel == this.yVel and stone.color == this.color and stone.plane == this.plane# and stone.lastCollision == this.lastCollision and stone.distanceToMiddle == this.distanceToMiddle and stone.isRealStone == this.isRealStone
    
    



