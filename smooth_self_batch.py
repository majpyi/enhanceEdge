#  对区域进行划分，各区域中的点进行中值滤波处理

#  显示纯大边点
import cv2
import numpy as np
import modify_rgb
import modify
import modify_rgb_Accumulative_multiple_thresholds
import os

inpath = "D:\\experiment\\pic\\batch\\"
outpath = "D:\\out\\try\\batch\\"

files = os.listdir(inpath)
for file in files:
	if not file.endswith(".jpg"):
		continue
	file = file[:file.index(".")]
	if len(file) == 0:
		continue
	src = file
	raw = cv2.imread(inpath + src + ".jpg")
	# grond = cv2.imread(inpath + src + "1.jpg")
	raw22 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)

	# raw_Filter = raw
	# raw2_Filter = raw22

	# raw_Filter = cv2.bilateralFilter(raw, 9, 150, 150)
	# raw_Filter = cv2.bilateralFilter(raw, 9, 100, 100)
	raw_Filter = cv2.bilateralFilter(raw, 9, 50, 50)

	raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
	# raw2_Filter = cv2.bilateralFilter(raw2, 9, 150, 150)
	# raw2_Filter = cv2.bilateralFilter(raw2, 9, 100, 100)
	raw2_Filter = cv2.bilateralFilter(raw2, 9, 50, 50)
	raw2_Filter_copy1 = raw2_Filter.copy()
	raw2_Filter_copy2 = raw2_Filter.copy()

	# raw2_Filter = raw22
	# raw_Filter = raw

	noise_num = 1
	# gra_th = 30
	th = 15

	cv2.imwrite(outpath + "raw2_Filter___" + str(th) + src + ".jpg", raw2_Filter)
	cv2.imwrite(outpath + "raw_Filter___" + str(th) + src + ".jpg", raw_Filter)

	# raw2_Filter = raw22
	# raw_Filter = raw

	gra = modify_rgb.gradient_average_abs_rgb(raw2_Filter, raw_Filter, noise_num)
	np.savetxt(outpath + src + "  gra" + ".csv", gra, fmt="%d", delimiter=',')
	for i in range(gra.shape[0]):
		for j in range(gra.shape[1]):
			if gra[i, j] > 30:
				gra[i, j] = 255
			else:
				gra[i, j] = 0
	np.savetxt(outpath + src + "  gra_tag" + ".csv", gra, fmt="%d", delimiter=',')
	cv2.imwrite(outpath + "gra_tag" + str(th) + "____" + src + ".jpg", gra)

	# print(1111)
	a, inner, guodu, edge_big, edge_small = modify_rgb.noise_array(raw2_Filter, raw_Filter, noise_num, th)

	# a, inner, guodu, edge_big, edge_small = modify.noise_array(raw22, noise_num, th)
	# a, inner, guodu, edge_big, edge_small = modify_rgb.noise_array(raw22, raw, noise_num, th)

	# th1 = 3
	# th2 = 8
	# a, inner, guodu, d, e = modify_rgb_Accumulative_multiple_thresholds.noise_array(raw2_Filter, raw_Filter, noise_num, th1,
	#                                                                             th2)

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
	# guodu = cv2.dilate(guodu, kernel)
	# edge_small = cv2.dilate(edge_small, kernel)
	# edge_big = cv2.dilate(edge_big, kernel)
	cv2.imwrite(outpath + "guodu" + str(th) + "____" + src + ".jpg", guodu)
	np.savetxt(outpath + src + "  guodu" + ".csv", guodu, fmt="%d", delimiter=',')
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
					if len(l) >= 3:
						if len(l) % 2 == 0:
							re1 = sorted(l)[int(len(l) / 2)]
							re2 = sorted(l)[int((len(l) - 2) / 2)]
							if abs(re1 - int(raw[i, j])) > abs(re2 - int(raw[i, j])):
								raw[i, j] = re2
							else:
								raw[i, j] = re1
						else:
							raw[i, j] = sorted(l)[int(len(l) / 2)]
						temp[i, j] = 1
		for i in range(1, tag.shape[0] - 1):
			for j in range(1, tag.shape[1] - 1):
				if temp[i, j] == 1:
					tag[i, j] = -1


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
		for k in range(20):
			smooth_mid_gray(temp, raw2_Filter)
	cv2.imwrite(outpath + "4__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", raw2_Filter)

	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if temp[i, j] == -1:
				temp[i, j] = 0
	cv2.imwrite(outpath + "temp" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg", temp)

	raw = cv2.imread(outpath + "4__raw" + str(th) + "noisenum" + str(noise_num) + "____" + src + ".jpg")


	raw22 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
	# a, inner, guodu, edge_big, edge_small = modify_rgb.noise_array(raw22, raw, noise_num, th)
	# a, inner, guodu, edge_big, edge_small = modify.noise_array(raw2_Filter, noise_num, th)
	# for i in range(guodu.shape[0]):
	# 	for j in range(guodu.shape[1]):
	# 		if guodu[i, j] == 1:
	# 			guodu[i, j] = 255
	# cv2.imwrite(outpath + "newguodu" + str(th) + "____" + src + ".jpg", guodu)
	#
	# for i in range(guodu.shape[0]):
	# 	for j in range(guodu.shape[1]):
	# 		if edge_big[i, j] == 1 or edge_small[i, j] == 1:
	# 			edge_big[i, j] = 255
	#
	# cv2.imwrite(outpath + "newedge" + str(th) + "____" + src + ".jpg", edge_big)

	th1 = 50
	th2 = 150
	canny = cv2.Canny(raw2_Filter_copy1, th1, th2)  # 原始图像
	# r = grond.copy()
	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if canny[i, j] == 255:
				raw2_Filter_copy1[i, j] = 255
				# r[i, j, 1] = 0
				# r[i, j, 2] = 0
	cv2.imwrite(outpath + "re1 "+str(th) + src + ".jpg", raw2_Filter_copy1)

	# canny = cv2.Canny(raw2_Filter_copy, th1, th2)  # 模糊图像
	# r = grond.copy()
	# for i in range(guodu.shape[0]):
	# 	for j in range(guodu.shape[1]):
	# 		if canny[i, j] == 255:
	# 			r[i, j, 0] = 255
	# 			r[i, j, 1] = 0
	# 			r[i, j, 2] = 0
	# cv2.imwrite(outpath + "re2" + src + ".jpg", r)
	#
	canny = cv2.Canny(raw2_Filter, th1, th2)  # 修复图像
	# r = grond.copy()
	for i in range(guodu.shape[0]):
		for j in range(guodu.shape[1]):
			if canny[i, j] == 255:
				# r[i, j, 0] = 255
				raw2_Filter_copy2[i, j] = 255
				# r[i, j, 1] = 0
				# r[i, j, 2] = 0
	cv2.imwrite(outpath + "re3 "+str(th) + src + ".jpg", raw2_Filter_copy2)
