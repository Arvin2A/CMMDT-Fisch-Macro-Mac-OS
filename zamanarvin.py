import time
from java.lang import System
from nu.pattern import OpenCV
OpenCV.loadShared()
from sikuli import *
from org.opencv.core import Mat, Scalar, Core, CvType, Size, MatOfPoint
from org.opencv.imgcodecs import Imgcodecs
from org.opencv.imgproc import Imgproc
from java.awt.image import BufferedImage
def find_color(color_lower, color_upper):
    scren = Screen()
    Nscreen = scren.capture(scren.getBounds())
    
    try:
        buffered_image = scren.getImage().get()     
        height = buffered_image.getHeight() 
        width = buffered_image.getWidth()
        #print(CvType.CV_8UC3)
        mat_image = Mat(height, width, CvType.CV_8UC3)
        #imgpixels = buffered_image.getRGB(0,0, float(width), float(height), None, 0, float(width))
        #mat_image.put(0,0,imgpixels)
        for x in range(width):
            for y in range(height):
                color = buffered_image.getRGB(x,y)
                b = (color >> 16) & 0xFF  
                g = (color >> 8) & 0xFF  
                r = color & 0xFF
                data = [float(b),float(g),float(r)]
                #print(data)
                mat_image.put(y,x,data)
        lower_bound = Scalar(color_lower[0], color_lower[1], color_lower[2]) #Color range
        upper_bound = Scalar(color_upper[0], color_upper[1], color_upper[2])#Color range
        mask = Mat()
        Core.inRange(mat_image, lower_bound, upper_bound, mask)
        pts = MatOfPoint()
        Core.findNonZero(mask, pts)

        detectedlocation = []

        if pts.rows()>0:
            point = pts.toList()[0]
            x, y = point.x, point,y
            return x, y # bro really had to do 5 side quests to finally return this 
        #also ahk can do this in like one line XD

    except Exception as e:
        print("it did NOT work: {}".format(e))
    return None,None
running = True
lower_bound = (88,71,64)
upper_bound = (94,77,70)
color_position = find_color(lower_bound, upper_bound)
print(color_position)
exit()
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
        color_position = find_color(lower_bound, upper_bound)
        if color_position is None:
            print("Color not found!")
            break
        else:
            current_x,y = color_position
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
