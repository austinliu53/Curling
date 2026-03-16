import pygame
import Button
import Stone
import GameManager
import Constants
import asyncio


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
        pygame.display.set_caption("Curling Arcade") 
        #Initialize game manager
        this.gameManager = GameManager.GameManager()
        
        #Clock
        this.clock = pygame.time.Clock()

        #Array of all our button

        this.buttons = []

        #Welcome
        this.welcomeLabel = Button.Button("Curling Arcade!", 200, 50, 400, 100, isVisible=True, fontSize=20, boxVisible=False)
        this.buttons.append(this.welcomeLabel)

        this.explainLabel = Button.Button(
            "Slide your stones, bump the opponent's stones out of the ring, and win points!",
            200, 200, 400, 100, isVisible=True, boxVisible=False)
        this.explainLabel.addEventListener(this)
        this.buttons.append(this.explainLabel)
                                          
        this.welcomeButton = Button.Button("Start curling!", 200, 300, 400, 100, 18, isVisible=True)
        this.welcomeButton.addEventListener(this)
        this.buttons.append(this.welcomeButton)
        
        # Curling works:                         

        #Start curling 

        this.startButton = Button.Button("A and D keys to move left or right", 0, 300, 200, 200, isVisible=False, fontSize=12, boxVisible=False)
        this.buttons.append(this.startButton)

        this.startButton = Button.Button("W and S keys to control strength", 0, 300, 200, 200, isVisible=False, fontSize=12, boxVisible=False)
        this.buttons.append(this.startButton)
        
        this.startButton = Button.Button("Press to launch", 0, 300, 200, 200, isVisible=False, fontSize=12)
        this.startButton.addEventListener(this)
        this.buttons.append(this.startButton)

        #Score:

    async def gameLoop(this):



        running = True
        while running: 


            this.drawSurface.fill(GREY)
            this.clock.tick(Constants.FPS)

            mousePos = pygame.mouse.get_pos()
            mousePressed = pygame.mouse.get_pressed()

            for event in pygame.event.get(): # When the window closes, the program is not running
                if event.type == pygame.QUIT:
                    running = False

            Button.checkClicked(mousePressed[0])
            for button in this.buttons:
                if button.isVisible:
                    button.draw(this.drawSurface)
                    button.tick(mousePos)


            this.gameManager.gameTick(pygame.key.get_pressed(), this.drawSurface)

            #rect = pygame.Rect(0, 0, 100, 100)

            #pygame.draw.rect(this.drawSurface, (255,0,0), rect,10,3)
            this.WINDOW.blit(this.drawSurface, (0, 0))
            pygame.display.flip()

            await asyncio.sleep(0)

    def eventFrom(this, button):
        
        if (button == this.welcomeButton):

            this.gameManager.gameMode = GameManager.PRE_DELIVERY
            this.gameManager.plane.generateStones()
            this.welcomeLabel.isVisible = False
            this.welcomeButton.isVisible = False
            this.explainLabel.isVisible = False
            this.startButton.isVisible = True

        if (button == this.startButton):
            this.gameManager.plane.startPhysics() 
            this.gameManager.gameMode = GameManager.SWEEPING

            this.startButton.isVisible = False
        

            #this.plane.addStone(30, 150, 430, 2, 0, RED)
    
            #this.plane.addStone(30, 250, 400, 0, 0, YELLOW)
            #this.plane.addStone(30, 250, 460, 0, 0, YELLOW)
            

            #this.plane.addStone(30, 400, 375, 0, 0, YELLOW)
            #this.plane.addStone(30, 400, 490, 0, 0, YELLOW)

            



            

            
        
    