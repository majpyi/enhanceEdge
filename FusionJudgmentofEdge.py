import cv2
import numpy as np

src = "blur5bodleian_000000"
src1 = "bodleian_000000"

inpath = "D:\\experiment\\pic\\q\\"
raw = cv2.imread(inpath + src1 + ".jpg")

guodu = np.loadtxt("D:\\out"+src+".csv", dtype=np.int, delimiter=",", encoding='utf-8')
for i in range (guodu.shape[0]):
    for j in range (guodu.shape[1]):
        if guodu[i,j]>=9:
            raw[i,j,:]=255
cv2.imwrite("D:\\out\\merge\\"+src+"out.jpg",raw)
