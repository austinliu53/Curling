import Stone
import GhostStone
import Constants
import Player
import GameManager

import pygame
import random
import math
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

class Plane:
    def __init__(this, x, y, width, length): # A curling alley is long and narrow. 
        this.x = x
        this.y = y
        this.length = length
        this.width = width
        this.stones = []
        this.ghostStones = []
        this.vectors = []
        this.stoneActive = False



        # Initializing the stones 
        this.redStone = Stone.Stone(Constants.STONE_RADIUS, 400, 700, 0, 0, RED, this)
        this.stones.append(this.redStone)

        # Initializing player

        this.player = Player.Player(this.redStone)

    def addStone(this, stone):
        this.stones.append(stone)

    def addGhostStone(this, stone):
        
        this.ghostStones.append(GhostStone.GhostStone(stone.radius, stone.x, stone.y, 
            (
                stone.color[0], 
                stone.color[1], 
                stone.color[2]
                #,Constants.GHOST_OPACITY
            )    
        ))

    def addVector(this, vector):
        this.vectors.append(vector)
    def tick(this, gamemode):

        this.stoneActive = False
        
        for stone in this.stones: # Simulate each stone
            
            stoneVel = stone.xVel ** 2 + stone.yVel ** 2
            if (stoneVel != 0):
                this.stoneActive = True

            stone.x += stone.xVel
            stone.y += stone.yVel

            stone.xVel *= (1 - stone.friction)
            stone.yVel *= (1 - stone.friction)

            if (stone.isOnPlane()):
                this.stones.remove(stone)
                this.vectors.remove(stone.vector)
            if ((stone.xVel ** 2) + (stone.yVel ** 2) < Constants.MIN_VEL_TOLERANCE):
                stone.xVel = 0
                stone.yVel = 0
        
            if (stone.xVel != 0 or stone.yVel != 0): # If the stone is moving
                stone.findCollision(this.stones)
                stone.vector.updateToStone()    
            
            if (gamemode == GameManager.PRE_DELIVERY):
                this.player.updateVecToPlayer()


            # print(stone.yVel)
        # print("stones.append line 21", len(this.stones))

    def startPhysics(this):
        this.redStone.setVelocity(0, this.player.iVel)
        this.vectors.remove(this.player.vector)

    def draw(this, drawSurface):
        pygame.draw.rect(drawSurface, WHITE, (this.x, this.y, this.width, this.length))

        pygame.draw.circle(drawSurface, BLUE, Constants.CIRCLE_CENTER, Constants.BLUE_CIRCLE_RADIUS)
        pygame.draw.circle(drawSurface, WHITE, Constants.CIRCLE_CENTER, Constants.WHITE_CIRCLE_RADIUS)
        pygame.draw.circle(drawSurface, RED, Constants.CIRCLE_CENTER, Constants.RED_CIRCLE_RADIUS)
        pygame.draw.circle(drawSurface, YELLOW, Constants.CIRCLE_CENTER, Constants.YELLOW_CIRCLE_RADIUS)
        
    def generateStones(this):
        
        numStones = random.randint(2, 5)

        for i in range(numStones):

            if (i % 2 == 1):
                stoneColor = RED
            else:
                stoneColor = YELLOW
            
            


            while (True):
                x = this.x + random.randint(Constants.STONE_RADIUS, this.width - Constants.STONE_RADIUS)
                y = (this.y + random.randint(Constants.STONE_RADIUS, Constants.STONE_SPAWN_Y_LIMIT - Constants.STONE_RADIUS))

                tempStone = Stone.Stone(Constants.STONE_RADIUS, x, y, 0, 0, stoneColor, this)

                hasCollision = False

                for stone in this.stones:
                    if tempStone.isColliding(stone):
                        hasCollision = True
                
                if not hasCollision:
                    break
            
            this.stones.append(Stone.Stone(Constants.STONE_RADIUS, x, y, 0, 0, stoneColor, this))

    """
    def calcScore(this):
        # Find the nearest stone.

        closestStone = None # placeholder

        sortedStones = []

        for stone in this.stones:

            xFromMiddle = stone.x - Constants.CIRCLE_CENTER[0]
            yFromMiddle = stone.y - Constants.CIRCLE_CENTER[1]

            stone.distanceToMiddle = math.sqrt(xFromMiddle ** 2 + yFromMiddle ** 2)

            if len(sortedStones) == 0:
                sortedStones.append(stone)

                
            for stone in sortedStones:
                if sortedStones:


        # Get the team of the closest stone
        color = closestStone.color

        if (color = )

    """
        

            
        












            

        




                