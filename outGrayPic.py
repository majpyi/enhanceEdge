import numpy as np
import cv2

inpath = "D:\\out\\"
outpath = "D:\\out\\"

gradient = np.loadtxt(inpath + "gray.csv", dtype=np.int, delimiter=",", encoding='utf-8')
cv2.imwrite(outpath + "outpicgray" + ".jpg", gradient)

