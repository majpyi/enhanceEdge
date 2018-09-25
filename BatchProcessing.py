import os
import numpy as np
import cv2
import change

inpath = "D:\\in\\"
outpath = "D:\\out\\"
threshold = 30

files = os.listdir(inpath)
for file in files:
    file = file[:file.index(".")]
    if (len(file) == 0):
        continue

    src = file
    raw = cv2.imread(inpath + src + ".jpg")
    raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    rows = raw2.shape
    np.savetxt(outpath + '原图灰度图' + src + '.csv', raw2, fmt="%d", delimiter=',')
    cv2.imwrite(outpath + "gray" + src + ".jpg", raw2)

    re = change.gradient_average(raw2, rows[0], rows[1])
    re[0, :] = re[rows[0] - 1, :] = re[:, 0] = re[:, rows[1] - 1] = 0
    np.savetxt(outpath + "gradient_" + src + ".csv", re, fmt="%d", delimiter=',')

    edge = change.extend_edge(re, threshold)
    cv2.imwrite(outpath + "edge_" + src + ".jpg", edge)
    np.savetxt(outpath + "edge_" + src + ".csv", edge, fmt="%d", delimiter=',')
