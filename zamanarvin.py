import time
running = True
barColor = (67,75,93)
Settings.MoveMouseDelay = 0
#How much time you want for the next shake. Ex. how much time you think will take to catch
TimeEachLoop = 5
Latency = 0.5 # this is if ur computer is very laggy, mine is so it is half a second for each shake
def runHotKey(event):
    global running
    print("pressedhotkey")
    running = False
#In this case, this is CTRL+X which is if you want to stop the program (stop after any sequence, not in between)
Env.addHotkey("x",KeyModifier.CTRL,runHotKey)    
isShaking = False
isCatching = False
ch = switchApp("Roblox")
screen = Region(App("Roblox").focusedWindow())
#Proccess
def Shake():
    while True:
        if exists(Pattern("1732982852570.png").similar(0.50)):
            try:
                click(Pattern("1732982852570.png").similar(0.50)) 
            except:
                pass
            wait(Latency)
        else:
            print("FAILED")
            isShaking = True
            return True
            break
    return True

while(ch.hasWindow() and running):   
    if exists("1732982595481.png"):
        click("1732982595481.png")
    else:
        print()
    mouseMove(30,100)
    mouseDown(Button.LEFT)
    wait(1)
    mouseUp(Button.LEFT)
    wait(0.5)
    isShaking = True
    hasFinishedShake = Shake()
    if hasFinishedShake == True:
        wait(0.5)
        print("User Is Catching...")
        wait(Pattern("InventoryNum.png").similar(0.85),3600)
