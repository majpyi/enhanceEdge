#  对区域进行划分，各区域中的点进行中值滤波处理

#  显示纯大边点
import cv2
import numpy as np
import matplotlib.pyplot as plt

import modify_rgb_Accumulative_multiple_thresholds
import modify_rgb

# src = "L0"
# src = "296059"
# src = "41004"
# src = "circle"
# src = "cs"
# src = "8068"
# src = "simple"
# src = "blur5precise1"
src = "blur15simple"
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

noise_num = 1
th = 6

a, inner, guodu, edge_big, edge_small = modify_rgb.noise_array(raw2_Filter, raw_Filter, noise_num, th)
# a, inner, guodu, edge_big, edge_small = modify_rgb.noise_array(raw22, raw, noise_num, th)
# raw_Filter = raw


for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		if edge_big[i, j] == 1:
			edge_big[i, j] = 255

for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		if edge_small[i, j] == 1:
			edge_small[i, j] = 255

for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		if inner[i, j] == 1:
			inner[i, j] = 255

for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		if guodu[i, j] == 1:
			guodu[i, j] = 255

si = 2
kernel = np.ones((si, si), np.uint8)
guodu = cv2.dilate(guodu, kernel)
# edge_small = cv2.dilate(edge_small, kernel)
# edge_big = cv2.dilate(edge_big, kernel)

cv2.imwrite(outpath + "big" + str(th) + "____" + src + ".jpg", edge_big)
cv2.imwrite(outpath + "small" + str(th) + "____" + src + ".jpg", edge_small)
cv2.imwrite(outpath + "guodu" + str(th) + "____" + src + ".jpg", guodu)
cv2.imwrite(outpath + "inner" + str(th) + "____" + src + ".jpg", inner)


def smooth_mid(tag, raw):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			if tag[i, j] > 0:
				r = []
				g = []
				b = []
				r.append(int(raw[i, j][0]))
				g.append(int(raw[i, j][1]))
				b.append(int(raw[i, j][2]))
				# r = [raw[i, j][0]]
				# g =[raw[i, j][1]]
				# b =[raw[i, j][2]]
				for k in range(8):
					if tag[i + xxx[k], j + yyy[k]] == tag[i, j]:
						r.append(raw[i + xxx[k], j + yyy[k]][0])
						g.append(raw[i + xxx[k], j + yyy[k]][1])
						b.append(raw[i + xxx[k], j + yyy[k]][2])
				raw[i, j][0] = sorted(r)[int(len(r) / 2)]
				raw[i, j][1] = sorted(g)[int(len(r) / 2)]
				raw[i, j][2] = sorted(b)[int(len(r) / 2)]


def smooth_mid_gray(tag, raw):
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


def smooth_mid_guodu(tag, raw):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	temp = np.zeros((guodu.shape[0], guodu.shape[1]))
	flag = 0
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			if tag[i, j] > 0:
				flag = 1
				r = []
				g = []
				b = []
				for k in range(8):
					# if tag[i + xxx[k], j + yyy[k]] == tag[i, j]:
					if tag[i + xxx[k], j + yyy[k]] == 0:
						r.append(raw[i + xxx[k], j + yyy[k]][0])
						g.append(raw[i + xxx[k], j + yyy[k]][1])
						b.append(raw[i + xxx[k], j + yyy[k]][2])
				if len(r) >= 3:
					raw[i, j][0] = sorted(r)[int(len(r) / 2)]
					raw[i, j][1] = sorted(g)[int(len(r) / 2)]
					raw[i, j][2] = sorted(b)[int(len(r) / 2)]
					temp[i, j] = 1
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			if temp[i, j] == 1:
				tag[i, j] = 0
	return flag


#  迭代均值平滑处理
def smooth(tag, raw):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	flag = 0
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			sumr = 0
			sumg = 0
			sumb = 0
			num = 0
			if tag[i, j] > 0:
				flag = 1
				sumr += raw[i, j][0]
				sumg += raw[i, j][1]
				sumb += raw[i, j][2]
				num += 1
				for k in range(8):
					if tag[i + xxx[k], j + yyy[k]] == tag[i, j]:
						sumr += raw[i + xxx[k], j + yyy[k]][0]
						sumg += raw[i + xxx[k], j + yyy[k]][1]
						sumb += raw[i + xxx[k], j + yyy[k]][2]
						num += 1
				# if sumr != 0 or sumg != 0 or sumb != 0:
				# if num != 0:
				if num >= 2:
					raw[i, j][0] = int(sumr / num)
					raw[i, j][1] = int(sumg / num)
					raw[i, j][2] = int(sumb / num)
	# tag[i, j] = 0
	return flag


def smooth_gray(tag, raw):
	temp = np.zeros((guodu.shape[0], guodu.shape[1]))
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
				# if num >= 3:
				raw[i, j] = int(sum / num)
			# temp[i, j] = 1
	# tag[i, j] = 0
	# for i in range(1, tag.shape[0] - 1):
	# 	for j in range(1, tag.shape[1] - 1):
	# 		if temp[i, j] == 1:
	# 			tag[i, j] = 0
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
					num=0
					end = 0
					min = 1000
					n = -1
					for k in range(8):
						x = i + xxx[k]
						y = j + yyy[k]
						if x >= 0 and x < tag.shape[0] and y >= 0 and y < tag.shape[1] and tag[x, y] == -1:
							num+=1
							min, n = diff_gray(raw2, i, j, i + xxx[k], j + yyy[k], min, k, n)
					if n >= 0 and num>=3:
						raw2[i, j] = raw2[i + xxx[n], j + yyy[n]]
						tag[i, j] = -1

