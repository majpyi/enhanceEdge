import os
import numpy as np
import cv2
import change
import marchingsquares1
import marchingsquares
import marchingsquares2
import matplotlib.pyplot as plt
import MyMarchingSquares
import modify

inpath = "D:\\in\\"
outpath = "D:\\out\\"
threshold = 10  ##  change.extend_edge
threshold_march = 20

files = os.listdir(inpath)
for file in files:
    file = file[:file.index(".")]
    if (len(file) == 0):
        continue

    src = file
    raw = cv2.imread(inpath + src + ".jpg")
    # raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)

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

    # noise_num = 1
    # a, b, c, d, e = modify.noise_array(raw2, noise_num)
    # np.savetxt("D:\\noise\\noise.csv", a, fmt="%d", delimiter=',')
    #
    # raw3 = change.fix_noise(raw2, a, 1)

    rows = raw2.shape
    # np.savetxt(outpath + src + '__原图灰度图' + '.csv', raw2, fmt="%d", delimiter=',')
    # cv2.imwrite(outpath + src + "__gray" + ".jpg", raw2)

    # re = change.gradient_average_new(raw2, rows[0], rows[1], 1)
    re = change.gradient_average(raw2, rows[0], rows[1], 1)
    re[0, :] = re[rows[0] - 1, :] = re[:, 0] = re[:, rows[1] - 1] = 0
    np.savetxt(outpath + src + "__gradien" + ".csv", re, fmt="%d", delimiter=',')

    # re1 = cv2.bilateralFilter(re, 7, 50, 50)
    # np.savetxt(outpath + src + "__gradien_bil" + ".csv", re1, fmt="%d", delimiter=',')
    # re = re1

    # edge = change.extend_edge(re, threshold)
    # cv2.imwrite(outpath + src + "___" + str(threshold) + "edge_" + ".jpg", edge)
    # np.savetxt(outpath + src + "___" + str(threshold) + "edge_" + ".csv", edge, fmt="%d", delimiter=',')

    # re = change.absabs(re)
    # cv2.imwrite(outpath + src + "__abs" + ".jpg", re)
    # np.savetxt(outpath + src + "__abs__" + ".csv", re, fmt="%d", delimiter=',')
    # reabs = cv2.imread(outpath + src + "__abs" + ".jpg")
    # regray = cv2.cvtColor(reabs, cv2.COLOR_BGR2GRAY)
    # np.savetxt(outpath + src + "__regray__" + ".csv", re, fmt="%d", delimiter=',')
    # ret2, th2 = cv2.threshold(regray, 0, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # print(ret2)
    # print(type(re))
    # print(type(raw2))

    # marching_filter = change.marching_filter(re, threshold_march)
    # np.savetxt(outpath + src + "___" + str(threshold_march) + "__marching_" + ".csv", marching_filter, fmt="%d",
    #            delimiter=',')

    # change.traverse(change.marching_filter(re, threshold_march))

    # marchingsquares2.traverse(marchingsquares2.labels_matrix(re,10), "" + src)

    # print("over")
    # marching_re, vector_re = change.marching_squares(marching_filter)
    # cv2.imwrite(outpath + src + "___" + str(threshold_march) + "__marching_filter_" + ".jpg", marching_re)
    # np.savetxt(outpath + src + "___" + str(threshold_march) + "__marching_filter_" + ".csv", marching_re, fmt="%d",
    #            delimiter=',')
    # #
    # extend = change.extend_double(marching_filter, re)
    # np.savetxt(outpath + src + "___" + str(threshold_march) + "__extend_" + ".csv", extend, fmt="%d",
    #            delimiter=',')
    # change.traverse(extend)

    # extend_re, vector_extend = change.marching_squares(extend)
    # cv2.imwrite(outpath + src + "___" + str(threshold_march) + "__extend_double" + ".jpg", extend_re)
    # np.savetxt(outpath + src + "___" + str(threshold_march) + "__extend_double_" + ".csv", extend_re, fmt="%d",
    #            delimiter=',')

    # print(vector_re)
    # for x in range(0,len(vector_re), 4):
    #     plt.plot( [vector_re[x + 1], vector_re[x + 3]] ,[vector_re[x], vector_re[x + 2]],  color='black', lw=0.1)
    # print(vector_re[x])
    # print(vector_re[x+1])
    # print(vector_re[x+2])
    # print(vector_re[x+3])
    # ax = plt.gca()
    # ax.invert_yaxis()  # y轴反向
    # plt.xticks([])
    # plt.yticks([])
    # plt.axis('off')
    # plt.show()

    # x, y = MyMarchingSquares.traverse(MyMarchingSquares.labels_matrix(re, threshold_march))
    # for i in range(0, len(x), 2):
    #     plt.plot([y[i], y[i + 1]], [x[i], x[i + 1]], color='black', lw=0.1)
    # ax = plt.gca()
    # ax.invert_yaxis()  # y轴反向
    # plt.xticks([])
    # plt.yticks([])
    # plt.axis('off')
    # plt.savefig("D:\\20\\"+src+"___"+str(threshold_march), dpi=500)  # 指定分辨率保存
    # plt.show()

    x, y = MyMarchingSquares.traverse(MyMarchingSquares.labels_matrix(re, threshold_march))

    length = re.shape[0]
    width = re.shape[1]
    while length > 10 or width > 10:
        length /= 10
        width /= 10

    plt.xticks([])
    plt.yticks([])
    plt.figure(figsize=(width, length), dpi=500)
    plt.gca().invert_yaxis()  # y轴反向
    plt.axis('off')

    for i in range(0, len(x), 2):
        plt.plot([y[i], y[i + 1]], [x[i], x[i + 1]], color='white', lw=0.5)

    plt.savefig("D:\\20\\" + src + "___" + str(threshold_march), figsize=(width, length), facecolor='black',
                dpi=500)  # 指定分辨率保存
    #  plt.savefig("D:\\test", figsize=(3, 8), dpi=500)  # 指定分辨率保存
    # plt.savefig("D:\\test", dpi=500)  # 指定分辨率保存
    # plt.savefig("D:\\test", figsize=(re.shape[1]/100, re.shape[0]/100),facecolor='black', dpi=500)  # 指定分辨率保存
    plt.show()

    # ax.invert_yaxis()  # y轴反向
    # plt.xticks([])
    # plt.yticks([])
    # plt.axis('off')
    # plt.savefig("D:\\20\\" + src + "___" + str(threshold_march), figsize=(width, length), facecolor='black',
    #             dpi=500)  # 指定分辨率保存
    # plt.show()
