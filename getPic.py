import change
import numpy as np
import MyMarchingSquares
import matplotlib.pyplot as plt
import cv2
import modify

inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\"
src = "296059"

raw = cv2.imread(inpath + src + ".jpg")
raw1 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
print(raw1.shape[0])
print(raw1.shape[1])
np.savetxt(outpath + src + ".csv", raw1, fmt="%d", delimiter=',')

# raw = cv2.bilateralFilter(raw, 7, 50, 50)

# raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
cv2.imwrite(outpath + src + ".jpg", raw1)
