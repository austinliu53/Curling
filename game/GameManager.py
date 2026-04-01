import Gui
import Plane
import Constants

import pygame
import math
# This class handles the game-level stuff like game status, pages, and inputs.
# For graphics, drawing, buttons and labels, go to Gui.
# For physics and real-time, go to Plane.
# For collision physics, go to Stone.


# Gamemode
MENU = 10
PLAYER_DELIVERY = 20
PLAYER_SWEEPING = 40
SCORE = 50
CLANKA_DELIVERY = 60
CLANKA_SWEEPING = 70

# Game difficulty
EASY = 100
MEDIUM = 200
HARD = 300
EVIL = 400


BLACK = (0, 0, 0)

class GameManager:
    def __init__(this, gui : Gui):
        this.plane = Plane.Plane(Constants.PLANE_X, Constants.PLANE_Y, Constants.PLANE_WIDTH, Constants.PLANE_LENGTH)
        this.gui = gui
        this.gameMode = MENU 

        this.playerGoesFirst = True
        this.difficulty = EASY

        this.playerScore = 0
        this.clankaScore = 0

        this.playerStonesLeft = Constants.STARTING_STONES
        this.clankaStonesLeft = Constants.STARTING_STONES

    def refreshScreen(this):
        this.plane.draw(this.gui.drawSurface)

        font = pygame.font.SysFont("Helvetica", 14)

        fontSurface = font.render("Player Score: " + str(math.floor(this.playerScore)), True, BLACK)
        this.gui.drawSurface.blit(fontSurface, (0, 50))

        fontSurface = font.render("Clanka Score: " + str(math.floor(this.clankaScore)), True, BLACK)
        this.gui.drawSurface.blit(fontSurface, (0, 80))

        fontSurface = font.render("Player stones left: " + str(this.playerStonesLeft), True, BLACK)
        this.gui.drawSurface.blit(fontSurface, (0, 110))

        fontSurface = font.render("Clanka stones left: " + str(this.clankaStonesLeft), True, BLACK)
        this.gui.drawSurface.blit(fontSurface, (0, 140))

        for stone in this.plane.stones:
            stone.draw(this.gui.drawSurface)

        """for vector in this.plane.vectors:
            vector.draw(this.gui.drawSurface)"""

        this.gui.WINDOW.blit(this.gui.drawSurface, (0, 0))
        pygame.display.flip()

    def endSequence(this):
        #print("End sequence")

        this.plane.player.score = this.plane.calcScore(this.plane.stones)
        
        if this.plane.player.score > 0:
            this.playerScore = this.plane.player.score
            this.clankaScore = 0
        else:
            this.playerScore = 0
            this.clankaScore = -this.plane.player.score

        if (this.clankaStonesLeft == 0) and (this.playerStonesLeft == 0):
            if (this.playerScore == 0):
                this.gui.eventFrom("Lose")
            else:
                this.gui.eventFrom("Win")

            this.gameMode = SCORE
            return

        for stone in this.plane.stones:

            stone.lastCollision = None # Reset "last collisions"

            if (stone.y) <= Constants.CIRCLE_CENTER[1] - Constants.BLUE_CIRCLE_RADIUS: # 
                this.plane.stones.remove(stone)
                this.plane.vectors.remove(stone.vector)

        if (this.gameMode == CLANKA_SWEEPING):
            if (this.clankaStonesLeft % 2 == 1): # If there's an odd number of stones, then it still hasn't thrown the other one.
                this.gameMode = CLANKA_DELIVERY
                this.gui.eventFrom("clankaThinking")
                this.refreshScreen()
                this.plane.addclankaStone(this.difficulty)
                this.clankaStonesLeft -= 1
                this.gui.eventFrom("clankaStopThinking")
            else:
                this.gameMode = PLAYER_DELIVERY
                this.gui.eventFrom("playerTurn")
                this.plane.addPlayerStone()
                this.playerStonesLeft -= 1
        
        if (this.gameMode == PLAYER_SWEEPING):

            if (this.playerStonesLeft % 2 == 1):
                this.gameMode = PLAYER_DELIVERY
                this.gui.eventFrom("playerTurn")
                this.plane.addPlayerStone()
                this.playerStonesLeft -= 1
            else:
                this.gameMode = CLANKA_DELIVERY
                this.gui.eventFrom("clankaThinking")
                this.refreshScreen()
                this.plane.addclankaStone(this.difficulty)
                this.clankaStonesLeft -= 1
                this.gui.eventFrom("clankaStopThinking")

    def gameTick(this, keysPressed, mousePos):

        if (this.gameMode == MENU):
            pass

        elif (this.gameMode == PLAYER_DELIVERY) or (this.gameMode == PLAYER_SWEEPING) or (this.gameMode == CLANKA_DELIVERY) or (this.gameMode == CLANKA_SWEEPING):
            
            # Draw the plane first.
            # Then the stones,
            # Then the vectors
            this.plane.draw(this.gui.drawSurface)

            # Calculate the score always
            this.plane.player.score = this.plane.calcScore(this.plane.stones)

            if this.plane.player.score > 0:
                this.playerScore = this.plane.player.score
                this.clankaScore = 0
            else:
                this.playerScore = 0
                this.clankaScore = -this.plane.player.score

            font = pygame.font.SysFont("Helvetica", 14)
            fontSurface = font.render("Player Score: " + str(math.floor(this.playerScore)), True, BLACK)
            this.gui.drawSurface.blit(fontSurface, (0, 50))

            fontSurface = font.render("Clanka Score: " + str(math.floor(this.clankaScore)), True, BLACK)
            this.gui.drawSurface.blit(fontSurface, (0, 80))

            fontSurface = font.render("Player stones left: " + str(this.playerStonesLeft), True, BLACK)
            this.gui.drawSurface.blit(fontSurface, (0, 110))

            fontSurface = font.render("Clanka stones left: " + str(this.clankaStonesLeft), True, BLACK)
            this.gui.drawSurface.blit(fontSurface, (0, 140))

            for stone in this.plane.stones:
                stone.draw(this.gui.drawSurface)

            """for vector in this.plane.vectors:
                vector.draw(this.gui.drawSurface)"""

            if (this.gameMode == PLAYER_DELIVERY): 
                
                this.plane.player.input(keysPressed[pygame.K_a], keysPressed[pygame.K_d], keysPressed[pygame.K_w], keysPressed[pygame.K_s])
                this.plane.player.vector.draw(this.gui.drawSurface)
                this.plane.player.updatePathTracer()
                this.plane.player.aimAssist.draw(this.gui.drawSurface)

                """if (keysPressed[pygame.K_p]): # If key p pressed, find optimal position.

                    pos = this.plane.findOptimal()
                    this.plane.player.iVel = pos[0]
                    this.plane.playerStone.x = pos[1]"""
                
                predictedPosition = this.plane.predictPosition(this.plane.playerStone, [0, this.plane.player.iVel])
                
                
                for stone in predictedPosition:
                    stone.draw(this.gui.drawSurface)
                

                font = pygame.font.SysFont("Helvetica", 14)
                fontSurface = font.render(str(math.floor(this.plane.positionPoints(predictedPosition))), True, BLACK)
                this.gui.drawSurface.blit(fontSurface, (0, 0))
                
                #print("ghostStones", len(this.plane.ghostStones))
                #print("stones", len(this.plane.stones))
            
            this.plane.tick(this.gameMode)

            if (this.gameMode == PLAYER_SWEEPING):
                if not this.plane.stoneActive: # When all stones have settled down
                    this.endSequence()
                    return

            # Print the player's score and the clanka's score

            if (this.gameMode == CLANKA_DELIVERY):
                
                this.gameMode = CLANKA_SWEEPING
                this.plane.stoneActive = True

            if (this.gameMode == CLANKA_SWEEPING):
                if not this.plane.stoneActive: # When all stones have settled down
                    this.endSequence()
                    return

        elif (this.gameMode == SCORE):
            
            this.plane.draw(this.gui.drawSurface)

            for stone in this.plane.stones:
                stone.draw(this.gui.drawSurface)

        font = pygame.font.SysFont("Helvetica", 14)

        fontSurface = font.render("Mouse: " + str(mousePos), True, BLACK)
        this.gui.drawSurface.blit(fontSurface, (600, 0))

        #print(this.gameMode)

    def reset(this):
        this.clankaStonesLeft = Constants.STARTING_STONES
        this.playerStonesLeft = Constants.STARTING_STONES
        this.playerScore = 0
        this.clankaScore = 0
        this.plane.reset()


        
        
            
            

            

    


            


            
            

        
        
        



        
