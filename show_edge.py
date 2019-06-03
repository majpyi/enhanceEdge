#  显示纯大边点
import cv2
import numpy as np
import matplotlib.pyplot as plt

import modify_rgb_Accumulative_multiple_thresholds
import modify_rgb

# src = "L0"
src = "circle"
# src = "41004"
# src = "8068"
# src = "216053"
# src = "rock2"
# src = "flower"
# src = "basketball"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\try\\" + src + "\\"
raw = cv2.imread(inpath + src + ".jpg")
raw22 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)

# raw_Filter = cv2.bilateralFilter(raw, 9, 150, 150)
raw_Filter = cv2.bilateralFilter(raw, 9, 50, 50)
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
# raw2_Filter = cv2.bilateralFilter(raw2, 9, 150, 150)
raw2_Filter = cv2.bilateralFilter(raw2, 9, 50, 50)
noise_num = 2
th = 5
# a, inner, guodu, edge_big, edge_small = modify_rgb.noise_array(raw2_Filter, raw_Filter, noise_num, th)
# gradient = modify_rgb.gradient_average_rgb(raw2_Filter, raw_Filter, noise_num)
gradient = modify_rgb.gradient_average_rgb(raw22, raw, noise_num)
# np.savetxt(outpath + "gradient" + "___" + src + ".csv", gradient, fmt="%d", delimiter=',')
# gradient = np.loadtxt(outpath + "gradient" + "___" + src + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')

xxx = [0, 0, 1, 1, 0]
yyy = [0, 1, 1, 0, 0]


def hasepoint(gradient, i1, j1, i2, j2, th):
	if min(gradient[i1, j1], gradient[i2, j2]) < th < max(gradient[i1, j1], gradient[i2, j2]):
		return (i1 + i2) / 2, (j1 + j2) / 2
	else:
		return -1, -1


plt.axis("equal")
plt.gca().invert_yaxis()
plt.axis('off')

for i in range(gradient.shape[0] - 1):
	for j in range(gradient.shape[1] - 1):
		xx = []
		yy = []
		for k in range(4):
			# if gradient[i,j] - gradient[i+x[k],j+y[k]]
			x, y = hasepoint(gradient, i + xxx[k], j + yyy[k], i + xxx[k + 1], j + yyy[k + 1], th)
			if x != -1:
				xx.append(x)
				yy.append(y)
		if len(xx) >= 2:
			plt.plot(yy, xx, lw=0.5, color='black')
			# plt.plot(yy, xx, lw=0.5,  color='white')
			# plt.plot(yy, xx, lw=0.5)
# print(xx, end=" ")
# print(yy)
# plt.show()
# plt.savefig("D:\\new" + src, dpi=500, acecolor='white')  # 指定分辨率保存
# plt.savefig("D:\\new" + src, dpi=500, acecolor='black')  # 指定分辨率保存
plt.savefig(outpath+"edge__" + src, dpi=500)  # 指定分辨率保存

# for i in range(guodu.shape[0]):
# 	for j in range(guodu.shape[1]):
# 		if edge_big[i, j] == 1:
# 			edge_big[i, j] = 255
#
# for i in range(guodu.shape[0]):
# 	for j in range(guodu.shape[1]):
# 		if edge_small[i, j] == 1:
# 			edge_small[i, j] = 255
#
# for i in range(guodu.shape[0]):
# 	for j in range(guodu.shape[1]):
# 		if inner[i, j] == 1:
# 			inner[i, j] = 255
#
# for i in range(guodu.shape[0]):
# 	for j in range(guodu.shape[1]):
# 		if guodu[i, j] == 1:
# 			guodu[i, j] = 255
#
# cv2.imwrite(outpath + "big" + str(th) + "____" + src + ".jpg", edge_big)
# cv2.imwrite(outpath + "small" + str(th) + "____" + src + ".jpg", edge_small)
# cv2.imwrite(outpath + "guodu" + str(th) + "____" + src + ".jpg", guodu)
# cv2.imwrite(outpath + "inner" + str(th) + "____" + src + ".jpg", inner)
#
#
# def smooth_mid(tag, raw):
# 	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
# 	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
# 	for i in range(1, tag.shape[0] - 1):
# 		for j in range(1, tag.shape[1] - 1):
# 			if tag[i, j] > 0:
# 				r = []
# 				g = []
# 				b = []
# 				r.append(int(raw[i, j][0]))
# 				g.append(int(raw[i, j][1]))
# 				b.append(int(raw[i, j][2]))
# 				# r = [raw[i, j][0]]
# 				# g =[raw[i, j][1]]
# 				# b =[raw[i, j][2]]
# 				for k in range(8):
# 					if tag[i + xxx[k], j + yyy[k]] == tag[i, j]:
# 						r.append(raw[i + xxx[k], j + yyy[k]][0])
# 						g.append(raw[i + xxx[k], j + yyy[k]][1])
# 						b.append(raw[i + xxx[k], j + yyy[k]][2])
# 				raw[i, j][0] = sorted(r)[int(len(r) / 2)]
# 				raw[i, j][1] = sorted(g)[int(len(r) / 2)]
# 				raw[i, j][2] = sorted(b)[int(len(r) / 2)]
#
# for i in range(100):
# 	# smooth_mid(inner, raw)
# 	# smooth_mid(edge_big, raw)
# 	# smooth_mid(edge_small, raw)
# 	# smooth_mid(guodu, raw)
# 	smooth_mid(inner, raw_Filter)
# 	smooth_mid(edge_big, raw_Filter)
# 	smooth_mid(edge_small, raw_Filter)
# 	smooth_mid(guodu, raw_Filter)
#
# cv2.imwrite(outpath + "raw" + str(th) + "____" + src + ".jpg", raw_Filter)
