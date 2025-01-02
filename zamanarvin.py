import time
from java.lang import System
from nu.pattern import OpenCV
OpenCV.loadShared()
from sikuli import *
from org.opencv.core import Mat, Scalar, Core, CvType, Size, MatOfPoint
from org.opencv.imgcodecs import Imgcodecs
from org.opencv.imgproc import Imgproc
from java.awt.image import BufferedImage
Settings.MoveMouseDelay = 0
#How much time you want for the next shake. Ex. how much time you think will take to catch
TimeEachLoop = 5
Latency = 0.5 # this is if ur computer is very laggy, mine is so it is half a second for each shake
running = True
#COLORS FOR FISCH DETECTION (WHITE_BAR, GREY_FISH_BAR)
Sets = {
    "Color_Fish" : {"0x434b5b": 3, "0x4a4a5c": 4, "0x47515d": 4},  
    "Color_White" : {"0xFFFFFF": 15}, 
    "Color_Bar" : {"0x848587": 4, "0x787773": 4, "0x7a7873": 4}
}
isShaking = False
isCatching = False
def runHotKey(event):
    global running
    print("pressedhotkey")
    running = False
#In this case, this is CTRL+X which is if you want to stop the program (stop after any sequence, not in between)
Env.addHotkey("x",KeyModifier.CTRL,runHotKey)    
r = switchApp("Roblox")
ch = App("Roblox")
#SCALING SIZES FOR COMPATIBILITY
RobloxWindowRegion = Region(App("Roblox").focusedWindow())
ReferenceResolution = [1440,875]
UserResolution = [RobloxWindowRegion.w,RobloxWindowRegion.h]
sf = [round(1440/RobloxWindowRegion.w,4),round(900/RobloxWindowRegion.h,4)]
#REGIONS:
ReelingRegion = Region(int(404*sf[0]),int(775*sf[1]),int(613*sf[0]),int(1*sf[1]))
print("NOTE***YOUR RESOLUTION MUST BE 1440x875 FOR THIS TO WORK! IF NOT, SELECT A BIGGER RESOLUTION AND SCALE THE ROBLOX WINDOW TO 1440x900")
#DETERMINE YOUR RESOLUTION HERE:
#NOTE* FOR USERS WITH A 1440x900 RESOLUTION, 1440x875 IS JUST NO FULLSCREEN BUT FILLS ENTIRE SCREEN
#Process
def find_color(color_lower, color_upper, region): 
    screen = Screen()
    timeNow = time.time()
    try:
        captured_image = screen.capture(region)
        region_x, region_y = screen_region.getX(), screen_region.getY()
        buffered_image = captured_image.getImage()   
        height = buffered_image.getHeight() 
        width = buffered_image.getWidth()
        
        mat_image = Mat(height, width, CvType.CV_8UC3)
        raster = buffered_image.getRaster()
        for x in range(width):
            for y in range(height):
                #color = buffered_image.getRGB(x,y)
                r,g,b = raster.getPixel(x,y,None)[:3]
                data = [float(b),float(g),float(r)]
                mat_image.put(y,x,data)
        lower_bound = Scalar(color_lower[0], color_lower[1], color_lower[2])
        upper_bound = Scalar(color_upper[0], color_upper[1], color_upper[2])
        mask = Mat()
        Core.inRange(mat_image, lower_bound, upper_bound, mask)
        pts = MatOfPoint()
        Core.findNonZero(mask, pts)

        detectedlocation = []

        if pts.rows()>0:
            point = pts.toList()[0]
            x, y = float(point.x), float(point.y)   
            absolute_x = region.x + x
            absolute_y = region.y + y
            print(time.time()-timeNow)
            return int(absolute_x), int(absolute_y)
        else:
            print("No pixel of color in range!")
            print(time.time()-timeNow)
            #i have to make my own function and meanwhile ahk has this already
    except Exception as e:
        print("it did NOT work: {}".format(e))
    return 0,0
def search(target, region):
    for color_hex, variation in target.items():
        color_rgb = (
            int(color_hex[2:4], 16),  # R
            int(color_hex[4:6], 16),  # G
            int(color_hex[6:], 16)   # B
        )
        
        lower_bound = (
            max(0, color_rgb[2] - variation),
            max(0, color_rgb[1] - variation),
            max(0, color_rgb[0] - variation)
        )
        upper_bound = (
            min(255, color_rgb[2] + variation),
            min(255, color_rgb[1] + variation),
            min(255, color_rgb[0] + variation)
        )
        
        x,y = find_color(lower_bound, upper_bound, region)
        if x != 0:
            return x,y
    return 0,0

def timeToHold(pixel,scale_factor):
    data = [
        [0, 0], [16, 0], [132, 1], [217, 5], [365, 29], [450, 54], 
        [534, 91], [632, 151], [736, 234], [817, 310], [900, 382], 
        [997, 469], [1081, 541], [1164, 613], [1250, 686], 
        [1347, 711], [1448, 721], [1531, 724], [1531, 9999]
    ]
    
    for pair in data:
        pair[0] = int(pair[0] * scale_factor)
    
    lower = None
    upper = None
    for i in range(len(data)):
        if pixel < data[i][0]:
            lower = data[i - 1]
            upper = data[i]
            break

    if lower is None or upper is None:
        raise ValueError("Pixel value out of range.")

    hold = lower[1] + (pixel - lower[0]) * (upper[1] - lower[1]) / (upper[0] - lower[0])

    print("Hold: {:.2f} ms".format(hold))

    return hold
def Catch():
    i = 0
    Ranges = []
    print("Iteration",i) 
    while True:
        i += 1
        targetbarColor = Sets["Color_Fish"]
        userbarColor = Sets["Color_White"]
        target_x,target_y = search(targetbarColor, reel_area)
        bar_x,bar_y = search(userbarColor, reel_area)
        
        if target_x != 0:
            if target_x> bar_x:
                dist = target_x - bar_x
                print(dist)
                #speed = dist/0.1
                #initialspeed = dist/11
                hello = timeToHold(dist)
                mouseDown(Button.LEFT)
                wait(hello)
                mouseUp(Button.LEFT)
                print(hello)
                Ranges.append(dist)
            elif bar_x > target_x:
                pass           
            else:
                pass
        else:
            break
    return Ranges    
def Shake():
    while True:
        if exists(Pattern("shake.png").similar(0.50)):
            try:
                click(Pattern("shake.png").similar(0.50)) 
            except:            
                wait(Latency)
        else:
            print("FAILED")
            isShaking = False
            return True
            break
    return True
while(running):   
    if exists("robloxtab.png"):
        try:
            click("robloxtab.png")
        except:
            pass
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
        DetectionConsistency = Catch()
        print(DetectionConsistency)
        wait(Pattern("InventoryNum.png").similar(0.85),3600)
