import cv2
import numpy as np
import modify_rgb
import sys
from thin import Two, Xihua, array

# sys.setrecursionlimit(1000000000)

#  获取原始数据
# src = "8068"
src = "216053"
# src = "rock2"
# src = "flower"
# src = "basketball"
# src = "f"
# src = "41004"
# src = "241004"
# src = "296059"
# src = "L0"
# src = "ashmolean_000350"
# src = "blur8precise1"
# src = "circle2"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\try\\" + src + "\\"
th = 6
raw = cv2.imread(inpath + src + ".jpg")
# raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# raw_Filter = cv2.bilateralFilter(raw, 7, 150, 150)
raw_Filter = raw
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
# raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
raw2_Filter = raw2
# raw2_Filter = cv2.bilateralFilter(raw2, 7, 150, 150)
cv2.imwrite("D:\\out\\try\\216053\\" + "raw_Filter" + "___" + src + ".jpg", raw_Filter)
cv2.imwrite("D:\\out\\try\\216053\\" + "raw2" + "___" + src + ".jpg", raw2)
cv2.imwrite("D:\\out\\try\\216053\\" + "raw2_Filter" + "___" + src + ".jpg", raw2_Filter)

#
# # 获取过渡区域
# noise_num = 1
# th = 8
# th2 = 2
# # a, b, guodu, d, e = modify_rgb.noise_array(raw2_Filter, raw_Filter, noise_num, th)
# a, b, guodu, d, e = modify_rgb.noise_array(raw2_Filter, raw_Filter, noise_num, th)
# a2, b2, guodu2, d2, e2 = modify_rgb.noise_array(raw2_Filter, raw_Filter, noise_num, th2)
# for i in range(guodu.shape[0]):
# 	for j in range(guodu.shape[1]):
# 		if guodu[i, j] == 1:
# 			guodu[i, j] = 255
# for i in range(guodu2.shape[0]):
# 	for j in range(guodu2.shape[1]):
# 		if guodu2[i, j] == 1:
# 			guodu2[i, j] = 255
#
# # cv2.imwrite("D:\\out\\try\\寻找过渡区域" + str(th) + "___" + src + ".jpg", guodu)
# cv2.imencode('.jpg', guodu)[1].tofile("D:\\out\\try\\寻找过渡区域" + str(th) + "___" + src + ".jpg")
#
# #  进行腐蚀和膨胀
# si = 3
# kernel = np.ones((si, si), np.uint8)
# dilation = cv2.dilate(guodu, kernel)
# # cv2.imwrite("D:\\out\\try\\膨胀" + str(th) + "___" + src + ".jpg", dilation)
# cv2.imencode('.jpg', dilation)[1].tofile("D:\\out\\try\\膨胀" + str(th) + "___" + src + ".jpg")
# np.savetxt("D:\\out\\try\\膨胀" + str(th) + "___" + src + ".csv", dilation, fmt="%d", delimiter=',')
#
# si2 = 2
# kernel2 = np.ones((si2, si2), np.uint8)
# dilation2 = cv2.dilate(guodu2, kernel2)
# iTwo = Two(dilation2)
# iThin = Xihua(iTwo, array)
# # iThin = cv2.dilate(iThin, kernel)
# np.savetxt("D:\\out\\try\\iThin" + str(th) + "___" + src + ".csv", iThin, fmt="%d", delimiter=',')
# cv2.imencode('.jpg', iThin)[1].tofile("D:\\out\\try\\iThin" + str(th) + "___" + src + ".jpg")
#
# for i in range(iTwo.shape[0]):
# 	for j in range(iTwo.shape[1]):
# 		if iThin[i, j] == 0:
# 			dilation[i, j] = 255
# 	# else:
# 	# 	dilation[i, j] = 0
# cv2.imencode('.jpg', dilation)[1].tofile("D:\\out\\try\\膨胀加瘦身结合" + str(th) + "___" + src + ".jpg")
# np.savetxt("D:\\out\\try\\膨胀加瘦身结合" + str(th) + "___" + src + ".csv", dilation, fmt="%d", delimiter=',')
#
#


