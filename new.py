import numpy as np
import modify_rgb_Accumulative_multiple_thresholds
import cv2
from thin import Two, Xihua, array
import modify_rgb

#
# # image = np.loadtxt("D:\\out\\tranrgb\\" + src + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')
#

#
# src = "L0"
# inpath = "D:\\experiment\\pic\\q\\"
# raw = cv2.imread(inpath + src + ".jpg")
# raw_Filter = cv2.bilateralFilter(raw, 7, 150, 150)
# raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
# raw2_Filter = cv2.bilateralFilter(raw2, 7, 150, 150)
# noise_num = 2
#
# # th1 = 1
# # th2 = 5
# # a, b, guodu, d, e = modify_rgb_Accumulative_multiple_thresholds.noise_array(raw2_Filter, raw_Filter, noise_num, th1,
# #                                                                             th2)
#
#
# # np.savetxt("D:\\out\\try\\re____" + src + ".csv", re, fmt="%d", delimiter=',')
# # np.savetxt("D:\\out\\try\\frequency____" + src + ".csv", frequency, fmt="%d", delimiter=',')
# re = np.loadtxt("D:\\out\\try\\re____" + src + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')
# frequency = np.loadtxt("D:\\out\\try\\frequency____" + src + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')
#
# merge = np.zeros((raw2_Filter.shape[0], raw2_Filter.shape[1]))
# for i in range(re.shape[0]):
# 	for j in range(re.shape[1]):
# 		merge[i, j] = re[i, j] * 5 + frequency[i, j] * 5
#
# xx = [-1, -1, -1, 0, +1, +1, +1, 0, -1]
# yy = [+1, 0, -1, -1, -1, 0, +1, +1, +1]
#
# point = np.zeros((raw2_Filter.shape[0], raw2_Filter.shape[1]))
# for i in range(1, re.shape[0] - 1):
# 	for j in range(1, re.shape[1] - 1):
# 		if merge[i, j] > 200:
# 			count_0 = 0
# 			for k in range(len(xx)):
# 				if merge[i + xx[k], j + yy[k]] == 0:
# 					count_0 += 1
# 			if count_0 == 7:
# 				point[i, j] = 255  # 延伸点
# 			else:
# 				point[i, j] = 100
# cv2.imwrite("D:\\re.jpg", point)


src = "L0"
# src = "41004"
# src = "8068"
# src = "216053"
# src = "rock2"
# src = "flower"
# src = "basketball"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\try\\"+src+"\\"
raw = cv2.imread(inpath + src + ".jpg")
raw_Filter = cv2.bilateralFilter(raw, 9, 150, 150)
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 9, 150, 150)


th1 = 1
th2 = 10
noise_num = 2
a, b, guodu, d, e = modify_rgb_Accumulative_multiple_thresholds.noise_array(raw2_Filter, raw_Filter, noise_num, th1,
                                                                            th2)
for th in range(th2 - th1):
	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if guodu[i, j][th] == 1:
				guodu[i, j][th] = 255

for th in range(th2 - th1):
	np.savetxt(outpath+"guodu" + str(th1 + th) + "____" + src + ".csv", guodu[:, :, th], fmt="%d", delimiter=',')

