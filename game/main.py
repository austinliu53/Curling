import Gui
import Constants
import asyncio

def main():

    gui = Gui.Gui(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
    asyncio.run(gui.gameLoop())
    
main() 