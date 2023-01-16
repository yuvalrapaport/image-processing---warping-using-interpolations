import math
import numpy
from Interpolations import BiLinear_Interpolation, NN, BICubic_Interpolation


def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
    '''
    Adapted and modifed to get the unknowns for defining a parabola:
    http://stackoverflow.com/questions/717762/how-to-calculate-the-vertex-of-a-parabola-given-three-points
    '''
    denom = (x1-x2) * (x1-x3) * (x2-x3)
    A = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom
    B = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom
    C = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1)
         * y2+x1 * x2 * (x1-x2) * y3) / denom

    return A, B, C


def calc_val(parab, x):
    return (parab[0]*(x**2))+(parab[1]*x)+(parab[2])
        
        


def calculateMedian(topL, bottomR):
    return [((topL[0]+bottomR[0])//2, topL[1]),
            ((topL[0]+bottomR[0])//2, bottomR[1])]


def deform(img, rect, delta, median):
    global parab
    p1 = median[0]
    p2 = median[1]
    # edge of parabola
    p3 = (median[0][0]+delta, (median[0][1]+median[1][1])//2)
    # calc parabola equation
    A, B, C = calc_parabola_vertex(p1[1], p1[0], p2[1], p2[0], p3[1], p3[0])
    parab = [A, B, C]

    rows, cols = img.shape[0], img.shape[1]
    newImg = numpy.zeros((rows, cols), img.dtype)
    size = rect[1][0]-median[0][0]

    for y in range(rect[0][1], rect[1][1]):
        if A < 0:
            parab_x = calc_val(parab, y)
            parab_to_median = parab_x - median[0][0]
            parab_to_rect = parab_x-rect[0][0]

            for x in range(rect[0][0], rect[1][0]):
                if x <= median[0][0]:
                    scale = (x-rect[0][0])/size
                    delta = round(parab_to_rect*scale)
                    newImg[y-rows, rect[0][0]+delta-cols] = img[y, x]

                else:
                    scale = 1-((x-median[0][0])/size)
                    delta = round((size-parab_to_median)*scale)
                    newImg[y-rows, rect[1][0]-delta-cols] = img[y, x]

        else:
            parab_x = calc_val(parab, y)
            parab_to_rect = rect[1][0] - parab_x
            parab_to_median = median[0][0] - parab_x

            for x in range(rect[0][0], rect[1][0]):
                if x <= median[0][0]:
                    scale = (x-rect[0][0])/size
                    delta = round(parab_to_rect*scale)
                    newImg[y-rows, 2*median[0][0] -
                           rect[0][0]-delta-cols] = img[y, 2*median[0][0]-x]

                else:
                    scale = 1-((x-median[0][0])/size)
                    delta = round((size-parab_to_median)*scale)
                    newImg[y-rows, 2*median[0][0] -
                           rect[1][0]+delta-cols] = img[y, 2*median[0][0]-x]

    return newImg


def inverse_trans(srcImg, destImg, rect, delta, median):
    size = rect[1][0]-median[0][0]
    rows, cols = srcImg.shape[0], srcImg.shape[1]

    NNImg = destImg.copy()
    BLImg = destImg.copy()
    CubicImg = destImg.copy()

    for x in range(cols):
        for y in range(rows):
            # if parab[0] > 0:
            parab_x = calc_val(parab, y)
            parab_to_median = parab_x - median[0][0]
            parab_to_rect = parab_x-rect[0][0]

            # check if pixel in rect
            if rect[0][0] <= x <= rect[1][0] and rect[0][1] <= y <= rect[1][1]:
                if x <= parab_x:
                    x1 = (
                        ((x-rect[0][0])/parab_to_rect)*size) + rect[0][0]
                    y1 = y
                    # interpolate
                    NNImg[y, x] = NN(srcImg, (y1, x1))
                    BLImg[y, x] = BiLinear_Interpolation(srcImg, (y1, x1))
                    CubicImg[y,x] = BICubic_Interpolation(srcImg, (y1,x1))

                else:
                    x1 = (
                        (((rect[1][0] - x)/(size - parab_to_median))-1)*size*(-1)) + median[0][0]
                    y1 = y
                    # interpolate
                    NNImg[y, x] = NN(srcImg, (y1, x1))
                    BLImg[y, x] = BiLinear_Interpolation(srcImg, (y1, x1))
                    CubicImg[y,x] = BICubic_Interpolation(srcImg, (y1,x1))

            else:
                NNImg[y, x] = srcImg[y, x]
                BLImg[y, x] = srcImg[y, x]
                CubicImg[y, x] = srcImg[y, x]

    return [NNImg, BLImg, CubicImg]