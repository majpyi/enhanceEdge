import numpy as np
import cv2
import p6MyMarchingSquares
import matplotlib.pyplot as plt
import modify_rgb
import modify

# src = "blur15simpleline"
# src = "rgbgray"
src = "blur1041004"
# src = "blurblur"
inpath = "D:\\experiment\\pic\\q\\"
# inpath = "D:\\"
outpath = "D:\\rgbtran\\"
raw = cv2.imread(inpath + src + ".jpg")
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# raw_Filter = raw
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
# raw2_Filter = raw2
cv2.imwrite("D:\\raw2" + src + ".jpg", raw2_Filter)
np.savetxt("D:\\raw2" + src + ".csv", raw2_Filter, fmt="%d", delimiter=',')

for noise_num in range(4):
    for th in range(1,7):
# noise_num = 0
# th =2
        a, b, guodu, d, e = modify_rgb.noise_array(raw2_Filter, raw_Filter,noise_num,th)
        # a, b, guodu, d, e = modify_rgb.noise_array(raw2_Filter,noise_num,th)
        # np.savetxt("D:\\guodu" + src + ".csv", guodu, fmt="%d", delimiter=',')
        for i in range(guodu.shape[0]):
            for j in range(guodu.shape[1]):
                if guodu[i, j] == 1:
                    guodu[i, j] = 255
                # else:
                #     guodu[i,j] = raw2_Filter[i,j]
        np.savetxt("D:\\guodu" + src + ".csv", guodu, fmt="%d", delimiter=',')

        xx_tag = [-1, -1, -1, 0, +1, +1, +1, 0]
        yy_tag = [+1, 0, -1, -1, -1, 0, +1, +1]
        re = raw2_Filter.copy()

        temp1 = np.zeros((raw2.shape[0], raw2.shape[1]))
        for i in range(1,raw2.shape[0]-1):
            for j in range(1,raw2.shape[1]-1):
                if guodu[i,j]==0:
                    num = 0
                    for k in range(8):
                        if guodu[i+xx_tag[k],j+yy_tag[k]]==255:
                            num+=1
                    if num>3:
                        temp1[i,j]=1
                        # guodu[i,j]=255
        for i in range(1, raw2.shape[0] - 1):
            for j in range(1, raw2.shape[1] - 1):
                if temp1[i,j]==1:
                    guodu[i,j]=255

        # temp1 = np.zeros((raw2.shape[0], raw2.shape[1]))
        # for i in range(1,raw2.shape[0]-1):
        #     for j in range(1,raw2.shape[1]-1):
        #         if guodu[i,j]==255:
        #             num = 0
        #             for k in range(8):
        #                 if guodu[i+xx_tag[k],j+yy_tag[k]]==255:
        #                     num+=1
        #             if num>3:
        #                 temp1[i,j]=1
        #                 # guodu[i,j]=255
        # for i in range(1, raw2.shape[0] - 1):
        #     for j in range(1, raw2.shape[1] - 1)
        #         if temp1[i,j]==1:
        #             guodu[i,j]=255

        # np.savetxt("D:\\trangray" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".csv", guodu, fmt="%d", delimiter=',')
        cv2.imwrite(outpath+"tranrgb" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".jpg", guodu)

# 查看过渡区域周围八邻域的像素点,查看是否有非过渡区的点,把非过渡区的点中最接近过渡区的像素点的值付给过渡区的这个像素点
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
                    # if min
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


# stop = change_tran(raw2_Filter, guodu)
# while (stop == 1):
#     stop = change_tran(raw2_Filter, guodu)
#
# # np.savetxt("D:\\raw2" + src + ".csv", raw2, fmt="%d", delimiter=',')
# np.savetxt("D:\\fix" + src + ".csv", re, fmt="%d", delimiter=',')
# # np.savetxt("D:\\guodu" + src + ".csv", guodu, fmt="%d", delimiter=',')
# cv2.imwrite("D:\\fix" + src + ".jpg", re)
