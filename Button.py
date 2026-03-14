import pygame
import Constants

WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)

class Button:

    clickEvent = False
    mouseDown = False

    def __init__(this, text, x, y, width, height, fontSize = 12, font = "Helvetica", isVisible = False, textColor = BLACK, fillColor = GREY, borderColor = WHITE, borderRadius = 1, opacity = 1, alignLeft = False, alignUp = False):

        this.text = text
        this.x = x
        this.y = y
        this.width = width
        this.height = height
        this.fontSize = fontSize
        this.font = font
        this.isVisible = isVisible
        this.textColor = textColor
        this.fillColor = fillColor
        this.borderColor = borderColor
        this.borderRadius = borderRadius
        this.opacity = opacity
        this.alignLeft = alignLeft
        this.alignUp = alignUp
        this.gui = None

        this.isHoveredOn = False

    def checkClicked(this, mouseDown):

        if (mouseDown):
            if (not Button.mouseDown):
                Button.clickEvent = True
                #print("MOUSE EVENT!!")
            else:
                Button.clickEvent = False
            Button.mouseDown = True
            return True
        else:
            Button.mouseDown = False
            return True
    
    def addEventListener(this, gui):
        this.gui = gui

    def checkHover(this, mousePos):

        this.isHoveredOn = (
                (mousePos[0] >= this.x) and 
                (mousePos[0] <= this.x + this.width) 
                and
                (mousePos[1] >= this.y) and 
                (mousePos[1] <= this.y + this.height)
            )
        
    def draw(this, drawSurface):

        if (this.isHoveredOn):
            
            if (Button.mouseDown):
                realFillColor = (
                    
                    this.fillColor[0] * Constants.CLICK_DIMMING, 
                    this.fillColor[1] * Constants.CLICK_DIMMING, 
                    this.fillColor[2] * Constants.CLICK_DIMMING
                ) 
                
            else:
                realFillColor = (

                    min(this.fillColor[0] * Constants.HOVER_HIGHLIGHTING, 255), 
                    min(this.fillColor[1] * Constants.HOVER_HIGHLIGHTING, 255), 
                    min(this.fillColor[2] * Constants.HOVER_HIGHLIGHTING, 255)
                )

        else:
            realFillColor = this.fillColor
        
        pygame.draw.rect(drawSurface, this.borderColor, pygame.Rect(this.x - this.borderRadius, this.y - this.borderRadius, this.width + 2*this.borderRadius, this.height + 2*this.borderRadius), border_radius=this.borderRadius)
        pygame.draw.rect(drawSurface, realFillColor, pygame.Rect(this.x, this.y, this.width, this.height))
        font = pygame.font.SysFont(this.font, this.fontSize)
        surface = font.render(this.text, True, this.textColor)

        drawSurface.blit(surface, (this.x + this.width/2 - surface.get_width()/2, this.y + this.height/2 - surface.get_height()/2)) 
        
    def tick(this, mousePos, mouseDown):

        this.checkHover(mousePos)
        this.checkClicked(mouseDown)
        
        if (this.isHoveredOn and Button.clickEvent and this.gui != None):
            print("CLICK EVENT") # find a way to tell the GUI has been clicked
            this.gui.eventFrom(this)
            
        #print(this.isHoveredOn)
        #print(Button.mouseDown)

            
            
        






        

