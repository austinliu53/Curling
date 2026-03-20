import Stone
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
    def __init__(this, x : float, y : float, width : float, length : float): # A curling alley is long and narrow. 
        this.x = x
        this.y = y
        this.length = length
        this.width = width
        this.stones = []
        this.ghostStones = []
        this.vectors = []
        this.stoneActive = False

        # Initializing the stones 
        this.playerStone = Stone.Stone(Constants.STONE_RADIUS, 400, 700, 0, 0, RED, this, True)
        this.stones.append(this.playerStone)

        # Initializing player

        this.player = Player.Player(this.playerStone)
    
    def predictPosition(this, movingStone, movingVelocity) -> list:

        stoneActive = True

        # What I'm doing here is that I'm making the player's stone velocity, and then I will copy the array of stones, and then reset the player stone's velocity to 0.
        # This will make a copy of the array, but with a moving player stone. 
        # The original this.stones will remain unchanged.

        stones = []
        for i in range(len(this.stones)):

            stones.append(this.stones[i].ghostCopy())

            
            if (stones[i].equals(movingStone)):

                stones[i].yVel = movingVelocity[1]

            #if (stones[i] == None):
            #    print("you dum")
        

        while (stoneActive):
            
            stoneActive = False
            
            for stone in stones: # Simulate each stone

                # Find the velocity, regardless of direction
                stoneVel = stone.xVel ** 2 + stone.yVel ** 2

                if (stoneVel != 0):
                    stoneActive = True

                # Move the stone based off of its velocity
                stone.x += stone.xVel
                stone.y += stone.yVel

                # Reduce the velocity using friction
                stone.xVel *= (1 - Constants.FRICTION)
                stone.yVel *= (1 - Constants.FRICTION)

                # Detect off-plane stones, and remove them
                if (stone.isOnPlane()):
                    stones.remove(stone)

                # If a stone is slow enough, just stop it.
                if (math.sqrt((stone.xVel ** 2) + (stone.yVel ** 2)) < Constants.MIN_VEL_TOLERANCE):
                    stone.xVel = 0
                    stone.yVel = 0
            
                # Detect collisions for this stone
                if (stone.xVel != 0 or stone.yVel != 0): # If the stone is moving
                    stone.findCollision(stones)

        for stone in stones: # Set the stone.distance
            # Find the distance of this stone to the middle
            stone.isRealStone = False
            xFromMiddle = stone.x - Constants.CIRCLE_CENTER[0]
            yFromMiddle = stone.y - Constants.CIRCLE_CENTER[1]
            stone.distanceToMiddle = math.sqrt(xFromMiddle ** 2 + yFromMiddle ** 2)

        #print(stones == this.stones)
        
        return stones
            # print(stone.yVel)
        # print("stones.append line 21", len(this.stones))
    
    def tick(this, gamemode):

        this.stoneActive = False
        
        for stone in this.stones: # Simulate each stone

            # Find the distance of this stone to the middle
            
            xFromMiddle = stone.x - Constants.CIRCLE_CENTER[0]
            yFromMiddle = stone.y - Constants.CIRCLE_CENTER[1]

            stone.distanceToMiddle = math.sqrt(xFromMiddle ** 2 + yFromMiddle ** 2)

            # Find the velocity, regardless of direction
            stoneVel = stone.xVel ** 2 + stone.yVel ** 2
            if (stoneVel != 0):
                this.stoneActive = True

            # Move the stone based off of its velocity
            stone.x += stone.xVel
            stone.y += stone.yVel

            # Reduce the velocity using friction
            stone.xVel *= (1 - Constants.FRICTION)
            stone.yVel *= (1 - Constants.FRICTION)

            # Detect off-plane stones, and remove them

            #print(len(this.vectors))
            #print(len(this.stones))
            if (stone.isOnPlane()):

                try:
                    this.stones.remove(stone)

                    if (stone.isRealStone):
                        this.vectors.remove(stone.vector)
                except:
                    pass
            
            # If a stone is slow enough, just stop it.
            if (math.sqrt((stone.xVel ** 2) + (stone.yVel ** 2)) < Constants.MIN_VEL_TOLERANCE):
                stone.xVel = 0
                stone.yVel = 0
        
            # Detect collisions for this stone
            if (stone.xVel != 0 or stone.yVel != 0): # If the stone is moving
                stone.findCollision(this.stones)
                stone.vector.updateToStone()    
            
            if (gamemode == GameManager.PRE_DELIVERY):
                this.player.updateVecToPlayer()

            
    

    def startPhysics(this):
        this.playerStone.setVelocity(0, this.player.iVel)
        this.vectors.remove(this.player.vector)

    def draw(this, drawSurface):
        pygame.draw.rect(drawSurface, WHITE, (this.x, this.y, this.width, this.length))

        pygame.draw.circle(drawSurface, BLUE, Constants.CIRCLE_CENTER, Constants.BLUE_CIRCLE_RADIUS)
        pygame.draw.circle(drawSurface, WHITE, Constants.CIRCLE_CENTER, Constants.WHITE_CIRCLE_RADIUS)
        pygame.draw.circle(drawSurface, RED, Constants.CIRCLE_CENTER, Constants.RED_CIRCLE_RADIUS)
        pygame.draw.circle(drawSurface, YELLOW, Constants.CIRCLE_CENTER, Constants.YELLOW_CIRCLE_RADIUS)
        
    def generateStones(this):
        
        this.stones = [this.playerStone]
        numStones = random.randint(2, 5)

        for i in range(numStones):

            if random.randint(0, 4) > 0:
                stoneColor = YELLOW
            else:
                stoneColor = RED
            

            while (True):
                x = this.x + random.randint(Constants.STONE_RADIUS, this.width - Constants.STONE_RADIUS)
                y = (this.y + random.randint(Constants.STONE_RADIUS, Constants.STONE_SPAWN_Y_LIMIT - Constants.STONE_RADIUS))

                tempStone = Stone.Stone(Constants.STONE_RADIUS, x, y, 0, 0, stoneColor, this, True)

                hasCollision = False

                for stone in this.stones:
                    if tempStone.isColliding(stone):
                        hasCollision = True
                
                if not hasCollision:
                    break

                #this.stones.remove(tempStone)
            
            this.stones.append(Stone.Stone(Constants.STONE_RADIUS, x, y, 0, 0, stoneColor, this, True))
        
    



    def calcScore(this):
        # Find the nearest stone.
        try:
            sortedStones = [this.stones[0]]
        except:
            # This means that there is no item in this.stones
            this.player.setScore(0, False)
            return

        # Sort all the stones by their distance using insertion sort
        for stone in this.stones:
            for i in range(len(sortedStones)):
                if sortedStones[i].distanceToMiddle > stone.distanceToMiddle:
                    sortedStones.insert(i, stone)
                    break
                
                if i == len(sortedStones) - 1:
                    sortedStones.append(stone)

        print("")
        
        # Get the team of the closest stone
        
        if (len(sortedStones) > 0 and sortedStones.__contains__(this.stones[0])):
            sortedStones.remove(this.stones[0])
        
        # Pass through the sortedStones list until 
        # the stone is outside of the list
        # or the stone is not the winning team.

        winningTeam = sortedStones[0].color
        print("Winning team:", winningTeam)
        winningPoints = 0

        for sortedStone in sortedStones:

            if (sortedStone.color != winningTeam):
                break
                
            if (sortedStone.distanceToMiddle > Constants.BLUE_CIRCLE_RADIUS + Constants.STONE_RADIUS):
                break

            print(sortedStone.color)

            winningPoints += 1
        
        print("winningPoints", winningPoints)

        if (winningTeam == YELLOW):
            winningPoints *= -1

        this.player.score = winningPoints

    def reset(this):

        this.stones = []
        this.ghostStones = []
        this.vectors = []
        this.stoneActive = False

        # Initializing the stones 
        this.playerStone = Stone.Stone(Constants.STONE_RADIUS, 400, 700, 0, 0, RED, this, True)
        this.stones.append(this.playerStone)

        # Initializing player
        this.player = Player.Player(this.playerStone)
    
            



        

            
        












            

        




                