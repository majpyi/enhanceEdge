import cv2
import numpy as np
from numpy.core.multiarray import ndarray

inpath = "C:\\Users\\M\\Documents\\MATLAB\\"
outpath = "C:\\Users\\M\\Documents\\MATLAB\\"
# src = "ceshi"
# raw = cv2.imread(inpath + src + ".jpg")
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
# for i in range(raw2.shape[0]):
# 	for j in range(raw2.shape[1]):
# 		if raw2[i,j] >= 100:
# 			raw2[i,j] = 100
# 		else:
# 			raw2[i,j] = 50
# cv2.imwrite(outpath + src + "change" + ".jpg", raw2)
re2 = np.loadtxt(outpath + "csv2" + ".csv", dtype=np.int32, delimiter=",", encoding='utf-8')
re1 = np.loadtxt(outpath + "csv1" + ".csv", dtype=np.int32, delimiter=",", encoding='utf-8')
re = re2 - re1
print(re)
# np.savetxt(outpath + "re.csv", re, fmt="%d", delimiter=',')
np.savetxt(outpath + "re.csv", re ,fmt='%d', delimiter=',')
