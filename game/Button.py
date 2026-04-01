import pygame
import Constants

WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)

def checkClicked(mouseDown):

        if (mouseDown):
            if (not Button.mouseDown):
                Button.clickEvent = True
            else:
                Button.clickEvent = False
            Button.mouseDown = True
            return True
        else:
            Button.mouseDown = False
            return True
        
class Button:

    clickEvent = False
    mouseDown = False

    def __init__(this, text, x, y, width, height, fontSize = 12, font = "Helvetica", isVisible = False, textColor = BLACK, lineSpacing = 10, fillColor = GREY, borderColor = WHITE, borderRadius = 1, boxVisible = True, alignLeft = False, alignUp = False):

        this.text = text
        this.x = x
        this.y = y
        this.width = width
        this.height = height
        this.fontSize = fontSize
        this.font = font
        this.isVisible = isVisible
        this.lineSpacing = lineSpacing
        this.textColor = textColor
        this.fillColor = fillColor
        this.borderColor = borderColor
        this.borderRadius = borderRadius
        this.boxVisible = boxVisible
        this.alignLeft = alignLeft
        this.alignUp = alignUp
        this.gui = None

        this.isHoveredOn = False
        this.isDisabled = False

    
    
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

        
            
        if (this.boxVisible):

            if (this.isDisabled):
                realFillColor = (
                    
                    this.fillColor[0] * Constants.CLICK_DIMMING, 
                    this.fillColor[1] * Constants.CLICK_DIMMING, 
                    this.fillColor[2] * Constants.CLICK_DIMMING,
                ) 

            elif (this.isHoveredOn):
                if (Button.mouseDown): # Hovered on + mousedown = dim (clicked button)
                    realFillColor = (
                        
                        this.fillColor[0] * Constants.CLICK_DIMMING, 
                        this.fillColor[1] * Constants.CLICK_DIMMING, 
                        this.fillColor[2] * Constants.CLICK_DIMMING,
                    ) 
                    
                else: # Hovered on + mouseup = highlight (hovered button)

                    realFillColor = (

                        min(this.fillColor[0] * Constants.HOVER_HIGHLIGHTING, 255), 
                        min(this.fillColor[1] * Constants.HOVER_HIGHLIGHTING, 255), 
                        min(this.fillColor[2] * Constants.HOVER_HIGHLIGHTING, 255),
                    )

            else: # Otherwise, make real fill color be the regular color

                realFillColor = this.fillColor
                
                

            # Draw both rects
            pygame.draw.rect(drawSurface, this.borderColor, pygame.Rect(this.x - this.borderRadius, this.y - this.borderRadius, this.width + 2*this.borderRadius, this.height + 2*this.borderRadius), border_radius=this.borderRadius)
            pygame.draw.rect(drawSurface, realFillColor, pygame.Rect(this.x, this.y, this.width, this.height))

        font = pygame.font.SysFont(this.font, this.fontSize)

        if type(this.text) == str:
            fontSurface = font.render(this.text, True, this.textColor)
            drawSurface.blit(fontSurface, (this.x + this.width/2 - fontSurface.get_width()/2, this.y + this.height/2 - fontSurface.get_height()/2))
        elif type(this.text) == list:

            for i in range(len(this.text)):
                fontSurface = font.render(this.text[i], True, this.textColor)
                drawSurface.blit(fontSurface, (this.x + this.width/2 - fontSurface.get_width()/2, this.y + this.height/2 - fontSurface.get_height()/2 + i * (this.lineSpacing + this.fontSize) - len(this.text) * (this.lineSpacing + this.fontSize) / 2 + (this.lineSpacing + this.fontSize) / 2))

    def tick(this, mousePos):

        this.checkHover(mousePos)
        
        if (this.isHoveredOn and Button.clickEvent and this.gui != None):
            #print("CLICK EVENT") # find a way to tell the GUI has been clicked
            this.gui.eventFrom(this)
            
        #print(this.isHoveredOn)
        #print(Button.mouseDown)

            
            
        






        

