import pygame
import Button
import Stone
import GameManager
import Constants

WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Gui:
    def __init__(this, width, height):
        pygame.init()

        #Window
        this.WINDOW_WIDTH = width
        this.WINDOW_HEIGHT = height
        this.WINDOW = pygame.display.set_mode((this.WINDOW_WIDTH, this.WINDOW_HEIGHT))

        this.drawSurface = pygame.Surface((this.WINDOW_WIDTH, this.WINDOW_HEIGHT))
        pygame.display.set_caption("Curling simulator") 
        #Plane
        this.gameManager = GameManager.GameManager()

        #Clock
        this.clock = pygame.time.Clock()

        #Button 
        this.buttons = []
        this.startButton = Button.Button("Press this button to launch red stone up", 100, 100, 400, 100, isVisible=True, font="Times New Roman", fontSize=20)
        this.startButton.addEventListener(this)
        this.buttons.append(this.startButton)

        this.uselessButton = Button.Button("Clicking me does nothing", 100, 200, 400, 100, isVisible=True, fontSize=20, boxOpacity=255)
        this.buttons.append(this.uselessButton)


    def gameLoop(this):

        running = True
        while running: 

            mousePos = pygame.mouse.get_pos()
            mousePressed = pygame.mouse.get_pressed()

            for event in pygame.event.get(): # When the window closes, the program is not running
                if event.type == pygame.QUIT:
                    running = False

            for button in this.buttons:
                if button.isVisible:
                    button.draw(this.drawSurface)
                    button.tick(mousePos, mousePressed[0])


            this.gameManager.gameTick(pygame.key.get_pressed(), this.drawSurface)

            #rect = pygame.Rect(0, 0, 100, 100)

            #pygame.draw.rect(this.drawSurface, (255,0,0), rect,10,3)
            this.WINDOW.blit(this.drawSurface, (0, 0))
            pygame.display.flip()
            this.drawSurface.fill(WHITE)
            this.clock.tick(Constants.FPS)

    def eventFrom(this, button):
        if (button == this.startButton):
            this.gameManager.plane.start() 
            this.gameManager.plane.gameMode = GameManager.MENU

            this.startButton.isVisible = False
            this.uselessButton.isVisible = False

            #this.plane.addStone(30, 150, 430, 2, 0, RED)
    
            #this.plane.addStone(30, 250, 400, 0, 0, YELLOW)
            #this.plane.addStone(30, 250, 460, 0, 0, YELLOW)
            

            #this.plane.addStone(30, 400, 375, 0, 0, YELLOW)
            #this.plane.addStone(30, 400, 490, 0, 0, YELLOW)

            



            

            
        
    