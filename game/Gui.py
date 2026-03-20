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
GREEN = (0, 255, 0)
class Gui:
    def __init__(this, width : int, height : int):
        pygame.init()

        #Window
        this.WINDOW_WIDTH = width
        this.WINDOW_HEIGHT = height
        this.WINDOW = pygame.display.set_mode((this.WINDOW_WIDTH, this.WINDOW_HEIGHT))

        this.drawSurface = pygame.Surface((this.WINDOW_WIDTH, this.WINDOW_HEIGHT))
        pygame.display.set_caption("Curling Arcade") 
        #Initialize game manager
        this.gameManager = GameManager.GameManager(this)
        
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

        this.controlsLabel = Button.Button(["A and D keys to move left or right", "W and S keys to control strength"], 0, 100, 200, 200, isVisible=False, fontSize=12, boxVisible=False)
        this.buttons.append(this.controlsLabel)

        this.startButton = Button.Button("Press to launch", 0, 300, 200, 200, fontSize=12, isVisible=False)
        this.startButton.addEventListener(this)
        this.buttons.append(this.startButton)

        #Score:
        this.scoreButton = Button.Button([], 200, 400, 400, 200, fontSize=25, isVisible=False)
        this.scoreButton.addEventListener(this)
        this.buttons.append(this.scoreButton)

    async def gameLoop(this):



        running = True
        while running: 


            this.drawSurface.fill(GREY)
            this.clock.tick(Constants.FPS)

            mousePos = pygame.mouse.get_pos()
            mousePressed = pygame.mouse.get_pressed()

            Button.checkClicked(mousePressed[0])
            this.gameManager.gameTick(pygame.key.get_pressed(), this.drawSurface)

            for event in pygame.event.get(): # When the window closes, the program is not running
                if event.type == pygame.QUIT:
                    running = False

            
            for button in this.buttons:
                if button.isVisible:
                    button.draw(this.drawSurface)
                    button.tick(mousePos)

            this.WINDOW.blit(this.drawSurface, (0, 0))
            pygame.display.flip()

            await asyncio.sleep(0)

    def eventFrom(this, trigger):
        
        if (trigger == this.welcomeButton):
            

            this.gameManager.gameMode = GameManager.PRE_DELIVERY
            this.gameManager.plane.generateStones()
            this.welcomeLabel.isVisible = False
            this.welcomeButton.isVisible = False
            this.explainLabel.isVisible = False
            this.startButton.isVisible = True
            this.controlsLabel.isVisible = True
            

        if (trigger == this.startButton):
            this.gameManager.plane.startPhysics() 
            this.gameManager.gameMode = GameManager.SWEEPING

            this.controlsLabel.isVisible = False
            this.startButton.isVisible = False
        
        if (trigger == "Win"):
            
            this.scoreButton.text = ["You win! ", "Score: " + str(this.gameManager.plane.player.score), "Click to play again."]
            this.scoreButton.textColor = GREEN
            this.scoreButton.isVisible = True
            

        if (trigger == "Lose"):
            
            this.scoreButton.text = ["You lose!", "Click to play again"]
            this.scoreButton.textColor = RED
            this.scoreButton.isVisible = True
            #this.plane.addStone(30, 150, 430, 2, 0, RED)
    
            #this.plane.addStone(30, 250, 400, 0, 0, YELLOW)
            #this.plane.addStone(30, 250, 460, 0, 0, YELLOW)
            

            #this.plane.addStone(30, 400, 375, 0, 0, YELLOW)
            #this.plane.addStone(30, 400, 490, 0, 0, YELLOW)

        if (trigger == this.scoreButton):
            
            this.gameManager.reset()

            this.scoreButton.isVisible = False
            this.explainLabel.isVisible = False
            this.startButton.isVisible = True
            this.controlsLabel.isVisible = True

            



            

            
        
    