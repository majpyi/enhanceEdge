import os
import numpy as np
import cv2
import change
import matplotlib.pyplot as plt

inpath = "D:\\in\\"
outpath = "D:\\out\\"
threshold = 10
threshold_march = 7

files = os.listdir(inpath)
for file in files:
    file = file[:file.index(".")]
    if (len(file) == 0):
        continue

    src = file
    raw = cv2.imread(inpath + src + ".jpg")
    raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
    cv2.imwrite(outpath + src + "__srcBil" + ".jpg", raw_Filter)
    raw = raw_Filter
    raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
    raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
    cv2.imwrite(outpath + src + "_grayBil" + ".jpg", raw2_Filter)
    np.savetxt(outpath + src + '__grayBil' + '.csv', raw2_Filter, fmt="%d", delimiter=',')
    raw2 = raw2_Filter
    # canny=cv2.Canny(raw,100,200)
    # cv2.imwrite(outpath + src + "__Canny" + ".jpg", canny)


    rows = raw2.shape
    # np.savetxt(outpath + src + '__原图灰度图' + '.csv', raw2, fmt="%d", delimiter=',')
    # cv2.imwrite(outpath + src + "__gray" + ".jpg", raw2)

    re = change.gradient_average(raw2, rows[0], rows[1])
    re[0, :] = re[rows[0] - 1, :] = re[:, 0] = re[:, rows[1] - 1] = 0
    np.savetxt(outpath + src + "__gradien" + ".csv", re, fmt="%d", delimiter=',')

    # re1 = cv2.bilateralFilter(re, 7, 50, 50)
    # np.savetxt(outpath + src + "__gradien_bil" + ".csv", re1, fmt="%d", delimiter=',')
    # re = re1

    edge = change.extend_edge(re, threshold)
    cv2.imwrite(outpath + src + "___" + str(threshold) + "edge_" + ".jpg", edge)
    np.savetxt(outpath + src + "___" + str(threshold) + "edge_" + ".csv", edge, fmt="%d", delimiter=',')

    marching_filter = change.marching_filter(re, threshold_march)
    np.savetxt(outpath + src + "___" + str(threshold_march) + "__marching_" + ".csv", marching_filter, fmt="%d",
               delimiter=',')
    marching_re, vector_re = change.marching_squares(marching_filter)
    cv2.imwrite(outpath + src + "___" + str(threshold_march) + "__marching_" + ".jpg", marching_re)
    np.savetxt(outpath + src + "___" + str(threshold_march) + "__marching_" + ".csv", marching_re, fmt="%d",
               delimiter=',')
    # # print(vector_re)
    # # for x in range(len(vector_re), 4):
    # #     plt.plot([vector_re[x], vector_re[x + 2]], [vector_re[x + 1], vector_re[x + 3]])
    # #     print(vector_re[x])
    # #     print(vector_re[x+1])
    # #     print(vector_re[x+2])
    # #     print(vector_re[x+3])
    # # plt.show()
    #
    #
    # # plt.plot([5, 10], [6, 20])
    # # plt.plot([1, 2], [3, 4])
    # # plt.show()
