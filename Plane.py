import Stone
import GhostStone
import Constants
import Player
import numpy

WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Plane:
    def __init__(this, length, width): # A curling alley is long and narrow. 
        this.length = length
        this.width = width
        this.stones = []
        this.ghostStones = []
        this.vectors = []

        this.circleCenter = length - 500
        this.smallCircleRadius = 150
        this.mediumCircleRadius = 250
        this.largeCircleRadius = 350

        # Initializing the stones ############################################################
        
        
        this.redStone = Stone.Stone(30, 300, 600, 0, 0, RED, this)
        this.stones.append(this.redStone)

        this.stones.append(Stone.Stone(30, 250, 400, 0, 0, YELLOW, this))
        this.stones.append(Stone.Stone(30, 310, 400, 0, 0, YELLOW, this))
        this.stones.append(Stone.Stone(30, 370, 400, 0, 0, YELLOW, this))

        this.player = Player.Player(this.redStone)

    def addStone(this, stone):
        this.stones.append(stone)

    def addGhostStone(this, stone):
        
        this.ghostStones.append(GhostStone.GhostStone(stone.radius, stone.x, stone.y, 
            (
                stone.color[0], 
                stone.color[1], 
                stone.color[2],
                Constants.GHOST_OPACITY
            )    
        ))

    def addVector(this, vector):
        this.vectors.append(vector)
    def tick(this):
        
        for stone in this.stones: # Simulate each stone

            stone.x += stone.xVel
            stone.y += stone.yVel

            stone.xVel *= (1 - stone.friction)
            stone.yVel *= (1 - stone.friction)

            if ((stone.xVel ** 2) + (stone.yVel ** 2) < Constants.MIN_VEL_TOLERANCE):
                stone.xVel = 0
                stone.yVel = 0
        
            if (stone.xVel != 0 or stone.yVel != 0): # If the stone is moving
                stone.findCollision(this.stones)
                stone.vector.updateToStone()    
            
            this.player.updateVecToPlayer()



            # print(stone.yVel)
        # print("stones.append line 21", len(this.stones))

    def start(this):
        this.redStone.setVelocity(0, this.player.iVel)


                
