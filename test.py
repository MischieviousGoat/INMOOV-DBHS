import cv2
import numpy as np

class ColorCoords: 
    def __init__(self, x, y, colors):
        self.x = x
        self.y = y
        self.colors = colors

cap=cv2.VideoCapture(0)

all_colors = []
all_sides = [[], [], [], [], [], []]
side = 0

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Red Bounds
redCode = (0, 0, 255)
lower_rangeR = np.array([130, 150, 210])
upper_rangeR = np.array([180, 255, 255])

# Orange Bounds
orangeCode = (10, 255, 255)
lower_rangeO = np.array([0, 0, 255])
upper_rangeO = np.array([30, 215, 255])

# Blue Bounds
blueCode = (255, 0, 0)
lower_rangeB = np.array([75, 95, 170])
upper_rangeB = np.array([105, 255, 255])

# Green Bounds
greenCode = (0, 255, 0)
lower_rangeG = np.array([55, 90, 150])
upper_rangeG = np.array([75, 255, 255])

# Yellow Bounds
yellowCode = (0, 255, 255)
lower_rangeY = np.array([20, 60, 245])
upper_rangeY = np.array([35, 175, 255])

# White Bounds
whiteCode = (255, 255, 255)
lower_rangeW = np.array([0, 0, 180])
upper_rangeW = np.array([180, 35, 255])

def recognition(frame, colorStr, colorCode, lowerBound, upperBound, all_colors): 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    _,mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    cnts,_ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        x = 600
        if cv2.contourArea(c) > x:
            x,y,w,h=cv2.boundingRect(c)
            if (SCREEN_WIDTH * (1 / 3) < x < SCREEN_WIDTH * (2 / 3)) & (SCREEN_HEIGHT * (1 / 3) < y < SCREEN_HEIGHT * (2 / 3)): 
                cv2.rectangle(frame, (x, y), (x + w, y + h), colorCode, 2)
                cv2.putText(frame, (colorStr), (x, y), cv2.FONT_HERSHEY_PLAIN,1,colorCode, 2)
                if len(all_colors) < 9: 
                    all_colors.append(ColorCoords((x + x + w) / 2, (y + y + h) / 2, colorStr))
            
def print_all_colors(all_colors):
    if len(all_colors) == 9:
        print('--------------------------------')
        for i in range(0, len(all_colors)):
            # print((all_colors[i].x, all_colors[i].y, all_colors[i].colors), end="  ")
            print((all_colors[i].colors[0]), end="  ")
            if (i + 1)% 3 == 0:
                print('\n')
        print('--------------------------------')
        
def print_all_sides(all_sides):
    print("⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄")
    for i in range(0, len(all_sides)):
        print_all_colors(all_sides[i])
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

def sort_all_colors(all_colors):
    if len(all_colors) == 9:
        for i in range(0, len(all_colors)):
            for j in range(i + 1, len(all_colors)):
                if all_colors[i].y > all_colors[j].y:
                    temp = all_colors[i]
                    all_colors[i] = all_colors[j]
                    all_colors[j] = temp

# Every time the computer updates, it will attempt to read all colors on the cube and display them on screen
while True:
    ret,frame = cap.read()
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    recognition(frame, "RED", redCode, lower_rangeR, upper_rangeR, all_colors)
    recognition(frame, "ORANGE", orangeCode, lower_rangeO, upper_rangeO, all_colors)
    recognition(frame, "BLUE", blueCode, lower_rangeB, upper_rangeB, all_colors)
    recognition(frame, "GREEN", greenCode, lower_rangeG, upper_rangeG, all_colors)
    recognition(frame, "YELLOW", yellowCode, lower_rangeY, upper_rangeY, all_colors)
    recognition(frame, "WHITE", whiteCode, lower_rangeW, upper_rangeW, all_colors)
    
    # sort_all_colors(all_colors)
    # print_all_colors(all_colors)
            
    cv2.imshow("FRAME", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("p"):
        sort_all_colors(all_colors)
        print_all_colors(all_colors)
    elif key == ord("r"):
        print("\033[2J\033[H", end="", flush=True)
        for i in range(0, len(all_colors)):
           all_sides[side].append(all_colors[i])
        if (side < 5):
            side += 1
        print_all_sides(all_sides)
    elif key == ord("c"):
        all_colors.clear()
cap.release()
cv2.destroyAllWindows()