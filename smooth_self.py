#  对区域进行划分，各区域中的点进行中值滤波处理

#  显示纯大边点
import cv2
import numpy as np
import matplotlib.pyplot as plt

import modify_rgb_Accumulative_multiple_thresholds
import modify_rgb
import modify

src = "L0"
src = "41004"
# src = "4__raw6noisenum2____113044"
# src = "296059"
# src = "101085"
# src = "113044"
# src = "113016"
# src = "circle"
# src = "cs"
# src = "8068"
# src = "simple"
# src = "blur5precise1"
# src = "blur15simple"
# src = "blur5296059"
# src = "blur5296059"
# src = "216053"
# src = "385028"
# src = "rock2"
# src = "flower"
# src = "basketball"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\try\\" + src + "\\"
raw = cv2.imread(inpath + src + ".jpg")
raw22 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)

# raw_Filter = raw
# raw2_Filter = raw22

raw_Filter = cv2.bilateralFilter(raw, 9, 150, 150)
# raw_Filter = cv2.bilateralFilter(raw, 9, 50, 50)
cv2.imwrite(outpath + "raw_Filter___" + src + ".jpg", raw_Filter)

raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 9, 150, 150)
# raw2_Filter = cv2.bilateralFilter(raw2, 9, 50, 50)

cv2.imwrite(outpath + "raw2_Filter___" + src + ".jpg", raw2_Filter)

noise_num = 2
th = 6

# raw2_Filter = raw22
# raw_Filter = raw

a, inner, guodu, edge_big, edge_small = modify_rgb.noise_array(raw2_Filter, raw_Filter, noise_num, th)
# a, inner, guodu, edge_big, edge_small = modify_rgb.noise_array(raw22, raw, noise_num, th)


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


si = 2
kernel = np.ones((si, si), np.uint8)
# guodu = cv2.dilate(guodu, kernel)
# inner = cv2.dilate(inner, kernel)
# edge_small = cv2.dilate(edge_small, kernel)
# edge_big = cv2.dilate(edge_big, kernel)

for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		if guodu[i, j] == 1:
			guodu[i, j] = 255

for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		if edge_big[i, j] == 1 and guodu[i, j] != 255:
			edge_big[i, j] = 255

for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		if edge_small[i, j] == 1 and guodu[i, j] != 255:
			edge_small[i, j] = 255

for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		# if inner[i, j] == 1 and edge_big[i, j] != 255 and edge_small[i, j] != 255 and guodu[i, j] != 255:
		if inner[i, j] == 1 and guodu[i, j] != 255:
			inner[i, j] = 255

cv2.imwrite(outpath + "guodu" + str(th) + "____" + src + ".jpg", guodu)
cv2.imwrite(outpath + "big" + str(th) + "____" + src + ".jpg", edge_big)
cv2.imwrite(outpath + "small" + str(th) + "____" + src + ".jpg", edge_small)
cv2.imwrite(outpath + "inner" + str(th) + "____" + src + ".jpg", inner)


def smooth_mid_gray(tag, raw):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	temp = np.zeros((guodu.shape[0], guodu.shape[1]))
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			if tag[i, j] > 0:
				l = []
				min_gray = 0
				# l.append(raw[i, j])
				for k in range(8):
					if tag[i + xxx[k], j + yyy[k]] == -1:
						l.append(raw[i + xxx[k], j + yyy[k]])
				# if abs(int(raw[i + xxx[k], j + yyy[k]]) - int(raw[i, j])) < abs(int(min_gray) - int(raw[i, j])):
				# 	min_gray = raw[i + xxx[k], j + yyy[k]]
				if len(l) >= 2:
					if len(l) % 2 == 0:
						re1 = sorted(l)[int(len(l) / 2)]
						re2 = sorted(l)[int((len(l) - 2) / 2)]
						if abs(re1 - int(raw[i, j])) > abs(re2 - int(raw[i, j])):
							raw[i, j] = re2
						else:
							raw[i, j] = re1
					# raw[i, j] = min_gray
					else:
						raw[i, j] = sorted(l)[int(len(l) / 2)]
					# raw[i, j] = sorted(l)[int(len(l) / 2)]
					temp[i, j] = 1
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			if temp[i, j] == 1:
				tag[i, j] = -1


