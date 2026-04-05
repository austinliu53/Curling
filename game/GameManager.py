import Gui

import Player
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
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class GameManager:
    def __init__(this, gui : Gui):
        this.plane = Plane.Plane(Constants.PLANE_X, Constants.PLANE_Y, Constants.PLANE_WIDTH, Constants.PLANE_LENGTH)
        this.gui = gui
        this.gameMode = MENU 

        this.playerGoesFirst = True
        this.difficulty = EASY

        this.playAgainstClanka = True

        this.player1 = Player.Player(RED, this.plane.player1Stone)
        this.player2 = Player.Player(YELLOW, this.plane.player1Stone)

        this.plane.setPlayer(this.player1)
        
        this.currentTurn = this.player1

    def refreshScreen(this):
        this.plane.draw(this.gui.drawSurface)

        font = pygame.font.SysFont("Helvetica", 14)

        fontSurface = font.render("Red Score: " + str(math.floor(this.player1.score)), True, BLACK)
        this.gui.drawSurface.blit(fontSurface, (0, 50))

        fontSurface = font.render("Yellow Score: " + str(math.floor(this.player2.score)), True, BLACK)
        this.gui.drawSurface.blit(fontSurface, (0, 80))

        fontSurface = font.render("Red stones left: " + str(this.player1.stonesLeft), True, BLACK)
        this.gui.drawSurface.blit(fontSurface, (0, 110))

        fontSurface = font.render("Yellow stones left: " + str(this.player2.stonesLeft), True, BLACK)
        this.gui.drawSurface.blit(fontSurface, (0, 140))

        for stone in this.plane.stones:
            stone.draw(this.gui.drawSurface)

        """for vector in this.plane.vectors:
            vector.draw(this.gui.drawSurface)"""

        this.gui.WINDOW.blit(this.gui.drawSurface, (0, 0))
        pygame.display.flip()

    def endSequence(this):
        print("End sequence")
        
        this.plane.player.score = this.plane.calcScore(this.plane.stones)
        
        if this.plane.player.score > 0:
            this.player1.score = this.plane.player.score
            this.player2.score = 0
        else:
            this.player1.score = 0
            this.player2.score = -this.plane.player.score

        if (this.player2.stonesLeft == 0) and (this.player1.stonesLeft == 0):
            if (this.player1.score == 0):
                this.gui.eventFrom("Lose")
            else:
                this.gui.eventFrom("Win")

            this.gameMode = SCORE
            return
        
        if (this.player2.stonesLeft == 0) and (this.player1.stonesLeft == 0):
            if (this.player1.score == 0):
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

        # print(this.gameMode)

        

            # Player has an even number of stones left and it's Player's turn: clanka turn
            # Clanka not has an even number of stones left and it's clanka's turn: clanka turn

            # Player not has even number of stones left and it's Player's turn:  Player turn
            # Clanka has even number of stones left and it's clanka's turn:  Player turn

        if (((this.currentTurn.stonesLeft % 2 == 0) + (this.currentTurn == this.player2)) == 1): # If there's an odd number of stones, then it still hasn't thrown the other one.
            
            if (this.playAgainstClanka): 
                this.gameMode = CLANKA_DELIVERY
                this.gui.eventFrom("clankaThinking")
                this.refreshScreen()
                this.plane.addclankaStone(this.difficulty)
                this.player2.stonesLeft -= 1
                this.gui.eventFrom("clankaStopThinking")

                
            else:
                this.gameMode = PLAYER_DELIVERY
                
                this.plane.addPlayerStone(this.player2)
                this.gui.eventFrom("playerTurn")
            
            this.currentTurn = this.player2
        
        else:
            this.gameMode = PLAYER_DELIVERY
            
            this.plane.addPlayerStone(this.player1)
            this.currentTurn = this.player1

            this.gui.eventFrom("playerTurn")                


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
                this.player1.score = this.plane.player.score
                this.player2.score = 0
            else:
                
                this.player2.score = this.plane.player.score * (-1)
                this.player1.score = 0
                


                """print(this.player2.score == this.plane.player.score * (-1))
                print(this.player2.score, this.plane.player.score * (-1))"""
                


            font = pygame.font.SysFont("Helvetica", 14)
            fontSurface = font.render("Red Score: " + str(this.player1.score), True, BLACK)
            this.gui.drawSurface.blit(fontSurface, (0, 50))

            fontSurface = font.render("Yellow Score: " + str(this.player2.score), True, BLACK)
            this.gui.drawSurface.blit(fontSurface, (0, 80))

            fontSurface = font.render("Red stones left: " + str(this.player1.stonesLeft), True, BLACK)
            this.gui.drawSurface.blit(fontSurface, (0, 110))

            fontSurface = font.render("Yellow stones left: " + str(this.player2.stonesLeft), True, BLACK)
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
            
            this.plane.tick(this.gameMode)

            if (this.gameMode == PLAYER_SWEEPING):
                if not this.plane.stoneActive: # When all stones have stopped moving
                    this.endSequence()
                    return

            # Print the player's score and the clanka's score

            if (this.gameMode == CLANKA_DELIVERY):
                this.gameMode = CLANKA_SWEEPING
                this.plane.stoneActive = True

            if (this.gameMode == CLANKA_SWEEPING):
                if not this.plane.stoneActive: # When all stones have stopped moving
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

        this.currentTurn = this.player1

        this.player1.stonesLeft = Constants.STARTING_STONES
        this.player2.stonesLeft = Constants.STARTING_STONES
        this.player1.score = 0
        this.player2.score = 0

        this.plane.reset()


        
        
            
            

            

    


            


            
            

        
        
        



        
