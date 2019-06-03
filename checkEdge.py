import cv2
import numpy as np

src = "L0"
# src = "296059"
src1 = "8068"
src2 = "rawe"
# src = "41004"
src = "1"

inpath = "D:\\experiment\\pic\\q\\check\\"
# inpath = "D:\\out\\canny\\"
outpath = "D:\\out\\check\\"
raw = cv2.imread(inpath + src + "1.jpg")
raw21 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw = cv2.imread(inpath + src + "2.jpg")
raw22 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
re = np.zeros((raw21.shape[0], raw21.shape[1]))

# th1 = 50
# th2 = 150
# raw21 = np.loadtxt(inpath + src1 + "__Canny th1   "+str(th1)+" th2   "+str(th2)+".csv", encoding='utf-8')
# raw22 = np.loadtxt(inpath + src2 + "__Canny th1   "+str(th1)+" th2   "+str(th2)+".csv", encoding='utf-8')


for i in range(raw21.shape[0]):
	for j in range(raw21.shape[1]):
		if raw21[i, j] > 50:
			raw21[i, j] = 255

for i in range(raw21.shape[0]):
	for j in range(raw21.shape[1]):
		if raw22[i, j] > 50:
			raw22[i, j] = 255

for i in range(raw21.shape[0]):
	for j in range(raw22.shape[1]):
		if raw21[i, j] == 255 and raw22[i, j] == 255:
			re[i, j] = 255

cv2.imwrite(outpath + "re___" + src + ".jpg", re)
