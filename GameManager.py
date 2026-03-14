import Stone
import Plane
import pygame
import Constants

# This class handles the game-level stuff like game status, pages, and inputs.
# For graphics, drawing, buttons and labels, go to Gui.
# For physics and real-time, go to Plane.
# For collision physics, go to Stone.


MENU = 10
DELIVERY = 20
SWEEPING = 30

class GameManager:
    def __init__(this):
        this.plane = Plane.Plane(500, 50)
        this.gameMode = DELIVERY
    
    def gameTick(this, keysPressed, drawSurface):
        for ghostStone in this.plane.ghostStones:
            ghostStone.draw(drawSurface)
            
        this.plane.player.input(keysPressed[pygame.K_a], keysPressed[pygame.K_d], keysPressed[pygame.K_w], keysPressed[pygame.K_s])
        this.plane.tick()

        for stone in this.plane.stones:
            stone.draw(drawSurface)

        for vector in this.plane.vectors:
            vector.draw(drawSurface)

        
        
        



        
