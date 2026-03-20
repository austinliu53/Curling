import Gui
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
    def __init__(this, gui : Gui):
        this.plane = Plane.Plane(Constants.PLANE_X, Constants.PLANE_Y, Constants.PLANE_WIDTH, Constants.PLANE_LENGTH)
        this.gui = gui
        this.gameMode = MENU 
        

    def gameTick(this, keysPressed, drawSurface):

        if (this.gameMode == MENU):
            pass

        elif (this.gameMode == PRE_DELIVERY) or (this.gameMode == SWEEPING):
            
            # Draw the plane first.
            # Then the stones,
            # Then the vectors
            this.plane.draw(drawSurface)

            if (this.gameMode == PRE_DELIVERY): 

                this.plane.player.input(keysPressed[pygame.K_a], keysPressed[pygame.K_d], keysPressed[pygame.K_w], keysPressed[pygame.K_s])
                this.plane.player.vector.draw(drawSurface)
                this.plane.player.updatePathTracer()
                this.plane.player.aimAssist.draw(this.gui.drawSurface)
                
                for stone in this.plane.predictPosition(this.plane.playerStone, [0, this.plane.player.iVel]):
                    stone.draw(this.gui.drawSurface)
                
                
                #print("ghostStones", len(this.plane.ghostStones))
                #print("stones", len(this.plane.stones))
            
            this.plane.tick(this.gameMode)
            
            if (this.gameMode == SWEEPING):
                if not this.plane.stoneActive:

                    this.plane.calcScore()


                    if this.plane.player.score > 0:
                        this.gui.eventFrom("Win")
                    else:
                        this.gui.eventFrom("Lose")

                    this.gameMode = SCORE


            for stone in this.plane.stones:
                stone.draw(drawSurface)

            for vector in this.plane.vectors:
                vector.draw(drawSurface)

            

        elif (this.gameMode == SCORE):
            
            this.plane.draw(drawSurface)

            for stone in this.plane.stones:
                stone.draw(drawSurface)

    def reset(this):
        this.gameMode = PRE_DELIVERY
        this.plane.reset()
        this.plane.generateStones()
        
            
            

            

    


            


            
            

        
        
        



        