#
# print(raw2)
# print(type(raw2))
#
# guodu1 = np.loadtxt("D:\\out\\try\\guodu9____L0.csv", dtype=np.uint8, delimiter=",", encoding='utf-8')
#
# # noise_num = 2
# # th = 10
# # a, b, guodu1, d, e = modify_rgb.noise_array(raw2_Filter, raw_Filter, noise_num, th)
#
# print(guodu1)
# print(type(guodu1))
#
# si = 2
# kernel = np.ones((si, si), np.uint8)
#
# dilation = cv2.dilate(guodu1, kernel)
# iTwo = Two(dilation)
# iThin = Xihua(iTwo, array)
# cv2.imwrite("D:\\re1.jpg", iThin)
# np.savetxt("D:\\out\\try\\iThin--re1" + "____" + src + ".csv", iThin, fmt="%d", delimiter=',')
#
# # for i in range(iThin.shape[0]):
# # 	for j in range(iThin.shape[1]):
# # 		if iThin[i, j] == 0:
# # 			iThin[i, j] = 255
# # 		else:
# # 			iThin[i, j] = 0
#
# # iTwo = Two(dilation)
# # iThin = Xihua(iTwo, array)
# # cv2.imwrite("D:\\re2.jpg", iThin)
# # np.savetxt("D:\\out\\try\\iThin--re2" + "____" + src + ".csv", iThin, fmt="%d", delimiter=',')
# xx = [-1, -1, -1, 0, +1, +1, +1, 0]
# yy = [+1, 0, -1, -1, -1, 0, +1, +1]
#
# # guodu1 = np.loadtxt("D:\\out\\try\\guodu2____L0.csv", dtype=np.uint8, delimiter=",", encoding='utf-8')
#
# point = np.zeros((raw2_Filter.shape[0], raw2_Filter.shape[1]))
# for i in range(1, point.shape[0] - 1):
# 	for j in range(1, point.shape[1] - 1):
# 		if iThin[i, j] == 0:
# 			count_0 = 0
# 			for k in range(len(xx)):
# 				if iThin[i + xx[k], j + yy[k]] == 255:
# 					count_0 += 1
# 			if count_0 == 7:
# 				point[i, j] = 0  # 延伸点
# 			else:
# 				point[i, j] = 255
# 		else:
# 			point[i, j] = 100
#
# cv2.imwrite("D:\\point.jpg", point)
#
#
# guodu1 = np.loadtxt("D:\\out\\try\\guodu9____L0.csv", dtype=np.uint8, delimiter=",", encoding='utf-8')
# guodu2 = np.loadtxt("D:\\out\\try\\guodu4____L0.csv", dtype=np.uint8, delimiter=",", encoding='utf-8')


# cv2.imwrite("D:\\guodu1.jpg", guodu1)
# cv2.imwrite("D:\\guodu2.jpg", guodu2)

xx = [-1, -1, -1, 0, +1, +1, +1, 0]
yy = [+1, 0, -1, -1, -1, 0, +1, +1]


def union(guodu1, guodu2):
	tag = 0
	while (tag == 0):
		for i in range(guodu1.shape[0]):
			for j in range(guodu1.shape[1]):
				tag = 1
				if guodu1[i, j] == 0 and guodu2[i, j] == 255:
					for k in range(8):
						n = i + xx[k]
						m = j + yy[k]
						if n >= 0 and n < guodu1.shape[0] and m >= 0 and m < guodu1.shape[1] and guodu1[
							i + xx[k], j + yy[k]] == 255:
							tag = 0
							guodu1[i, j] = 255


# union(guodu1,guodu2)
# cv2.imwrite("D:\\merge.jpg", guodu1)

si = 2
kernel = np.ones((si, si), np.uint8)
re = np.loadtxt(outpath+"guodu9____" + src + ".csv", dtype=np.uint8, delimiter=",", encoding='utf-8')
re = cv2.dilate(re, kernel)

for th in range(th2-1, th1, -1):
	# guodu1 = np.loadtxt("D:\\out\\try\\guodu9____L0.csv", dtype=np.uint8, delimiter=",", encoding='utf-8')
	guodu2 = np.loadtxt(outpath+"guodu" + str(th) + "____" + src + ".csv", dtype=np.uint8, delimiter=",",
	                    encoding='utf-8')
	guodu2 = cv2.dilate(guodu2, kernel)
	union(re, guodu2)
	cv2.imwrite(outpath+"merge" + str(th) + "____" + src + ".jpg", re)
	np.savetxt(outpath+"merge____" + str(th) + src + ".csv", re, fmt="%d", delimiter=',')
	cv2.imwrite(outpath+"guodu" + str(th) + "____" + src + ".jpg", guodu2)

# cv2.imwrite("D:\\merge.jpg", re)

np.savetxt(outpath+"merge" + "____" + src + ".csv", re, fmt="%d", delimiter=',')
re = np.loadtxt(outpath+"merge" + "____" + src + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')

# iTwo = Two(re)
# iThin = Xihua(iTwo, array)
# cv2.imwrite("D:\\xihua.jpg", iThin)