dilation = np.loadtxt(outpath + "merge____" + str(th) + src + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')
print(type(dilation))
# dilation = np.array([[0, 0, 10, 0], [0, 0, 11, 0], [0, 0, 5, 0], [0, 0, 10, 0]])
# xx = [-1, -1, -1, 0, +1, +1, +1, 0]
# yy = [+1, 0, -1, -1, -1, 0, +1, +1]
xx = [1, -1, 1, -1, -1, 1, 0, 0]
yy = [1, -1, -1, 1, 0, 0, -1, 1]

tag = np.zeros((dilation.shape[0], dilation.shape[1]))


# t = np.zeros((dilation.shape[0], dilation.shape[1]))
#  密闭区域划分进行编号处理
def expend(dilation, x, y, num, tag):
	# dilation[i, j] = num
	# tag[i, j] = num
	# if i <= 1 or i >= dilation.shape[0] - 1 or j <= 1 or j >= dilation.shape[1] - 1:
	#     return
	# for k in range(8):
	#     if (i + xx[k]) <= 1 or (i + xx[k]) >= dilation.shape[0] - 1 or (j + yy[k]) <= 1 or (j + yy[k]) >= \
	#             dilation.shape[1] - 1:
	#         return
	#     elif dilation[i + xx[k], j + yy[k]] == 0:
	#         expend(dilation, i + xx[k], j + yy[k], num, tag)
	# print(type(dilation))
	# print(x)
	while (len(x) != 0):
		tempx = x.pop()
		tempy = y.pop()
		dilation[tempx, tempy] = num
		tag[tempx, tempy] = num
		for k in range(8):
			if (tempx + xx[k]) < 0 or (tempx + xx[k]) > dilation.shape[0] - 1 or (tempy + yy[k]) < 0 or (
							tempy + yy[k]) > \
							dilation.shape[1] - 1:
				continue  # 之所以会有nonetype的出现就是因为在这里一开始写了return了，而你直接return而没有任何返回值当然是nonetype了。
			elif dilation[tempx + xx[k], tempy + yy[k]] == 0:
				x.append(tempx + xx[k])
				y.append(tempy + yy[k])


num = 1
for i in range(dilation.shape[0]):
	for j in range(dilation.shape[1]):
		x = []
		y = []
		if dilation[i, j] == 0:
			# print(1)
			x.append(i)
			y.append(j)
			# print(x.)
			expend(dilation, x, y, num, tag)
			num += 1
# dilation = t
np.savetxt(outpath + "标记封闭区域" + str(th) + src + ".csv", tag, fmt="%d", delimiter=',')

# cv2.imwrite("D:\\out\\try\\开始的原始图像" + str(th) + "___" + src + ".jpg", raw)
cv2.imencode('.jpg', raw)[1].tofile(outpath + "开始的原始图像" + str(th) + "___" + src + ".jpg")


#  迭代均值平滑处理
def smooth(tag, raw):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			sumr = 0
			sumg = 0
			sumb = 0
			num = 0
			if tag[i, j] > 0:
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
			if num != 0:
				raw[i, j][0] = int(sumr / num)
				raw[i, j][1] = int(sumg / num)
				raw[i, j][2] = int(sumb / num)


# def smooth_mid(tag, raw2):
# 	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
# 	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
# 	for i in range(1, tag.shape[0] - 1):
# 		for j in range(1, tag.shape[1] - 1):
# 			if tag[i, j] > 0:
# 				l = {(i, j): raw2[i, j]}
# 				for k in range(8):
# 					if tag[i + xxx[k], j + yyy[k]] == tag[i, j]:
# 						l[(i + xxx[k], j + yyy[k])] = raw2[i, j]
# 					# if len(l) > 0:
# 					re = sorted(l.items(), key=lambda d: d[1])
# 					x = re[int(len(re)/2)][0][0]
# 					y = re[int(len(re)/2)][0][1]
# 					raw[i, j][0] = raw[x, y][0]
# 					raw[i, j][1] = raw[x, y][1]
# 					raw[i, j][2] = raw[x, y][2]

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
				raw[i, j][0] = sorted(r)[int(len(r)/2)]
				raw[i, j][1] = sorted(g)[int(len(r)/2)]
				raw[i, j][2] = sorted(b)[int(len(r)/2)]

			# if sumr != 0 or sumg != 0 or sumb != 0:

def smooth_mid_gray(tag, raw2):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			if tag[i, j] > 0:
				r = []
				r.append(int(raw2[i, j]))
				for k in range(8):
					if tag[i + xxx[k], j + yyy[k]] == tag[i, j]:
						r.append(raw2[i + xxx[k], j + yyy[k]])
				raw2[i, j] = sorted(r)[int(len(r)/2)]

for i in range(30):
	smooth_mid(tag, raw)
	smooth_mid_gray(tag, raw2)

# for i in range(raw2.shape[0]):
#     for j in range(raw2.shape[1]):
#         if tag[i,j]==0:
#             raw[i,j] =
# cv2.imwrite("D:\\out\\try\\平滑之后的图像" + str(th) + "___" + src + ".jpg", raw)
cv2.imencode('.jpg', raw)[1].tofile(outpath + "平滑之后的__原始图像" + str(th) + "___" + src + ".jpg")
cv2.imencode('.jpg', raw)[1].tofile(outpath + "平滑之后的__灰度图像" + str(th) + "___" + src + ".jpg")


# np.savetxt("D:\\out\\try\\smooth" + str(th) + "___" + src + ".csv", raw, fmt="%d", delimiter=',')

# xx1 = [ 1, -1, 1, -1, -1, 1, 0, 0]
# yy1 = [ 1, -1, -1, 1, 0, 0, -1, 1]


def diff(raw, i, j, x, y, min, k, n):
	sum = 0
	sum += abs(int(raw[i, j][0]) - int(raw[x, y][0]))
	sum += abs(int(raw[i, j][1]) - int(raw[x, y][1]))
	sum += abs(int(raw[i, j][2]) - int(raw[x, y][2]))
	if sum < min:
		return sum, k
	return min, n


def diff_gray(raw2, i, j, x, y, min, k, n):
	sum = 0
	sum += abs(int(raw2[i, j]) - int(raw2[x, y]))
	if sum < min:
		return sum, k
	return min, n


def smooth_edge(raw, tag):
	end = 0
	while end == 0:
		end = 1
		for i in range(tag.shape[0]):
			for j in range(tag.shape[1]):
				if tag[i, j] == 0:
					end = 0
					min = 1000
					n = -1
					for k in range(8):
						x = i + xx[k]
						y = j + yy[k]
						if x >= 0 and x < tag.shape[0] and y >= 0 and y < tag.shape[1] and tag[x, y] != 0:
							min, n = diff(raw, i, j, i + xx[k], j + yy[k], min, k, n)
					if n >= 0:
						raw[i, j] = raw[i + xx[n], j + yy[n]]
						tag[i, j] = -1

def smooth_edge_gray(raw2, tag):
	end = 0
	while end == 0:
		end = 1
		for i in range(tag.shape[0]):
			for j in range(tag.shape[1]):
				if tag[i, j] == 0:
					end = 0
					min = 1000
					n = -1
					for k in range(8):
						x = i + xx[k]
						y = j + yy[k]
						if x >= 0 and x < tag.shape[0] and y >= 0 and y < tag.shape[1] and tag[x, y] != 0:
							min, n = diff_gray(raw2, i, j, i + xx[k], j + yy[k], min, k, n)
					if n >= 0:
						raw2[i, j] = raw2[i + xx[n], j + yy[n]]
						tag[i, j] = -1

smooth_edge(raw, tag)
smooth_edge_gray(raw2, tag)


cv2.imencode('.jpg', raw)[1].tofile(outpath + "end_原图" + str(th) + "___" + src + ".jpg")
cv2.imencode('.jpg', raw2)[1].tofile(outpath + "end_灰度图" + str(th) + "___" + src + ".jpg")
