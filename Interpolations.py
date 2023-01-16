import math
import numpy



#InterPolations#
#srcPoint[0] - y, srcPoint[1] - x
# Nearest Neighbor Interpolation
def NN(srcImg, srcPoint):
    NNx = int(round(srcPoint[1]))
    NNy = int(round(srcPoint[0]))
    rows, cols = srcImg.shape[:2]
    
    if (NNx < 0 or NNx > cols-1 or NNy < 0 or NNy > rows-1):
        return 0
    else:
        return srcImg[NNy, NNx]
 
 
    
#Bi-Linear Interpolation
def BiLinear_Interpolation(srcImg, srcPoint):
    x, y = srcPoint[1], srcPoint[0]
    rows, cols = srcImg.shape[:2]
    
    # 4 nearest negibors
    topL = (math.floor(y), math.floor(x))
    bottomL = (math.floor(y)+1, math.floor(x))
    topR = (math.floor(y), math.floor(x)+1)
    bottomR = (math.floor(y)+1, math.floor(x)+1)

    if (topL[1]< 0 or topL[1] > cols-1 or topL[0] < 0 or topL[0] > rows-1):
        return 0
    else:
        Alpha = x - topL[1]
        Beta = bottomL[0] - y

        Ct = (1-Alpha)*srcImg[topL]+Alpha*srcImg[topR]
        Cb = (1-Alpha)*srcImg[bottomL]+(Alpha)*srcImg[bottomR]
        Cwh = (1-Beta)*Cb + Beta*Ct
        
        return Cwh


def cEquationSolver(d, a):
    d = abs(d)
    if(0<=d and d<=1):
        return (a+2)*(d**3)-((a+3)*(d**2))+1
    elif (1<d and d<=2):
        return a*(d**3)-5*a*(d**2)+(8*a*d)-4*a
    else:
        return 0

#Cubic InterPolation
def BICubic_Interpolation(srcImg, srcPoint):
    x, y = srcPoint[1], srcPoint[0]
    dx, dy = abs(x-round(x)), abs(y-round(y))
    rows, cols = srcImg.shape[:2]
    
    
    color=0
    CaX=0
    Cay=0
    
    if (math.floor(x)-1<0 or math.floor(x)+2>cols-1 or math.floor(y)<0 or math.floor(y)>rows-1):
        return 0
    else:
        for c in range(-1,3):
            for r in range(-1,3):
                Cax = cEquationSolver(r+dx, -0.5)
                CaY = cEquationSolver(c+dy, -0.5)
                color += srcImg[round(y)+r, round(x)+c]*Cax*CaY
    
    if color>255:
        return 255
    elif color<0:
        return 0
    else:
        return color