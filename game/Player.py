import pygame
import math
import Constants
import Vector

WHITE = (255, 255, 255)
class Player:
    def __init__(this, stone):

        this.stone = stone
        this.iVel = Constants.INITIAL_DELIVERY
        this.iAngle = math.pi # 180 degrees : down

        this.vector = Vector.Vector(
            this.stone.x,
            this.stone.y,
            math.sin(this.iAngle) * this.iVel,
            -math.cos(this.iAngle) * this.iVel,
            this.stone,
            this.stone.plane
        )

    def input(this, aPressed, dPressed, wPressed, sPressed):

        this.stone.x += Constants.X_MOVE_ACCEL * (dPressed - aPressed)
        this.iVel -= (wPressed - sPressed) * Constants.DELIVERY_ACCEL

        this.stone.x = max(Constants.PLANE_X, min(this.stone.x, Constants.PLANE_X + Constants.PLANE_WIDTH))
        this.iVel = max(-Constants.PLAYER_MAX_VEL, min(this.iVel, 0))


    def updateVecToPlayer(this):

        this.vector.x = this.stone.x
        this.vector.y = this.stone.y
        this.vector.xVector = math.sin(this.iAngle) * this.iVel
        this.vector.yVector = -math.cos(this.iAngle) * this.iVel