def smooth_edge_gray(tag, raw2):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	end = 0
	z = 0
	while end == 0 and z < 20:
		end = 1
		z+=1
		for i in range(tag.shape[0]):
			for j in range(tag.shape[1]):
				if tag[i, j] == 255:
					num=0
					end = 0
					min = 1000
					n = -1
					for k in range(8):
						x = i + xxx[k]
						y = j + yyy[k]
						if x >= 0 and x < tag.shape[0] and y >= 0 and y < tag.shape[1] and tag[x, y] == -1:
							num+=1
							min, n = diff_gray(raw2, i, j, i + xxx[k], j + yyy[k], min, k, n)
					if n >= 0 and num>=3:
						raw2[i, j] = raw2[i + xxx[n], j + yyy[n]]
						tag[i, j] = -1


generation = 10
g = 1
# for i in range(generation):
# 	smooth(inner, raw_Filter)
# # while smooth(inner, raw) == 1:
# # 	pass
# print(1)
# cv2.imwrite(outpath + "1__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw_Filter)
#
# for i in range(g):
# 	temp = edge_big.copy()
# 	for k in range(generation):
# 		smooth_mid_guodu(temp, raw_Filter)
# # for i in range(generation):
# # 	smooth(edge_big, raw_Filter)
# # while smooth(edge_big, raw) == 1:
# # 	pass
# print(2)
# cv2.imwrite(outpath + "2__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw_Filter)
#
# for i in range(g):
# 	temp = edge_small.copy()
# 	for k in range(generation):
# 		smooth_mid_guodu(temp, raw_Filter)
# # for i in range(generation):
# # 	smooth(edge_small, raw_Filter)
# # while smooth(edge_small, raw) == 1:
# # 	pass
# print(3)
# cv2.imwrite(outpath + "3__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw_Filter)
#
# for i in range(g):
# 	temp = guodu.copy()
# 	for k in range(generation):
# 		smooth_mid_guodu(temp, raw_Filter)
# # while smooth_mid_guodu(guodu, raw) == 1:
# # 	pass
# print(4)
# cv2.imwrite(outpath + "4__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw_Filter)


# smooth(guodu, raw)
# smooth(inner, raw_Filter)
# smooth(edge_big, raw_Filter)
# smooth(edge_small, raw_Filter)
# smooth_mid(guodu, raw_Filter)
#
# cv2.imwrite(outpath + "raw" + str(th) + "____" + src + ".jpg", raw_Filter)
# cv2.imwrite(outpath + "raw没有滤波" + str(th) + "____" + src + ".jpg", raw)
# cv2.imwrite(outpath + "raw没有滤波过渡中值其余均值" + str(th) + "____" + src + ".jpg", raw)
# cv2.imwrite(outpath + "false__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw_Filter)
# print(1)

ge = 1

for i in range(20):
	smooth_gray(inner, raw2_Filter)
# while smooth(inner, raw) == 1:
# 	pass
print(1)
cv2.imwrite(outpath + "1__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw2_Filter)

for l in range(ge):
	temp = edge_big.copy()
	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if inner[i, j] == 255:
				temp[i, j] = -1
	smooth_edge_gray(temp, raw2_Filter)
# for k in range(generation):
# 	smooth_mid_gray(temp, raw2_Filter)
# for i in range(generation):
# 	smooth(edge_big, raw_Filter)
# while smooth(edge_big, raw) == 1:
# 	pass
print(2)
cv2.imwrite(outpath + "2__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw2_Filter)

for l in range(ge):
	temp = edge_small.copy()
	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if inner[i, j] == 255:
				temp[i, j] = -1
	smooth_edge_gray(temp, raw2_Filter)
# for k in range(generation):
# 	smooth_mid_gray(temp, raw2_Filter)

# for i in range(generation):
# 	smooth(edge_small, raw_Filter)
# while smooth(edge_small, raw) == 1:
# 	pass
print(3)
cv2.imwrite(outpath + "3__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw2_Filter)

# re = raw_Filter.copy()
# for i in range(guodu.shape[0]):
# 	for j in range(guodu.shape[1]):
# 		if guodu[i, j] == 255:
# 			re[i, j][0] = 0
# 			re[i, j][1] = 0
# 			re[i, j][2] = 0
# cv2.imwrite(outpath + "5__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", re)


for l in range(ge):
	temp = guodu.copy()
	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if temp[i, j] == 0:
				temp[i, j] = -1
	smooth_edge_gray_guodu(temp, raw2_Filter)
# for k in range(100):
# 	smooth_mid_gray(temp, raw2_Filter)

# while smooth_mid_guodu(guodu, raw) == 1:
# 	pass


print(4)
cv2.imwrite(outpath + "4__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw2_Filter)
