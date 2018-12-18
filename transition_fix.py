import numpy as np
import cv2
import p6MyMarchingSquares
import matplotlib.pyplot as plt
import modify

src = "41004"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\"
raw = cv2.imread(inpath + src + ".jpg")
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
# raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
raw_Filter = raw
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
# raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
raw2_Filter = raw2

np.savetxt("D:\\raw2" + src + ".csv", raw2, fmt="%d", delimiter=',')



noise_num = 1
a, b, guodu, d, e = modify.noise_array(raw2_Filter, noise_num)
np.savetxt("D:\\tag_guodu" + src + ".csv", guodu, fmt="%d", delimiter=',')
for i in range(guodu.shape[0]):
    for j in range(guodu.shape[1]):
        if guodu[i, j] == 1:
            guodu[i, j] = 255
        # else:
        #     guodu[i,j] = raw2_Filter[i,j]
np.savetxt("D:\\cs_guodu" + src + ".csv", guodu, fmt="%d", delimiter=',')
cv2.imwrite("D:\\tran" + src + ".jpg", guodu)

xx_tag = [-1, -1, -1, 0, +1, +1, +1, 0]
yy_tag = [+1, 0, -1, -1, -1, 0, +1, +1]
re = raw2_Filter.copy()


def change_tran(raw2, guodu):
    tag = 0
    temp = np.zeros((raw2.shape[0], raw2.shape[1]))
    for i in range(2, raw2.shape[0] - 2):
        for j in range(2, raw2.shape[1] - 2):
            choose_near = []
            if guodu[i, j] == 255:
                tag = 1
                for k in range(len(xx_tag)):
                    if guodu[i + xx_tag[k], j + yy_tag[k]] != 255:
                        # re[i,j] = re[i+xx_tag[k],j+yy_tag[k]]
                        choose_near.append(re[i + xx_tag[k], j + yy_tag[k]])
                        temp[i, j] = -1
                if len(choose_near)>0:
                    min = abs(int(choose_near[0]) - int(re[i, j]))
                    re[i,j] = choose_near[0]

                    for m in range(1, len(choose_near)):
                        diff = abs(int(choose_near[m]) - int(re[i, j]))
                        if diff < min:
                            re[i, j] = choose_near[m]
                            min = diff
    print(1)
    for i in range(2, raw2.shape[0] - 2):
        for j in range(2, raw2.shape[1] - 2):
            if temp[i, j] == -1:
                guodu[i, j] = 0
    return tag


stop = change_tran(raw2_Filter, guodu)
while (stop == 1):
    stop = change_tran(raw2_Filter, guodu)

np.savetxt("D:\\raw2" + src + ".csv", raw2, fmt="%d", delimiter=',')
np.savetxt("D:\\re" + src + ".csv", re, fmt="%d", delimiter=',')
np.savetxt("D:\\guodu" + src + ".csv", guodu, fmt="%d", delimiter=',')
