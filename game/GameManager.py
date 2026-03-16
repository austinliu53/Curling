import Stone
import Plane
import pygame
import Constants

# This class handles the game-level stuff like game status, pages, and inputs.
# For graphics, drawing, buttons and labels, go to Gui.
# For physics and real-time, go to Plane.
# For collision physics, go to Stone.


MENU = 10
PRE_DELIVERY = 20
#DELIVERY = 30
SWEEPING = 40
SCORE = 50



class GameManager:
    def __init__(this):
        this.plane = Plane.Plane(Constants.PLANE_X, Constants.PLANE_Y, Constants.PLANE_WIDTH, Constants.PLANE_LENGTH)
        this.gameMode = MENU
    

    def gameTick(this, keysPressed, drawSurface):

        if (this.gameMode == MENU):
            pass

        elif (this.gameMode == PRE_DELIVERY) or (this.gameMode == SWEEPING):
            
            if (this.gameMode == PRE_DELIVERY): 

                this.plane.player.input(keysPressed[pygame.K_a], keysPressed[pygame.K_d], keysPressed[pygame.K_w], keysPressed[pygame.K_s])
                this.plane.player.vector.draw(drawSurface)
            
            this.plane.tick(this.gameMode)
            
            if (this.gameMode == SWEEPING):
                if not this.plane.stoneActive:

                    this.gameMode = SCORE

            #print(this.gameMode)

            this.plane.draw(drawSurface)

            for stone in this.plane.stones:
                stone.draw(drawSurface)

            for vector in this.plane.vectors:
                vector.draw(drawSurface)

        elif (this.gameMode == SCORE):

            this.plane.draw(drawSurface)

            for stone in this.plane.stones:
                stone.draw(drawSurface)
            
            

            

    


            


            
            

        
        
        



        
