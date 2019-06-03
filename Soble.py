import numpy as np
import cv2
src = "blur5bodleian_000000"
inpath = "D:\\experiment\\pic\\q\\"
img = cv2.imread(inpath+src+".jpg")

x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
y = cv2.Sobel(img, cv2.CV_16S, 0, 1)

xy = cv2.Sobel(img, cv2.CV_16S, 1, 1)

absX = cv2.convertScaleAbs(x)
absY = cv2.convertScaleAbs(y)

xy = cv2.convertScaleAbs(xy)

dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

# cv2.imshow("absX", absX)
# cv2.imshow("absY", absY)
# cv2.imshow("Result", dst)
# cv2.imshow("XY", xy)
cv2.imwrite("D://out//edge//Soble___"+src+".jpg",dst)

# cv2.waitKey(0)
