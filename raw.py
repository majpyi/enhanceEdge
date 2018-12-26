import numpy as np
import cv2
import p6MyMarchingSquares
import matplotlib.pyplot as plt
import modify

src = "circle"
# src = "blurblur"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\"
raw = cv2.imread(inpath + src + ".jpg")
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# raw_Filter = raw
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
# raw2_Filter = raw2

cv2.imwrite("D:\\raw2" + src + ".jpg", raw2_Filter)
np.savetxt("D:\\raw2" + src + ".csv", raw2_Filter, fmt="%d", delimiter=',')