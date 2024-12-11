Region(0,25,1280,772)

from sikuli import *

while exists("1733591833311.png"):


    if exists("1733451580826.png"):
        Settings.MoveMouseDelay = 0.01
        Settings.ActionLogs = False
        App.focus("Roblox")
        print("Requires 1280x800 Resolution")
        print("Roblox Window Detected")
        wait(1)
        click
        wait(0.5)
        hover(Location(600, 350))
        mouseDown(Button.LEFT)
        wait(0.65)
        mouseUp(Button.LEFT)
        
        # Initialize previous X-coordinate
        if exists("1733451454828.png"):
            wait(0.05)
            click("1733451461220.png")
    
            # Find the element on the screen
            
        else:
            print("Got Here")
            break

#ENTER YOUR CODE HERE
