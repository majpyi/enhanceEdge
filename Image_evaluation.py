# PSNR.py

import numpy as np
import math
import cv2

import cv2
import numpy as np
import math
# 图像压缩中典型的峰值信噪比值在 30 到 40dB 之间，愈高愈好。
# 当PSNR值大于30dB的时候，可以认为去噪或压缩后的图像质量较好，低于20dB表示图像质量不可接受


def psnr1(img1, img2):
	mse = np.mean((img1 / 1.0 - img2 / 1.0) ** 2)
	# mse = np.mean((img1 - img2) ** 2)
	if mse < 1.0e-10:
		return 100
	return 10 * math.log10(255.0 ** 2 / mse)


def psnr2(img1, img2):
	mse = np.mean((img1 / 255. - img2 / 255.) ** 2)
	if mse < 1.0e-10:
		return 100
	PIXEL_MAX = 1
	return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


inpath = "D:\\experiment\\pic\\batch\\"
outpath = "D:\\out\\try\\batch\\"
# src = "4__raw5____9GaussianBlursquare"
src = "4__raw10____raw"
src = "L0"
raw1 = cv2.imread(inpath + src + ".jpg")
raw1 = cv2.cvtColor(raw1, cv2.COLOR_BGR2GRAY)
src = "square"
src = "41004"
src = "re"
raw2 = cv2.imread(inpath + src + ".jpg")
raw2 = cv2.cvtColor(raw2, cv2.COLOR_BGR2GRAY)

print(psnr1(raw1, raw2))
# print(psnr2(raw1, raw2))


inpath = "D:\\experiment\\pic\\batch\\"
outpath = "D:\\out\\try\\batch\\"
src = "square"
src = "41004"
src = "L0"
src = "L0"
raw1 = cv2.imread(inpath + src + ".jpg")
raw1 = cv2.cvtColor(raw1, cv2.COLOR_BGR2GRAY)
# src = "9GaussianBlursquare"
src = "blur1041004"
src = "blur"
# src = "L0"
raw2 = cv2.imread(inpath + src + ".jpg")
raw2 = cv2.cvtColor(raw2, cv2.COLOR_BGR2GRAY)

print(psnr1(raw1, raw2))
# print(psnr2(raw1, raw2))