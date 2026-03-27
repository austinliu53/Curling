import pygame
import Stone
import math
import Constants
import Vector
import AimAssist

class Player:
    def __init__(this, stone: Stone):

        this.stone = stone
        this.iVel = Constants.INITIAL_DELIVERY
        this.iAngle = math.pi # 180 degrees : down
        this.score = 0

        this.vector = Vector.Vector(
            this.stone.x,
            this.stone.y,
            math.sin(this.iAngle) * this.iVel,
            -math.cos(this.iAngle) * this.iVel,
            this.stone
        )

        this.aimAssist = AimAssist.AimAssist(this.stone.x, this.stone.y, this.stone.radius)

    def input(this, aPressed, dPressed, wPressed, sPressed):

        this.stone.x += Constants.X_MOVE_ACCEL * (dPressed - aPressed)
        this.iVel -= (wPressed - sPressed) * Constants.DELIVERY_ACCEL

        this.stone.x = max(Constants.PLANE_X, min(this.stone.x, Constants.PLANE_X + Constants.PLANE_WIDTH))
        this.iVel = max(-Constants.PLAYER_MAX_VEL, min(this.iVel, 0))
        #print(this.iVel)

    def updateVecToPlayer(this):

        this.vector.x = this.stone.x
        this.vector.y = this.stone.y
        this.vector.xVector = math.sin(this.iAngle) * this.iVel
        this.vector.yVector = -math.cos(this.iAngle) * this.iVel

    def updatePathTracer(this):

        # Start at the player.
        # Then, move the player's stone up until it has touched another stone.
        # What happens next? 
        # Find collision point.
        # If none has been found, and the y level has passed below 0, (beyond the screen)
        # Then just don't give anything.

        collisionVel = this.iVel
        foundCollision = False
        this.aimAssist.x = this.stone.x
        this.aimAssist.y = this.stone.y
        
        stones = []
        
        for stone in this.stone.plane.stones:
            if this.stone != stone:
                stones.append(stone)

        while not foundCollision:

            # Find a collision
            for stone in stones:
                if stone.isColliding(this.aimAssist):
                    foundCollision = True
                    this.collisionStone = stone
                    
                    break

            if (this.aimAssist.y < 0):
                this.collisionStone = None
                break
            
            collisionVel *= (1 - Constants.FRICTION)
            this.aimAssist.y += collisionVel

            if (collisionVel > -Constants.MIN_VEL_TOLERANCE):
                #print("Hello")
                break



        #print(this.aimAssist.y)

        