# encoding:utf-8

#
# laplacian边缘检测
#

import numpy
import cv2

src = "raw2_Filter___16068"
inpath = "D:\\experiment\\pic\\q\\"
img = cv2.imread(inpath + src + ".jpg")
raw2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# raw2 = cv2.GaussianBlur(img, (5, 5), 0)
#
# # gray_lap = cv2.Laplacian(imgGau, cv2.CV_16S, ksize=3)
# gray_lap = cv2.Laplacian(img, cv2.CV_16S, ksize=3)
# # dst = cv2.convertScaleAbs(gray_lap)
#
# # bond = numpy.hstack((img, dst))
#
# # cv2.imshow("bond", bond)
# cv2.imwrite("D://laplacian___"+src+".jpg",gray_lap)

# cv2.waitKey(0)

xxx = [-1, 0, 0, 1]
yyy = [0, 1, -1, 0]
# xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
# yyy = [+1, 0, -1, -1, -1, 0, +1, +1]


re = raw2.copy()
for i in range(1,raw2.shape[0]-1):
	for j in range(1,raw2.shape[1]-1):
		# re[i, j] = 9 * raw2[i, j]
		re[i, j] = 5 * raw2[i, j]
		for k in range(len(xxx)):
			re[i, j] = int(re[i, j]) - int(raw2[i + xxx[k], j + yyy[k]])
# cv2.imwrite("D://re___9"+src+".jpg",re)
cv2.imwrite("D://re___5"+src+".jpg",re)

import cv2 as cv
import numpy as np

# rgb = cv.imread(inpath + src + ".jpg")
