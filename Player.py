import pygame
import math
import Constants
import Vector

WHITE = (255, 255, 255)
class Player:
    def __init__(this, stone):

        this.stone = stone
        this.iVel = Constants.INITIAL_LAUNCH
        this.iAngle = math.pi # 180 degrees : down

        this.vector = Vector.Vector(
            this.stone.x,
            this.stone.y,
            math.sin(this.iAngle) * this.iVel,
            -math.cos(this.iAngle) * this.iVel,
            this.stone,
            this.stone.plane
        )

        this.stone.plane.addVector(this.vector)

    def input(this, leftPressed, rightPressed, wPressed, sPressed):

        this.stone.x += Constants.LAUNCH_MOVEMENT * (rightPressed - leftPressed)
        this.iVel -= (wPressed - sPressed) * 0.5

    def updateVecToPlayer(this):
        this.vector.x = this.stone.x
        this.vector.y = this.stone.y
        this.vector.xVector = math.sin(this.iAngle) * this.iVel
        this.vector.yVector = -math.cos(this.iAngle) * this.iVel