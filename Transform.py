from Methods import calculateMedian, deform, inverse_trans
import cv2
import sys

# suppose to keep tupple of starting coordinate to rectangle
global refPt
refPt = []

# callback for left mouse click event
def clickEvent(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))


# loading Picture

imgPath = sys.argv[1]
img = cv2.imread(imgPath, 0)
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
cv2.imshow('Image', img)

cv2.setMouseCallback('Image', clickEvent)
cv2.waitKey(0)
cv2.destroyAllWindows()

#clicked by user rectangle pixels
topL = refPt[0]
bottomR = refPt[1]

#median - keeps points to middle line inside rectangle
#median[0] - upper point, median[1] -bottom point
median = calculateMedian(topL, bottomR)

# draw Lines
drawedImg = img.copy()
drawedImg = cv2.rectangle(drawedImg, topL, bottomR, 255, 5)
drawedImg = cv2.line(drawedImg, median[0], median[1], 255, 5)
cv2.imshow('Image', drawedImg)
cv2.setMouseCallback('Image', clickEvent)
cv2.waitKey(0)
cv2.destroyAllWindows()

userChoice = []
parabEdge = refPt[2]


userChoice.append(parabEdge[0]-median[0][0])



if userChoice[0] > 0:
    # 180 right parabola
    userChoice.append(180)
else:
    # 0 left parabola
    userChoice.append(0)


center = (median[0][0], (median[0][1]+median[1][1])//2)
axes = (abs(int(userChoice[0])), (center[1]-median[0][1]))
cv2.ellipse(drawedImg, center, axes, userChoice[1], 270, 90, 255, 5)
cv2.imshow('angle', drawedImg)
cv2.waitKey(0)
cv2.destroyAllWindows()




#print('now for the main event: ')
deformedImg = deform(img, [topL, bottomR], userChoice[0], median)

after_inverse_img = inverse_trans(
    img, deformedImg, [topL, bottomR], userChoice[0], median)

NNImg, BLImg, CubicImg = after_inverse_img[:3]

cv2.imwrite('Nearest Neighbor Interpolation Image.jpg', NNImg)
cv2.imwrite('Bi-Linear Interpolation Image.jpg', BLImg)
cv2.imwrite('Bicubic Interpolation Image.jpg', CubicImg)

cv2.imshow('Nearest Neighbor Interpolation Image.jpg', NNImg)
cv2.imshow('Bi-Linear Interpolation Image.jpg', BLImg)
cv2.imshow('Bicubic Interpolation Image.jpg', CubicImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
