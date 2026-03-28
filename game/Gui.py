import pygame
import Button
import Stone
import GameManager
import Constants
import asyncio


WHITE = (255, 255, 255)
GREY = (127, 127, 127)
LIGHT_BLUE = (100, 127, 255)
LIGHTER_BLUE = (127, 157, 255)
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

        # Welcome to the game!
        this.welcomeLabel = Button.Button("Curling Arcade!", 200, 50, 400, 100, isVisible=True, fontSize=20, boxVisible=False, fillColor=LIGHTER_BLUE)
        this.buttons.append(this.welcomeLabel)

        this.explainLabel = Button.Button(
            "Slide your stones, bump the opponent's stones out of the ring, and win points!",
            200, 200, 400, 100, isVisible=True, boxVisible=False, fillColor=LIGHTER_BLUE)
        this.explainLabel.addEventListener(this)
        this.buttons.append(this.explainLabel)
                                          
        this.welcomeButton = Button.Button("Play against clanka", 200, 300, 400, 100, fontSize=18, isVisible=True, fillColor=LIGHTER_BLUE)
        this.welcomeButton.addEventListener(this)
        this.buttons.append(this.welcomeButton)
        
        # So, play first or play second ????

        this.selectOrderLabel = Button.Button("Select your order.", 200, 300, 400, 100, fontSize=36, isVisible=False, boxVisible=False)
        this.selectOrderLabel.addEventListener(this)
        this.buttons.append(this.selectOrderLabel)

        this.playFirstButton = Button.Button(["Play first", "(This is harder)"], 200, 400, 400, 100, fontSize=18, isVisible=False, fillColor=LIGHTER_BLUE)
        this.playFirstButton.addEventListener(this)
        this.buttons.append(this.playFirstButton)

        this.playSecondButton = Button.Button(["Play second", "(This is easier)"], 200, 500, 400, 100, fontSize=18, isVisible=False, fillColor=LIGHTER_BLUE)
        this.playSecondButton.addEventListener(this)
        this.buttons.append(this.playSecondButton)
        
        # Started curling 

        this.controlsLabel = Button.Button(["A and D keys to move left or right", "W and S keys to control strength"], 0, 100, 200, 200, isVisible=False, fontSize=12, boxVisible=False, fillColor=LIGHTER_BLUE)
        this.buttons.append(this.controlsLabel)

        this.startButton = Button.Button("Press to launch", 0, 300, 200, 200, fontSize=12, isVisible=False, fillColor=LIGHTER_BLUE)
        this.startButton.addEventListener(this)
        this.buttons.append(this.startButton)

        # Clanker is thinking...
        this.clankaThinkingLabel = Button.Button(["The clanka is thinking..."], 300, 650, 200, 100, isVisible=False, fontSize=12, boxVisible=False, fillColor=LIGHTER_BLUE)
        this.buttons.append(this.clankaThinkingLabel)

        #Score:
        this.continueButton = Button.Button([], 200, 400, 400, 200, fontSize=25, isVisible=False, fillColor=LIGHTER_BLUE)
        this.continueButton.addEventListener(this)
        this.buttons.append(this.continueButton)

    async def gameLoop(this):



        running = True
        while running: 


            this.drawSurface.fill(LIGHT_BLUE)
            this.clock.tick(Constants.FPS)

            mousePos = pygame.mouse.get_pos()
            mousePressed = pygame.mouse.get_pressed()

            Button.checkClicked(mousePressed[0])
            this.gameManager.gameTick(pygame.key.get_pressed(), pygame.mouse.get_pos())

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

            this.selectOrderLabel.isVisible = True
            this.playFirstButton.isVisible = True
            this.playSecondButton.isVisible = True
            
            #this.gameManager.plane.generateStones()
            this.welcomeLabel.isVisible = False
            this.welcomeButton.isVisible = False
            this.explainLabel.isVisible = False
            """
            this.startButton.isVisible = True
            this.controlsLabel.isVisible = True"""
        
        if (trigger == this.playFirstButton): 
            this.gameManager.gameMode = GameManager.CLANKA_SWEEPING 
            this.selectOrderLabel.isVisible = False
            this.playFirstButton.isVisible = False
            this.playSecondButton.isVisible = False
        
        if (trigger == this.playSecondButton):
            this.gameManager.gameMode = GameManager.PLAYER_SWEEPING
            this.selectOrderLabel.isVisible = False
            this.playFirstButton.isVisible = False
            this.playSecondButton.isVisible = False

        if (trigger == this.startButton):
            this.gameManager.plane.startPhysics()
            this.gameManager.gameMode = GameManager.PLAYER_SWEEPING

            this.controlsLabel.isVisible = False
            this.startButton.isVisible = False
        
        if (trigger == "Win"):
            this.continueButton.text = ["Red points this end: " + str(this.gameManager.plane.player.score), "You win!", "Click to go to main screen."]
            this.continueButton.textColor = BLACK
            this.continueButton.isVisible = True
            
        if (trigger == "Lose"):

            this.continueButton.text = ["Yellow points this end:" + str(-this.gameManager.plane.player.score), "You lose!", "Click to go to main screen."]
            this.continueButton.textColor = BLACK
            this.continueButton.isVisible = True
            
        if (trigger == this.continueButton):
            
            this.gameManager.reset()
            this.gameManager.gameMode = GameManager.MENU

            this.welcomeLabel.isVisible = True
            this.explainLabel.isVisible = True
            this.welcomeButton.isVisible = True

            this.continueButton.isVisible = False
            
            this.startButton.isVisible = False
            this.controlsLabel.isVisible = False


        if (trigger == "clankaThinking"):
            this.clankaThinkingLabel.isVisible = True
            this.clankaThinkingLabel.draw(this.drawSurface)
            print("clanka think")
        if (trigger == "clankaStopThinking"):
            this.clankaThinkingLabel.isVisible = False
            this.clankaThinkingLabel.draw(this.drawSurface)
            print("clanka no think")
        if (trigger == "playerTurn"):

            this.controlsLabel.isVisible = True
            this.startButton.isVisible = True
            
        this.WINDOW.blit(this.drawSurface, (0, 0))
        pygame.display.flip()


            

            
        
    