def smooth_mid_gray_cs(tag, raw, ci):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	temp = np.zeros((guodu.shape[0], guodu.shape[1]))
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			if tag[i, j] > 0:
				l = []
				# l.append(raw[i, j])
				for k in range(8):
					if tag[i + xxx[k], j + yyy[k]] == -1:
						l.append(raw[i + xxx[k], j + yyy[k]])
				if len(l) >= 3:
					raw[i, j] = sorted(l)[int(len(l) / 2)]
					temp[i, j] = 1
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			if temp[i, j] == 1:
				tag[i, j] = -1
	cv2.imwrite(outpath + str(ci) + src + "____" + str(th) + ".jpg", raw2_Filter)


def smooth_gray(tag, raw):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	flag = 0
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			sum = 0
			num = 0
			if tag[i, j] > 0:
				flag = 1
				sum += raw[i, j]
				num += 1
				for k in range(8):
					if tag[i + xxx[k], j + yyy[k]] == tag[i, j]:
						sum += raw[i + xxx[k], j + yyy[k]]
						num += 1
				raw[i, j] = int(sum / num)
	return flag


def diff_gray(raw2, i, j, x, y, min, k, n):
	sum = 0
	sum += abs(int(raw2[i, j]) - int(raw2[x, y]))
	if sum < min:
		return sum, k
	return min, n


def smooth_edge_gray_guodu(tag, raw2):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	end = 0
	while end == 0:
		end = 1
		for i in range(tag.shape[0]):
			for j in range(tag.shape[1]):
				if tag[i, j] == 255:
					num = 0
					end = 0
					min = 1000
					n = -1
					for k in range(8):
						x = i + xxx[k]
						y = j + yyy[k]
						if 0 <= x < tag.shape[0] and 0 <= y < tag.shape[1] and tag[x, y] == -1:
							num += 1
							min, n = diff_gray(raw2, i, j, i + xxx[k], j + yyy[k], min, k, n)
					if n >= 0 and num >= 3:
						raw2[i, j] = raw2[i + xxx[n], j + yyy[n]]
						tag[i, j] = -1


def smooth_edge_gray(tag, raw2):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	end = 0
	z = 0
	while end == 0 and z < 20:
		end = 1
		z += 1
		for i in range(tag.shape[0]):
			for j in range(tag.shape[1]):
				if tag[i, j] == 255:
					num = 0
					end = 0
					min = 1000
					n = -1
					for k in range(8):
						x = i + xxx[k]
						y = j + yyy[k]
						if x >= 0 and x < tag.shape[0] and y >= 0 and y < tag.shape[1] and tag[x, y] == -1:
							num += 1
							min, n = diff_gray(raw2, i, j, i + xxx[k], j + yyy[k], min, k, n)
					if n >= 0 and num >= 3:
						raw2[i, j] = raw2[i + xxx[n], j + yyy[n]]
						tag[i, j] = -1


generation = 10
ge = 1

for i in range(40):
	smooth_gray(inner, raw2_Filter)
cv2.imwrite(outpath + "1__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw2_Filter)

for l in range(ge):
	temp = edge_big.copy()
	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if inner[i, j] == 255:
				temp[i, j] = -1
	for k in range(5):
		smooth_mid_gray(temp, raw2_Filter)
cv2.imwrite(outpath + "2__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw2_Filter)

for l in range(ge):
	temp = edge_small.copy()
	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if inner[i, j] == 255:
				temp[i, j] = -1
	for k in range(5):
		smooth_mid_gray(temp, raw2_Filter)
cv2.imwrite(outpath + "3__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw2_Filter)

for l in range(ge):
	temp = guodu.copy()
	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if temp[i, j] == 0:
				temp[i, j] = -1
	# smooth_edge_gray_guodu(temp, raw2_Filter)
	for k in range(50):
		smooth_mid_gray(temp, raw2_Filter)
cv2.imwrite(outpath + "4__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw2_Filter)

# raw = cv2.imread(outpath + "4__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg")
# raw22 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
# a, inner, guodu, edge_big, edge_small = modify_rgb.noise_array(raw22, raw, noise_num, th)
a, inner, guodu, edge_big, edge_small = modify.noise_array(raw2_Filter, noise_num, th)
for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		if guodu[i, j] == 1:
			guodu[i, j] = 255
cv2.imwrite(outpath + "newguodu" + str(th) + "____" + src + ".jpg", guodu)

for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		if edge_big[i, j] == 1 or edge_small[i, j] == 1:
			edge_big[i, j] = 255

cv2.imwrite(outpath + "newedge" + str(th) + "____" + src + ".jpg", edge_big)
