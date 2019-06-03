import cv2
import numpy as np
import modify4y2r
import Mymodify
import os

inpath = "D:\\experiment\\pic\\batch\\"
outpath = "D:\\out\\try\\batch\\"

# files = os.listdir(inpath)
# for file in files:
# 	if not file.endswith(".jpg"):
# 		continue


# 0蓝  2 红 1 绿
# th1 = 150
# th2 = 200
# # 读取原始图像
# src = "square"
# raw = cv2.imread(inpath + src + ".jpg")
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
# canny = cv2.Canny(raw2, th1, th2)
# re = np.zeros((canny.shape[0], canny.shape[1], 3))
# for i in range(canny.shape[0]):
# 	for j in range(canny.shape[1]):
# 		if canny[i, j] == 255:
# 			re[i, j, 2] = 255
# # cv2.imwrite(outpath + src + "原始canny" + ".jpg", re)
# cv2.imencode('.jpg', re)[1].tofile(outpath + src + "原始canny" + ".jpg")
#
# #########################################################################################
#
#
# # 读取处理结果
# re1 = np.loadtxt(outpath + src + "  tagre.csv", dtype=np.int, delimiter=",", encoding='utf-8')
# re = np.zeros((canny.shape[0], canny.shape[1], 3))
# for i in range(canny.shape[0]):
# 	for j in range(canny.shape[1]):
# 		if re1[i, j] == 1 or re1[i, j] == 2:
# 			re[i, j, 0] = 255
# # cv2.imwrite(outpath + src + "原始我们的大小边" + ".jpg", re)
# cv2.imencode('.jpg', re)[1].tofile(outpath + src + "原始我们的大小边" + ".jpg")
#
# #########################################################################################
#
# # 原始融合
# src = "square"
# raw = cv2.imread(inpath + src + ".jpg")
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
# canny = cv2.Canny(raw2, th1, th2)
# re = np.zeros((canny.shape[0], canny.shape[1], 3))
# for i in range(canny.shape[0]):
# 	for j in range(canny.shape[1]):
# 		if canny[i, j] == 255:
# 			re[i, j, 2] = 255
# # 读取处理结果
# re1 = np.loadtxt(outpath + src + "  tagre.csv", dtype=np.int, delimiter=",", encoding='utf-8')
# for i in range(canny.shape[0]):
# 	for j in range(canny.shape[1]):
# 		if re1[i, j] == 1 or re1[i, j] == 2:
# 			re[i, j, 0] = 255
# # cv2.imwrite(outpath + src + "原始融合" + ".jpg", re)
# cv2.imencode('.jpg', re)[1].tofile(outpath + src + "原始融合" + ".jpg")
#
# #########################################################################################
# #########################################################################################


th1 = 150
th2 = 200
# th1 = 100
# th2 = 150
# th1 = 50
# th2 = 150
src = "blur"
# 读取原始模糊图像
raw = cv2.imread(inpath + src + ".jpg")
canny = cv2.Canny(raw, th1, th2)
re = np.zeros((canny.shape[0], canny.shape[1], 3))
for i in range(canny.shape[0]):
	for j in range(canny.shape[1]):
		if canny[i, j] == 255:
			re[i, j, 2] = 255
cv2.imencode('.jpg', re)[1].tofile(outpath + src + "模糊canny" + ".jpg")

#########################################################################################

