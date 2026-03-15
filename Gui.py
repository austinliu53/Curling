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
        #Initialize game manager
        this.gameManager = GameManager.GameManager()
        
        #Clock
        this.clock = pygame.time.Clock()

        #Array of all our button

        this.buttons = []

        #Welcome
        this.welcomeLabel = Button.Button("Curling Simulator!", 100, 200, 400, 100, isVisible=True, fontSize=20, boxVisible=False)
        this.buttons.append(this.welcomeLabel)

        this.welcomeButton = Button.Button("Start curling!", 100, 300, 400, 100, 18, isVisible=True)
        this.welcomeButton.addEventListener(this)
        this.buttons.append(this.welcomeButton)
        

        #Start curling 
        
        this.startButton = Button.Button("Press this button to launch your stone in a direction.", 100, 100, 400, 100, isVisible=False, fontSize=15)
        this.startButton.addEventListener(this)
        this.buttons.append(this.startButton)

    def gameLoop(this):

        running = True
        while running: 

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
            this.drawSurface.fill(GREY)
            this.clock.tick(Constants.FPS)

    def eventFrom(this, button):
        
        if (button == this.welcomeButton):

            this.gameManager.gameMode = GameManager.PRE_DELIVERY
            this.welcomeLabel.isVisible = False
            this.welcomeButton.isVisible = False
            this.startButton.isVisible = True
            print("HELLO")

        if (button == this.startButton):
            this.gameManager.plane.start() 
            this.gameManager.gameMode = GameManager.SWEEPING

            this.startButton.isVisible = False
            




            #this.plane.addStone(30, 150, 430, 2, 0, RED)
    
            #this.plane.addStone(30, 250, 400, 0, 0, YELLOW)
            #this.plane.addStone(30, 250, 460, 0, 0, YELLOW)
            

            #this.plane.addStone(30, 400, 375, 0, 0, YELLOW)
            #this.plane.addStone(30, 400, 490, 0, 0, YELLOW)

            



            

            
        
    