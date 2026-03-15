import math
import Constants

import Vector

import pygame

BLACK = (0, 0, 0)

class Stone:

    def __init__(this, radius, x, y, xVel, yVel, color, plane):
        this.radius = radius
        this.x = x
        this.y = y
        this.xVel = xVel
        this.yVel = yVel
        this.friction = Constants.FRICTION
        this.color = color
        this.plane = plane
        this.lastCollision = None

        this.vector = Vector.Vector(this.x, this.y, xVel, yVel, this, plane)
    
    def setVelocity(this, xVel, yVel):
        this.xVel = xVel
        this.yVel = yVel

    def findNewVelocities(this, stone):
        
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

        thisNewVelocity = (1 - energyTransferred) * thisRelVelocityToStone
        
        tempStoneX = stone.xVel
        tempStoneY = stone.yVel

        this.setVelocity(
            stoneNewVelocity * (math.cos(collisionAngle)) + this.xVel, 
            stoneNewVelocity * (math.sin(collisionAngle)) + this.yVel
        )
        
        stone.setVelocity(
            -stoneNewVelocity * (math.cos(collisionAngle)) + tempStoneX, 
            -stoneNewVelocity * (math.sin(collisionAngle)) + tempStoneY
        )

        #print("Stone velocity", stone.xVel, stone.yVel)

        return

    def findCollision(this, stones):

        
        for stone in stones:

            if (stone == this):
                #print(":NNNOWEF")
                continue
        
            #print("Finding collision")
            dX = this.x - stone.x
            dY = this.y - stone.y

            dEuclidean = math.sqrt(dX ** 2 + dY ** 2)
            #print(dEuclidean)

            if (dEuclidean > 100):
                continue

            else:
                dMin = this.radius + stone.radius # minimum distance for the stones to not be touching

                #print(dEuclidean, dMin)
                if (dEuclidean < dMin) and (this.lastCollision != stone): # If this is a valid collision
                    

                    if ((stone.lastCollision == this)):
                        this.lastCollision = stone
                        continue
                    
                    this.plane.addGhostStone(this)
                    this.plane.addGhostStone(stone)


                    this.findNewVelocities(stone)

                    # Mark last collision to be this
                    this.lastCollision = stone
                    stone.lastCollision = this

    def draw(this, drawSurface):
        pygame.draw.circle(drawSurface, this.color, (this.x, this.y), this.radius)
        #pygame.draw.aaline(drawSurface, BLACK, (this.x, this.y), (this.x + this.xVel * 4, this.y + this.yVel * 4))
 