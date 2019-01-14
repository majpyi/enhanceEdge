import numpy as np
import cv2
import p6MyMarchingSquares
import matplotlib.pyplot as plt
import modify_rgb
import modify_3rgb

# src = "blur15simpleline"
# src = "blur1041004"
src = "135069"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\tran\\"
raw = cv2.imread(inpath + src + ".jpg")
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# raw_Filter = raw
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
# raw2_Filter = raw2


noise_num = 0
th =4
np.savetxt(outpath+"3rgbraw2_Filter" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".csv", raw2_Filter, fmt="%d", delimiter=',')


np.savetxt(outpath+"0" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".csv", raw_Filter[:,:,0], fmt="%d", delimiter=',')
np.savetxt(outpath+"1" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".csv", raw_Filter[:,:,1], fmt="%d", delimiter=',')
np.savetxt(outpath+"2" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".csv", raw_Filter[:,:,2], fmt="%d", delimiter=',')
cv2.imwrite(outpath + "0" + src + "ththth" + str(th) + "noisenum" + str(noise_num) + ".jpg", raw_Filter[:,:,0])
cv2.imwrite(outpath + "1" + src + "ththth" + str(th) + "noisenum" + str(noise_num) + ".jpg", raw_Filter[:,:,1])
cv2.imwrite(outpath + "2" + src + "ththth" + str(th) + "noisenum" + str(noise_num) + ".jpg", raw_Filter[:,:,2])




a, b, guodu, d, e = modify_3rgb.noise_array(raw_Filter[:,:,0], noise_num, th)
a1, b1, guodu1, d1, e1 = modify_3rgb.noise_array(raw_Filter[:,:,1], noise_num, th)
a2, b2, guodu2, d2, e2 = modify_3rgb.noise_array(raw_Filter[:,:,2], noise_num, th)
for i in range(guodu.shape[0]):
    for j in range(guodu.shape[1]):
        if guodu[i,j]==1:
            guodu[i,j]=255
np.savetxt(outpath+"guodu" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".csv", guodu, fmt="%d", delimiter=',')
np.savetxt(outpath+"guodu" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".csv", guodu, fmt="%d", delimiter=',')
for i in range(guodu1.shape[0]):
    for j in range(guodu1.shape[1]):
        if guodu1[i,j]==1:
            guodu1[i,j]=255
np.savetxt(outpath+"guodu1" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".csv", guodu1, fmt="%d", delimiter=',')
cv2.imwrite(outpath + "guodu1" + src + "ththth" + str(th) + "noisenum" + str(noise_num) + ".jpg", guodu1)
for i in range(guodu2.shape[0]):
    for j in range(guodu2.shape[1]):
        if guodu2[i,j]==1:
            guodu2[i,j]=255
np.savetxt(outpath+"guodu2" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".csv", guodu2, fmt="%d", delimiter=',')
cv2.imwrite(outpath + "guodu2" + src + "ththth" + str(th) + "noisenum" + str(noise_num) + ".jpg", guodu2)
# for i in range(guodu.shape[0]):
#     for j in range(guodu.shape[1]):
#         if guodu[i, j] == 1:
#             guodu[i, j] = 255
# for i in range(guodu1.shape[0]):
#     for j in range(guodu1.shape[1]):
#         if guodu1[i, j] == 1:
#             guodu1[i, j] = 255
# for i in range(guodu2.shape[0]):
#     for j in range(guodu2.shape[1]):
#         if guodu2[i, j] == 1:
#             guodu2[i, j] = 255
rgb3 = np.zeros((guodu.shape[0],guodu.shape[1]))
for i in range(guodu.shape[0]):
    for j in range(guodu.shape[1]):
        if guodu[i,j]==255 or guodu1[i,j]==255 or guodu2[i,j]==255:
            rgb3[i,j]=255


# np.savetxt("D:\\guodu" + src + ".csv", guodu, fmt="%d", delimiter=',')
#
# xx_tag = [-1, -1, -1, 0, +1, +1, +1, 0]
# yy_tag = [+1, 0, -1, -1, -1, 0, +1, +1]
# re = raw2_Filter.copy()
#
# temp1 = np.zeros((raw2.shape[0], raw2.shape[1]))
# for i in range(1, raw2.shape[0] - 1):
#     for j in range(1, raw2.shape[1] - 1):
#         if guodu[i, j] == 0:
#             num = 0
#             for k in range(8):
#                 if guodu[i + xx_tag[k], j + yy_tag[k]] == 255:
#                     num += 1
#             if num > 3:
#                 temp1[i, j] = 1
#                 # guodu[i,j]=255
# for i in range(1, raw2.shape[0] - 1):
#     for j in range(1, raw2.shape[1] - 1):
#         if temp1[i, j] == 1:
#             guodu[i, j] = 255

np.savetxt(outpath+"3rgb" + src +"ththth"+str(th)+"noisenum"+str(noise_num)+".csv", rgb3, fmt="%d", delimiter=',')
cv2.imwrite(outpath + "3rgb" + src + "ththth" + str(th) + "noisenum" + str(noise_num) + ".jpg", rgb3)