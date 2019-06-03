# import transition_fixrgb
import numpy as np
from thin import Two, Xihua, array

# # for i in range(10,1,-1):
# #     print(i)

import modify_rgb_Accumulative_multiple_thresholds
import cv2

# src = "41004"
src = "8068"
# src = "blur5precise1"
# src = "blur11precise1"
# src = "blur58068"
# src = "blur8296059"
# src = "blur5bodleian_000000"
# src = "blur11ashmolean_000350"
# src = "L0"
inpath = "D:\\experiment\\pic\\q\\"
raw = cv2.imread(inpath + src + ".jpg")
raw_Filter = cv2.bilateralFilter(raw, 7, 150, 150)
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 7, 150, 150)
noise_num = 2

# for th in range(10, 2, -1):
# 	a, b, guodu, d, e = modify_rgb_Accumulative_multiple_thresholds.noise_array(raw2_Filter, raw_Filter, noise_num, th1,th2)
# 	for i in range(guodu.shape[0]):
# 		for j in range(guodu.shape[1]):
# 			if guodu[i, j] == 1:
# 				guodu[i, j] = 255
# 	si = 2
# 	kernel = np.ones((si, si), np.uint8)
# 	dilation = cv2.dilate(guodu, kernel)
# 	iTwo = Two(dilation)
# 	iThin = Xihua(iTwo, array)
#
# 	for i in range(iTwo.shape[0]):
# 		for j in range(iTwo.shape[1]):
# 			if iThin[i, j] == 0:
# 				re[i, j] += th
# 				frequency[i, j] += 1
th1 = 1
th2 = 10
a, b, guodu, d, e = modify_rgb_Accumulative_multiple_thresholds.noise_array(raw2_Filter, raw_Filter, noise_num, th1,
                                                                            th2)
for th in range(th2 - th1):
	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if guodu[i, j][th] == 1:
				guodu[i, j][th] = 255

re = np.zeros((raw2_Filter.shape[0], raw2_Filter.shape[1]))
frequency = np.zeros((raw2_Filter.shape[0], raw2_Filter.shape[1]))

for th in range(th2 - th1):
	np.savetxt("D:\\out\\try\\guodu" + str(th1 + th) + "____" + src + ".csv", guodu[:, :, th], fmt="%d", delimiter=',')

si = 2
kernel = np.ones((si, si), np.uint8)
for th in range(th2 - th1):
	dilation = cv2.dilate(guodu[:, :, th], kernel)
	iTwo = Two(dilation)
	iThin = Xihua(iTwo, array)
	np.savetxt("D:\\out\\try\\iThin" + str(th1 + th) + "____" + src + ".csv", iThin, fmt="%d", delimiter=',')
	for i in range(iTwo.shape[0]):
		for j in range(iTwo.shape[1]):
			if iThin[i, j] == 0:
				# re[i, j] += (th + 1)*(th + 1)
				re[i, j] += (th + 1)
				frequency[i, j] += 1
np.savetxt("D:\\out\\try\\re____" + src + ".csv", re, fmt="%d", delimiter=',')
np.savetxt("D:\\out\\try\\frequency____" + src + ".csv", frequency, fmt="%d", delimiter=',')

merge = np.zeros((raw2_Filter.shape[0], raw2_Filter.shape[1]))
for i in range(re.shape[0]):
	for j in range(re.shape[1]):
		merge[i, j] = re[i, j] * 5 + frequency[i, j] * 10
cv2.imwrite("D:\\out\\try\\show____" + src + "out.jpg", merge)
np.savetxt("D:\\out\\try\\merge____" + src + ".csv", merge, fmt="%d", delimiter=',')

xx = [-1, -1, -1, 0, +1, +1, +1, 0, -1]
yy = [+1, 0, -1, -1, -1, 0, +1, +1, +1]
re = np.zeros((re.shape[0], re.shape[1]))

for i in range(1, re.shape[0] - 1):
	for j in range(1, re.shape[1] - 1):
		if re[i, j] == 255:
			count_0 = 0
			for k in range(len(xx)):
				if re[i + xx[k], j + yy[k]] == 0:
					count_0 += 1
			if count_0 == 7:
				re[i, j] = 255  # 延伸点
cv2.imwrite("D:\\re.jpg", re)
