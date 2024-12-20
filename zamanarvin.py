import time
from java.lang import System 
from sikuli import *
from org.opencv.core import Mat, Scalar
from org.opencv.imgcodecs import *
from org.opencv.imgproc import *
from java.awt.image import BufferedImage
def find_color(color_lower, color_upper):
    scren = Screen()
    Nscreen = scren.capture(scren.getBounds())
    
    try:
        buffered_image = screen.getImage() 
        mat_image = Mat() # convert to gray (idk why cv2 want to be gray but ok)
        cvtColor(buffered_image, mat_image, COLOR_RGB2BGR) 
        img = imread(image_path) 
        hsv = cvtColor(img, COLOR_BGR2HSV)
        mask = inRange(hsv, Scalar(color_lower), Scalar(color_upper)) # Scalar basically BGR format writing ex.  bgr(0,0,255)
        nonzero = cv2.findNonZero(mask)
        if nonzero is not None:
            x, y = nonzero[0, 0]
            return x, y # bro really had to do 5 side quests to finally return this 
        #also ahk can do this in like one line XD

    except Exception as e:
        print("Exception at find_color {}".format(e)")
    return None
running = True
lower_bound = (88,71,64)
upper_bound = (94,77,70)
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
r = switchApp("Roblox")
ch = App("Roblox")
screen = Region(App("Roblox").focusedWindow())
#Proccess
def timeToHold(speed,distance,acceleration):
    acceleration_time = speed / acceleration
    acceleration_distance = 0.5 * acceleration * acceleration_time**2
    remaining_distance = distance - acceleration_distance
    remaining_time = remaining_distance / speed
    return remaining_time + acceleration_time
def getbarX(image):
    if exists(image):
        match = screen.find(image)
        return match.getX()
    else:
        print("Match FAILED")
        return None
def Catch():
    i = 0
    Ranges = []
    print("Iteration",i) 
    while True:
        i += 1
        print("Iteration: "+str(i))
        if exists("ArrowLeft.png"):
            userX = getbarX("ArrowLeft.png")
        elif exists("ArrowRight.png"):
            userX = getbarX("ArrowRight.png")
        else:
            print("Image Not Found : 1")
            break
        x,y = find_color()
        if current_x > userX:
            dist = current_x - userX
            print(dist)
            speed = dist/0.1
            initialspeed = dist/11
            hello = timeToHold(speed,dist,speed-initialspeed/0.1)
            mouseDown(Button.LEFT)
            wait(hello)
            mouseUp(Button.LEFT)
            print(hello)
            Ranges.append(dist)
        elif userX > current_x:
            pass           
        else:
            pass
    return Ranges    
def Shake():
    while True:
        if exists(Pattern("shake.png").similar(0.50)):
            try:
                click(Pattern("shake.png").similar(0.50)) 
            except:
                pass
            wait(Latency)
        else:
            print("FAILED")
            isShaking = False
            return True
            break
    return True

while(running):   
    if exists("robloxtab.png"):
        click("robloxtab.png")
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
