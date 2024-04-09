import cv2
import numpy as np

class ColorCoords: 
    def __init__(self, x, y, colors):
        self.x = x
        self.y = y
        self.colors = colors

cap=cv2.VideoCapture(0)

all_colors = []
sorted_colors = []

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Red Bounds
redCode = (0, 0, 255)
lower_rangeR = np.array([0, 95, 255])
upper_rangeR = np.array([10, 165, 255])

# Orange Bounds
orangeCode = (10, 255, 255)
lower_rangeO = np.array([15, 0, 255])
upper_rangeO = np.array([30, 215, 255])

# Blue Bounds
blueCode = (255, 0, 0)
lower_rangeB = np.array([90, 90, 180])
upper_rangeB = np.array([105, 250, 255])

# Green Bounds
greenCode = (0, 255, 0)
lower_rangeG = np.array([55, 85, 140])
upper_rangeG = np.array([75, 160, 255])

# Yellow Bounds
yellowCode = (0, 255, 255)
lower_rangeY = np.array([25, 40, 245])
upper_rangeY = np.array([40, 115, 255])

# White Bounds
whiteCode = (255, 255, 255)
lower_rangeW = np.array([0, 0, 180])
upper_rangeW = np.array([180, 35, 255])

def recognition(frame, colorStr, colorCode, lowerBound, upperBound): 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    _,mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    cnts,_ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        x = 600
        if cv2.contourArea(c) > x:
            x,y,w,h=cv2.boundingRect(c)
            if (SCREEN_WIDTH * (1 / 4) < x < SCREEN_WIDTH * (3 / 4)) & (SCREEN_HEIGHT * (1 / 4) < y < SCREEN_HEIGHT * (3 / 4)): 
                cv2.rectangle(frame, (x, y), (x + w, y + h), colorCode, 2)
                cv2.putText(frame, (colorStr), (x, y), cv2.FONT_HERSHEY_PLAIN,1,colorCode, 2)
                if len(all_colors) < 9: 
                    all_colors.append(ColorCoords((x + x + w) / 2, (y + y + h) / 2, colorStr))
            
def print_all_colors(all_colors):
    if len(all_colors) == 9:
        for i in range(0, len(all_colors)):
            print((all_colors[i].x, all_colors[i].y, all_colors[i].colors[0]), end="  ")
            # print((all_colors[i].colors[0]), end="  ")
            if (i + 1)% 3 == 0:
                print('\n')
        print(len(all_colors))
    all_colors.clear()

def sort_all_colors(all_colors):
    if len(all_colors) == 9:
        for i in range(0, len(all_colors)):
            for j in range(i + 1, len(all_colors)):
                if all_colors[i].y > all_colors[j].y:
                    temp = all_colors[i]
                    all_colors[i] = all_colors[j]
                    all_colors[j] = temp
            sorted_colors.append(all_colors[i])

# Every time the computer updates, it will attempt to read all colors on the cube and display them on screen
while True:
    ret,frame = cap.read()
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    recognition(frame, "RED", redCode, lower_rangeR, upper_rangeR)
    recognition(frame, "ORANGE", orangeCode, lower_rangeO, upper_rangeO)
    recognition(frame, "BLUE", blueCode, lower_rangeB, upper_rangeB)
    recognition(frame, "GREEN", greenCode, lower_rangeG, upper_rangeG)
    recognition(frame, "YELLOW", yellowCode, lower_rangeY, upper_rangeY)
    recognition(frame, "WHITE", whiteCode, lower_rangeW, upper_rangeW)
    
    sort_all_colors(all_colors)
    # print_all_colors(all_colors)
            
    cv2.imshow("FRAME", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("p"):
        print_all_colors(all_colors)
cap.release()
cv2.destroyAllWindows()

"""
(499.0, 250.5, 'O')  (518.5, 302.5, 'O')  (541.0, 354.0, 'B')  

(568.0, 236.5, 'Y')  (590.0, 289.0, 'W')  (615.5, 341.5, 'R')

(634.5, 227.5, 'B')  (661.0, 274.5, 'O')  (679.5, 325.5, 'W')

9
(493.0, 377.0, 'O')  (511.0, 431.0, 'O')  (534.0, 484.0, 'B')  

(564.0, 361.5, 'Y')  (586.0, 418.0, 'W')  (609.5, 473.0, 'R')

(637.0, 352.0, 'B')  (658.5, 402.0, 'O')  (676.5, 456.0, 'W')

9

rotated 90deg clockwise
"""