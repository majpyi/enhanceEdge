import cv2
import numpy as np
import Mymodify
import os

inpath = "D:\\experiment\\pic\\batch\\"
outpath = "D:\\out\\try\\batch\\"
xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
src = "blur"
# raw2 = np.array([[1, 1, 1], [1, 1, 1], [11, 11, 1]])
# raw2 = np.array([[1, 100, 1], [1, 1, 1], [11, 11, 11]])
raw = cv2.imread(inpath + src + ".jpg")
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
# raw2 = np.array([[1, 1, 1], [1, 1, 5], [100, 100, 1]])
# raw2 = np.array([[1, 1, 1], [1, 1, 1], [100, 1, 1]])
# for i in range(1, raw2.shape[0] - 1):
# 	for j in range(1, raw2.shape[1] - 1):
# noise, a, b = modify4y2r.point_classification(raw2, i, j,1)
# a, b, noise = Mymodify.Denoising(raw2, i, j)
# print(a)
# print(b)
# print(noise)
re1 = np.loadtxt(outpath + src + "  tagre" + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')
x = 76 - 1
y = 229 - 1
print(re1[76, 229])
for k in range(8):
	print(re1[x + xxx[k], y + yyy[k]])
	a, b, noise = Mymodify.Denoising(raw2, x + xxx[k], y + yyy[k])
	print(a, end="  ")

	print(b, end="  ")

	print(noise, end="  ")
	for m in a:
		print(raw2[m[0],m[1]],end=" ")
	for m in b:
		print(raw2[m[0], m[1]], end=" ")
	for m in noise:
		print(raw2[m[0],m[1]],end=" ")
	print()