# 读取   带入我们处理之后的图像重新用我们的方法得到的1，2结果
re1 = np.loadtxt(outpath + "blur  tagre2" + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')
re = np.zeros((canny.shape[0], canny.shape[1], 3))
for i in range(canny.shape[0]):
	for j in range(canny.shape[1]):
		# if re1[i, j] == 1 or re1[i, j] == 2 or re1[i, j] == 0:
		if re1[i, j] == 1 or re1[i, j] == 2 or re1[i, j] == 0:
			re[i, j, 0] = 255
cv2.imencode('.jpg', re)[1].tofile(outpath + src + "我们的大小边" + ".jpg")

#########################################################################################


th1 = 150
th2 = 200
# 读取我们处理之后的图像
src = "re"
raw = cv2.imread(inpath + src + ".jpg")
canny = cv2.Canny(raw, th1, th2)
re = np.zeros((canny.shape[0], canny.shape[1], 3))
for i in range(canny.shape[0]):
	for j in range(canny.shape[1]):
		if canny[i, j] == 255:
			re[i, j, 1] = 255
cv2.imencode('.jpg', re)[1].tofile(outpath + src + "使用canny检测我们的方法处理之后的结果" + ".jpg")
#
# #########################################################################################
#
# canny处理清晰与模糊的误差
src = "blur"
raw = cv2.imread(inpath + src + ".jpg")
canny = cv2.Canny(raw, th1, th2)
re = np.zeros((canny.shape[0], canny.shape[1], 3))
for i in range(canny.shape[0]):
	for j in range(canny.shape[1]):
		if canny[i, j] == 255:
			re[i, j, 2] = 255
src = "L0"
raw = cv2.imread(inpath + src + ".jpg")
canny = cv2.Canny(raw, th1, th2)
for i in range(canny.shape[0]):
	for j in range(canny.shape[1]):
		if canny[i, j] == 255:
			re[i, j, 1] = 255
cv2.imencode('.jpg', re)[1].tofile(outpath + src + "canny处理清晰与模糊的误差的融合" + ".jpg")

# #########################################################################################
#
# 我们处理清晰与模糊的误差
src = "re"
raw = cv2.imread(inpath + src + ".jpg")
canny = cv2.Canny(raw, th1, th2)
re = np.zeros((canny.shape[0], canny.shape[1], 3))
for i in range(canny.shape[0]):
	for j in range(canny.shape[1]):
		if canny[i, j] == 255:
			re[i, j, 2] = 255
src = "L0"
raw = cv2.imread(inpath + src + ".jpg")
canny = cv2.Canny(raw, th1, th2)
for i in range(canny.shape[0]):
	for j in range(canny.shape[1]):
		if canny[i, j] == 255:
			re[i, j, 1] = 255
cv2.imencode('.jpg', re)[1].tofile(outpath + src + "我们处理清晰与模糊的误差的融合" + ".jpg")

#########################################################################################
#########################################################################################


# # 原图图像canny结果与我们方法处理完之后的结果融合
# src = "shuye"
# raw = cv2.imread(inpath + src + ".jpg")
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
# canny = cv2.Canny(raw2, th1, th2)
# re = np.zeros((canny.shape[0], canny.shape[1], 3))
# for i in range(canny.shape[0]):
# 	for j in range(canny.shape[1]):
# 		if canny[i, j] == 255:
# 			re[i, j, 2] = 255
# # 读取我们处理之后的图像
# src = "4__raw9____shuyeblur"
# raw = cv2.imread(inpath + src + ".jpg")
# canny = cv2.Canny(raw, th1, th2)
# for i in range(canny.shape[0]):
# 	for j in range(canny.shape[1]):
# 		if canny[i, j] == 255:
# 			re[i, j, 1] = 255
# cv2.imencode('.jpg', re)[1].tofile(outpath + src + "原图图像canny结果与我们方法处理完之后的结果融合" + ".jpg")

#########################################################################################
#########################################################################################


# th1 = 150
# th2 = 200
# src = "shuyeblur"
# # 读取原始模糊图像
# raw = cv2.imread(inpath + src + ".jpg")
# canny = cv2.Canny(raw, th1, th2)
# re = np.zeros((canny.shape[0], canny.shape[1], 3))
# for i in range(canny.shape[0]):
# 	for j in range(canny.shape[1]):
# 		if canny[i, j] == 255:
# 			re[i, j, 2] = 255
# cv2.imwrite(outpath + src + "1" + ".jpg", re)
#
# # 读取   带入我们处理之后的图像重新用我们的方法得到的1，2结果
# re1 = np.loadtxt(outpath + "4__raw9____shuyeblur  tagre" + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')
# for i in range(canny.shape[0]):
# 	for j in range(canny.shape[1]):
# 		if re1[i, j] == 1 or re1[i, j] == 2:
# 			re[i, j, 0] = 255
# cv2.imwrite(outpath + src + "1" + ".jpg", re)
#
# th1 = 150
# th2 = 200
# # 读取我们处理之后的图像
# src = "4__raw9____shuyeblur"
# raw = cv2.imread(inpath + src + ".jpg")
# canny = cv2.Canny(raw, th1, th2)
# for i in range(canny.shape[0]):
# 	for j in range(canny.shape[1]):
# 		if canny[i, j] == 255:
# 			re[i, j, 0] = 255
# cv2.imwrite(outpath + src + "2" + ".jpg", re)
