import Stone
import Constants
import Player
import Vector
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
        this.player = None

        # Initializing the stones 
        this.player1Stone = Stone.Stone(Constants.STONE_RADIUS, -400, 700, 0, 0, RED, this, True)

        this.stones.append(this.player1Stone)

        this.clankaStone = None 

        # Initializing player
    
    def setPlayer(this, player: Player):
        this.player = player

    def startPhysics(this):
        this.playerStone.setVelocity(0, this.player.iVel)
        this.vectors.remove(this.player.vector)

    def draw(this, drawSurface: pygame.Surface):
        pygame.draw.rect(drawSurface, WHITE, (this.x, this.y, this.width, this.length))

        pygame.draw.circle(drawSurface, BLUE, Constants.CIRCLE_CENTER, Constants.BLUE_CIRCLE_RADIUS)
        pygame.draw.circle(drawSurface, WHITE, Constants.CIRCLE_CENTER, Constants.WHITE_CIRCLE_RADIUS)
        pygame.draw.circle(drawSurface, RED, Constants.CIRCLE_CENTER, Constants.RED_CIRCLE_RADIUS)
        pygame.draw.circle(drawSurface, YELLOW, Constants.CIRCLE_CENTER, Constants.YELLOW_CIRCLE_RADIUS)
        
    
    def generateStones(this):
        
        try:
            this.stones = [this.playerStone]
        except:
            pass
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
        
    def addclankaStone(this, difficulty):

        this.clankaStone = Stone.Stone(Constants.STONE_RADIUS, 400, 700, 0, 0, YELLOW, this, True)

        this.stones.append(this.clankaStone)

        pos = this.findOptimal(difficulty)

        this.clankaStone.yVel = pos[0]
        this.clankaStone.x = pos[1]
        
        #print(len(this.stones))

    def addPlayerStone(this, currentTurn):
        this.playerStone = Stone.Stone(Constants.STONE_RADIUS, 400, 700, 0, 0, currentTurn.color, this, True)
        this.stones.append(this.playerStone)
        this.player.stone = this.playerStone
        this.player.vector = Vector.Vector(
            this.playerStone.x,
            this.playerStone.y,
            0,
            Constants.INITIAL_DELIVERY,
            this.playerStone
        )

        currentTurn.stonesLeft -= 1

    def reset(this):

        this.stones = []
        this.ghostStones = []
        this.vectors = []
        this.stoneActive = False
        """
        # Initializing the stones 
        this.playerStone = Stone.Stone(Constants.STONE_RADIUS, 400, 700, 0, 0, RED, this, True)
        this.stones.append(this.playerStone)

        # Initializing player
        this.player = Player.Player(this.playerStone)"""

    def sortStonesDistance(this, stones):

        # Find the nearest stone.
        try:
            sortedStones = [stones[0]]
        except:
            # This means that there is no item in stones
            this.player.score = 0
            return []

        # Sort all the stones by their distance using insertion sort
        for stone in stones:
            for i in range(len(sortedStones)):
                if sortedStones[i].distanceToMiddle > stone.distanceToMiddle:
                    sortedStones.insert(i, stone)
                    break
                
                if i == len(sortedStones) - 1:
                    sortedStones.append(stone)

        #print("")
        
        # Get the team of the closest stone
        
        if (len(sortedStones) > 0 and sortedStones.__contains__(this.stones[0])): # Add the length first for a bit of memory optimization
            sortedStones.remove(this.stones[0])
        
        return sortedStones
    


    def calcScore(this, stones):

        sortedStones = this.sortStonesDistance(stones)
        
        # Pass through the sortedStones list until 
        # the stone is outside of the list
        # or the stone is not the winning team.

        if (len(sortedStones) == 0):
            return 0
        
        winningTeam = sortedStones[0].color

        winningPoints = 0

        for sortedStone in sortedStones:

            if (sortedStone.color != winningTeam):
                break
                
            if (sortedStone.distanceToMiddle > Constants.BLUE_CIRCLE_RADIUS + Constants.STONE_RADIUS):
                break

            #print(sortedStone.color)

            winningPoints += 1
    

        if (winningTeam == YELLOW):
            winningPoints *= -1

        this.player.score = winningPoints

        return winningPoints

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

                #print(movingVelocity[1], "helo")

            #if (stones[i] == None):


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
    
    def positionPoints(this, stones): # This number is based off of the overall position of the player. The worse position for the player, the more the clanka will play.

        # Find how much points you got.
        endPoints = this.calcScore(stones)

        points = 1000 * endPoints 

        for stone in stones:

            if (stone.color == RED):
                if stone.distanceToMiddle <= 2 * stone.radius + Constants.BLUE_CIRCLE_RADIUS:
                    points += 500
                points += stone.stoneEffectiveness()
            else:
                if stone.distanceToMiddle <= 2 * stone.radius + Constants.BLUE_CIRCLE_RADIUS:
                    points -= 500
                points -= stone.stoneEffectiveness()
            
        return points
    
    def findStoneExtremes(this, stones, excludedStone):
        
        minX = math.inf
        maxX = -math.inf

        minY = math.inf
        maxY = -math.inf

        for stone in stones:

            if not stone.equals(excludedStone):
                if stone.x <= minX:
                    minX = stone.x
                if stone.x >= maxX:
                    maxX = stone.x
                if stone.y <= minY:
                    minY = stone.y
                if stone.y >= maxY:
                    maxY = stone.y

        return [[minX, maxX], [minY, maxY]]
    
    def findOptimal(this, difficulty): # This algorithm gets the scoring of all potential positions, and finds which one helps the bot's position the most.

        # Firstly, we will do coarse calculations for every shot that is not going to collide. 
        # Next, there will be 100% percent accuracy calculations for shots that will collide.
        
        if (difficulty == GameManager.EASY):
            
            if (len(this.stones) >= 1):
                randomX = random.randint(Constants.CIRCLE_CENTER[0] - Constants.BLUE_CIRCLE_RADIUS, Constants.CIRCLE_CENTER[0] + Constants.BLUE_CIRCLE_RADIUS)

                randomIVel = (this.clankaStone.y - random.randint(
                        Constants.CIRCLE_CENTER[1] - Constants.BLUE_CIRCLE_RADIUS, Constants.CIRCLE_CENTER[1] + Constants.BLUE_CIRCLE_RADIUS
                        )
                    ) * Constants.FRICTION

                return (-randomIVel, randomX)
            else:
                extremes = this.findStoneExtremes(this.stones, this.clankaStone)

            xChoice = random.randint(int(extremes[0][0]), int(extremes[0][1])) + random.randint(-50, 50)
            xChoice = max(Constants.PLANE_X, min(Constants.PLANE_X + Constants.PLANE_WIDTH, xChoice))

            iVelChoice = int((this.clankaStone.y - random.randint(int(extremes[1][0]), int(extremes[1][1]))) / Constants.FRICTION) # A random launch between the minimum and the maximum distance stone already shot.
            
            return (iVelChoice, xChoice)
        

        optimalPoints = -math.inf
        optimalShot = (0, Constants.PLANE_X)

        iVel = 0
        this.clankaStone.x = 0

        passes = 0
        positionsCalculated = 0

        if (difficulty == GameManager.MEDIUM):
            xPrecision = 10 * Constants.X_MOVE_ACCEL
        else:
            xPrecision = 5 * Constants.X_MOVE_ACCEL

        while iVel <= Constants.PLAYER_MAX_VEL:
            
            launchX = Constants.PLANE_X # All the way left.

            while launchX <= Constants.PLANE_X + Constants.PLANE_WIDTH:
                passes += 1

                predictPosition = this.predictPosition(this.clankaStone, [0, -iVel])
                points = -this.positionPoints(predictPosition)

                positionsCalculated += 1
                
                #print("points", points, iVel)
                if (points > optimalPoints):
                    #print(launchX, iVel, points, len(this.stones))
    
                    optimalPoints = points
                    optimalShot = (iVel, launchX)

                launchX += xPrecision

                this.clankaStone.x = launchX

            iVel += Constants.DELIVERY_ACCEL * 20

        if (difficulty != GameManager.EVIL):
            return (-optimalShot[0], optimalShot[1])

        # Reset the theoretical position for another finer comb
        iVel = 0
        this.clankaStone.x = 0

        previousStones = [stone for stone in this.stones if stone != this.clankaStone] # the current stones that exclude the clanka stone
        # print(len(previousStones))
        # Finer comb        
        
        while iVel <= Constants.PLAYER_MAX_VEL:
            
            launchX = Constants.PLANE_X 

            while launchX <= Constants.PLANE_X + Constants.PLANE_WIDTH:
                
                passes += 1

                predictY = this.clankaStone.y - (iVel / Constants.FRICTION)

                for stone in previousStones:

                    if stone.willThisShadow(this.clankaStone.x, predictY, Constants.STONE_RADIUS): # If it will collide
                        #print("stone pos", stone.x, stone.y, "this pos", this.clankaStone.x, predictY)
                        predictPosition = this.predictPosition(this.clankaStone, [0, -iVel])
                        points = -this.positionPoints(predictPosition)
                        positionsCalculated += 1
                        #print(positionsCalculated)
                
                        #print("points", points, iVel)
                        if (points > optimalPoints):
                            #print(launchX, iVel, points, len(this.stones))
            
                            optimalPoints = points
                            optimalShot = (iVel, launchX)
                        
                        break
                    
                launchX += Constants.X_MOVE_ACCEL * 1

                this.clankaStone.x = launchX

            iVel += Constants.DELIVERY_ACCEL * 2

        """print("Optimal points: ", optimalPoints)
        print("passes", passes)"""

        print("positionsCalculated", positionsCalculated)
        # Record: 15093 passes

        return (-optimalShot[0], optimalShot[1])
            
    def tick(this, gamemode):

        this.stoneActive = False
        
        for stone in this.stones: # Simulate each stone

            # Find the distance of this stone to the middle
            
            xFromMiddle = stone.x - Constants.CIRCLE_CENTER[0]
            yFromMiddle = stone.y - Constants.CIRCLE_CENTER[1]

            stone.distanceToMiddle = math.sqrt(xFromMiddle ** 2 + yFromMiddle ** 2)

            # Find the velocity, regardless of direction
            stoneVel = stone.xVel ** 2 + stone.yVel ** 2

            #print(stone.x, stone.y, stoneVel)
            if (stoneVel != 0):
                this.stoneActive = True

            # Move the stone based off of its velocity
            stone.x += stone.xVel
            stone.y += stone.yVel

            # Reduce the velocity using friction
            stone.xVel *= (1 - Constants.FRICTION)
            stone.yVel *= (1 - Constants.FRICTION)

            #Detect off-plane stones, and remove them
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
            
            if (gamemode == GameManager.PLAYER_DELIVERY):
                this.player.updateVecToPlayer()

            
    



        

            
        












            

        




                