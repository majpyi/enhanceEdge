import cv2
import numpy as np
import Mymodify
import os

inpath = "D:\\experiment\\pic\\batch\\"
outpath = "D:\\out\\try\\batch\\"

files = os.listdir(inpath)


#  按照从中心点右侧为0点逆时针一圈编号的相对位置进行标记8个矩阵
def localpixel(i1, j1, i, j, re, tag):
	if i1 == i and j1 == j + 1:
		re[i1, j1, 0] = tag
	elif i1 == i - 1 and j1 == j + 1:
		re[i1, j1, 1] = tag
	elif i1 == i - 1 and j1 == j:
		re[i1, j1, 2] = tag
	elif i1 == i - 1 and j1 == j - 1:
		re[i1, j1, 3] = tag
	elif i1 == i and j1 == j - 1:
		re[i1, j1, 4] = tag
	elif i1 == i + 1 and j1 == j - 1:
		re[i1, j1, 5] = tag
	elif i1 == i + 1 and j1 == j:
		re[i1, j1, 6] = tag
	elif i1 == i + 1 and j1 == j + 1:
		re[i1, j1, 7] = tag


# re[i, j, 8]    中心像素点  0是交叉   1是小   2是大   -1是两个区域的差值一样
# re[i, j, 9]    能分区 大区最小减去小区最大    不能分区 -1
# re[i, j, 0-7]    1是小 2是大  0是噪声没标记原始值  3是交叉
#  噪声点0，小边点1，大边点2，内部点3
for file in files:
	if not file.endswith(".jpg"):
		continue
	file = file[:file.index(".")]
	if len(file) == 0:
		continue
	src = file
	raw = cv2.imread(inpath + src + ".jpg")
	raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
	# raw2 = cv2.bilateralFilter(raw2, 7, 50, 50)
	np.savetxt(outpath + src + "  gray" + ".csv", raw2, fmt="%d", delimiter=',')

	cv2.imwrite(outpath + src + "gray" + ".jpg", raw2)

	for th in range(2, 1, -2):
		# 存储结果
		re = np.zeros((raw2.shape[0], raw2.shape[1], 10))
		# 存储噪声
		noise_re = np.zeros((raw2.shape[0], raw2.shape[1]))

		for i in range(1, raw2.shape[0] - 1):
			for j in range(1, raw2.shape[1] - 1):
				a, b, noise = Mymodify.Denoising(raw2, i, j)
				num_a = []
				num_b = []
				num_noise = []
				for k in a:
					num_a.append(raw2[k[0]][k[1]])
				for k in b:
					num_b.append(raw2[k[0]][k[1]])
				for k in noise:
					num_noise.append(raw2[k[0]][k[1]])
				num_a = sorted(num_a)
				num_b = sorted(num_b)
				num_noise = sorted(num_noise)
				for k in noise:
					noise_re[noise[0][0], noise[0][1]] += 1

				if min(num_a) > max(num_b) and (min(num_a) - max(num_b)) > th:
					#  可以分为两个部分，寻找中心像素点应该为哪个部分
					mindiff1 = 255
					mindiff2 = 255
					for k in num_a:
						if abs(int(raw2[i, j]) - k) < mindiff1:
							mindiff1 = abs(int(raw2[i, j]) - k)
					for k in num_b:
						if abs(int(raw2[i, j]) - k) < mindiff2:
							mindiff2 = abs(int(raw2[i, j]) - k)
					if mindiff1 > mindiff2:
						re[i, j, 8] = 1
					elif mindiff1 < mindiff2:
						re[i, j, 8] = 2
					else:
						re[i, j, 8] = -1
					#  中心像素点区分度的大小
					re[i, j, 9] = num_a[0] - num_b[-1]
					#  分区之后的周围八个像素点分别相对位置八层的标记
					for n in a:
						tag = 2
						i1 = n[0]
						j1 = n[1]
						localpixel(i1, j1, i, j, re, tag)
					for n in b:
						tag = 1
						i1 = n[0]
						j1 = n[1]
						localpixel(i1, j1, i, j, re, tag)
				elif min(num_b) > max(num_a) and (min(num_b) - max(num_a)) > th:
					#  可以分为两个部分，寻找中心像素点应该为哪个部分
					mindiff1 = 255
					mindiff2 = 255
					for k in num_a:
						if abs(int(raw2[i, j]) - k) < mindiff1:
							mindiff1 = abs(int(raw2[i, j]) - k)
					for k in num_b:
						if abs(int(raw2[i, j]) - k) < mindiff2:
							mindiff2 = abs(int(raw2[i, j]) - k)
					if mindiff1 > mindiff2:
						re[i, j, 8] = 2
					elif mindiff1 < mindiff2:
						re[i, j, 8] = 1
					else:
						re[i, j, 8] = -1
					#  中心像素点区分度的大小
					re[i, j, 9] = num_b[0] - num_a[-1]
					#  分区之后的周围八个像素点分别相对位置八层的标记
					for n in a:
						tag = 1
						i1 = n[0]
						j1 = n[1]
						localpixel(i1, j1, i, j, re, tag)
					for n in b:
						tag = 2
						i1 = n[0]
						j1 = n[1]
						localpixel(i1, j1, i, j, re, tag)
				else:
					# 无法分为两个区域，有交集
					#  中心像素点区分度的大小
					re[i, j, 9] = -1
					#  分区之后的周围八个像素点分别相对位置八层的标记
					for n in a:
						tag = 3
						i1 = n[0]
						j1 = n[1]
						localpixel(i1, j1, i, j, re, tag)
					for n in b:
						tag = 3
						i1 = n[0]
						j1 = n[1]
						localpixel(i1, j1, i, j, re, tag)
					for n in noise:
						tag = 3
						i1 = n[0]
						j1 = n[1]
						localpixel(i1, j1, i, j, re, tag)

		# 存储八层，对八邻域进行统计的结果
		for i in range(8):
			np.savetxt(outpath + src + "  layer" + str(i) + ".csv", re[:, :, i], fmt="%d", delimiter=',')

		# 对9层结果进行汇总标记
		tag = np.zeros((raw2.shape[0], raw2.shape[1]))
		for i in range(1, raw2.shape[0] - 1):
			for j in range(1, raw2.shape[1] - 1):
				for k in range(9):
					if re[i, j][k] == 1:
						tag[i, j] += 1
					elif re[i, j][k] == 2:
						tag[i, j] += 10
		np.savetxt(outpath + src + "  tag" + ".csv", tag, fmt="%d", delimiter=',')
		# 对9层结果判断大小区域过渡区
		tagre = np.zeros((raw2.shape[0], raw2.shape[1]))
		for i in range(1, raw2.shape[0] - 1):
			for j in range(1, raw2.shape[1] - 1):
				if tag[i, j] % 10 != 0 and tag[i, j] // 10 % 10 == 0:
					tagre[i, j] = 1  # 小边
				elif tag[i, j] % 10 == 0 and tag[i, j] // 10 % 10 != 0:
					tagre[i, j] = 2  # 大边
				elif tag[i, j] % 10 == 0 and tag[i, j] // 10 % 10 == 0:
					tagre[i, j] = 3  # 内部
				elif tag[i, j] % 10 != 0 and tag[i, j] // 10 % 10 != 0:
					tagre[i, j] = 0  # 矛盾过渡
		np.savetxt(outpath + src + "  tagre" + ".csv", tagre[:, :], fmt="%d", delimiter=',')
		# 显示过渡点
		guodu_show = np.zeros((tagre.shape[0], tagre.shape[1]))
		for i in range(tagre.shape[0]):
			for j in range(tagre.shape[1]):
				if tagre[i, j] == 0:
					guodu_show[i, j] = 255
		cv2.imwrite(outpath + src + str(th) + "guodu" + ".jpg", guodu_show)

		#  存储区分度
		np.savetxt(outpath + src + "  diff" + ".csv", re[:, :, 9], fmt="%d", delimiter=',')
		# 存储中心像素点的分类
		np.savetxt(outpath + src + "  center" + ".csv", re[:, :, 8], fmt="%d", delimiter=',')
		# 存储噪声点
		np.savetxt(outpath + src + "  noise" + ".csv", noise_re[:, :], fmt="%d", delimiter=',')


		#  中值处理过渡点的函数
		def smooth_mid_gray(tag, raw):
			xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
			yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
			temp = np.zeros((raw2.shape[0], raw2.shape[1]))
			for i in range(1, tag.shape[0] - 1):
				for j in range(1, tag.shape[1] - 1):
					if tag[i, j] > 0:
						l = []
						min_gray = 0
						for k in range(8):
							if tag[i + xxx[k], j + yyy[k]] == -1:
								l.append(raw[i + xxx[k], j + yyy[k]])
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
			return tag

		#  均值处理内部点的函数
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


		# ge = 1
		# guodu = np.zeros((raw2.shape[0], raw2.shape[1]))
		# for i in range(tagre.shape[0]):
		# 	for j in range(tagre.shape[1]):
		# 		if tagre[i, j] == 0:
		# 			guodu[i, j] = 255
		# for l in range(ge):
		# 	temp = guodu.copy()
		# 	for i in range(guodu.shape[0]):
		# 		for j in range(guodu.shape[1]):
		# 			if temp[i, j] == 0:
		# 				temp[i, j] = -1
		# 	for k in range(10):
		# 		smooth_mid_gray(temp, raw2)
		# 	for i in range(guodu.shape[0]):
		# 		for j in range(guodu.shape[1]):
		# 			if temp[i, j] == -1:
		# 				temp[i, j] = 0
		# 	cv2.imwrite(outpath + "temp" + str(th) + "____" + src + ".jpg", temp)
		# cv2.imwrite(outpath + "4__raw" + str(th) + "____" + src + ".jpg", raw2)




		# 平滑的过程  与 L0进行比较
		# 迭代平滑
		ge = 1
		inner = np.zeros((raw2.shape[0], raw2.shape[1]))
		for i in range(inner.shape[0]):
			for j in range(inner.shape[1]):
				if tagre[i, j] == 3:
					inner[i, j] = 255
		edge_big = np.zeros((raw2.shape[0], raw2.shape[1]))
		for i in range(inner.shape[0]):
			for j in range(inner.shape[1]):
				if tagre[i, j] == 2:
					edge_big[i, j] = 255
		edge_small = np.zeros((raw2.shape[0], raw2.shape[1]))
		for i in range(inner.shape[0]):
			for j in range(inner.shape[1]):
				if tagre[i, j] == 1:
					edge_small[i, j] = 255
		guodu = np.zeros((raw2.shape[0], raw2.shape[1]))
		for i in range(inner.shape[0]):
			for j in range(inner.shape[1]):
				if tagre[i, j] == 0:
					guodu[i, j] = 255

		normal = np.zeros((raw2.shape[0], raw2.shape[1]))
		for i in range(guodu.shape[0]):
			for j in range(guodu.shape[1]):
				if guodu[i, j] != 255:
					normal[i, j] = raw2[i,j]
		cv2.imwrite(outpath + "normal" + str(th) + "____" + src + ".jpg", normal)
		# 平滑内部点
		# for i in range(5):
		# 	smooth_gray(inner, raw2)
		# # cv2.imwrite(outpath + "1__raw" + str(th) + "____" + src + ".jpg", raw2)
		# # 用平滑内部点处理大边
		# for l in range(ge):
		# 	temp = edge_big.copy()
		# 	for i in range(guodu.shape[0]):
		# 		for j in range(guodu.shape[1]):
		# 			if inner[i, j] == 255:
		# 				temp[i, j] = -1
		# 	# 大边点为255>0
		# 	# 内部点为 -1
		# 	for k in range(5):
		# 		smooth_mid_gray(temp, raw2)
		# # cv2.imwrite(outpath + "2__raw" + str(th) + "____" + src + ".jpg", raw2)
		# # 用平滑内部点处理小边
		# for l in range(ge):
		# 	temp = edge_small.copy()
		# 	for i in range(guodu.shape[0]):
		# 		for j in range(guodu.shape[1]):
		# 			if inner[i, j] == 255:
		# 				temp[i, j] = -1
		# 	# 小边点为255>0
		# 	# 内部点为 -1
		# 	for k in range(5):
		# 		temp = smooth_mid_gray(temp, raw2)
		# cv2.imwrite(outpath + "3__raw" + str(th) + "____" + src + ".jpg", raw2)

		for l in range(ge):
			temp = guodu.copy()
			for i in range(guodu.shape[0]):
				for j in range(guodu.shape[1]):
					if temp[i, j] == 0:
						temp[i, j] = -1
			# 过渡点为255>0
			# 非过渡点为 -1
			for k in range(15):
				smooth_mid_gray(temp, raw2)
			# 显示处理之后剩余过渡点
			for i in range(guodu.shape[0]):
				for j in range(guodu.shape[1]):
					if temp[i, j] == -1:
						temp[i, j] = 0
			cv2.imwrite(outpath + "temp" + str(th) + "____" + src + ".jpg", temp)
		cv2.imwrite(outpath + "4__raw" + str(th) + "____" + src + ".jpg", raw2)
