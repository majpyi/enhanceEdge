import os
import numpy as np
import cv2
import change
import matplotlib.pyplot as plt
from PIL import Image


# inpath = "D:\\experiment\\pic\\q\\"
# inpath = "D:\\experiment\\pic\\q\\"
inpath = "D:\\in\\canny\\"
outpath = "D:\\out\\"

files = os.listdir(inpath)
for file in files:
    file = file[:file.index(".")]
    if len(file) == 0:
        continue

    src = file
    raw = cv2.imread(inpath + src + ".jpg")
    # raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
    # cv2.imwrite(outpath + src + "__srcBil" + ".jpg", raw_Filter)
    # # raw = raw_Filter
    # raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)

    # raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)

    # raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
    # cv2.imwrite(outpath + src + "_grayBil" + ".jpg", raw2_Filter)
    # np.savetxt(outpath + src + '__grayBil' + '.csv', raw2_Filter, fmt="%d", delimiter=',')
    #
    # raw2 = raw2_Filter
    canny = cv2.Canny(raw, 10, 100)
    # canny = cv2.Canny(raw, 5, 100)
    # cv2.imwrite(outpath + src + "__Canny" + ".jpg", canny)
    cv2.imwrite("D:\\out\\" + src + "__Canny" + ".jpg", canny)
    # img = Image.open(inpath + src + ".jpg")
    # print(img.size)