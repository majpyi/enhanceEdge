import numpy as np
import time


# class point：
#     def __init__(self):
#         self.value = 0
#         self.rgb = [0,0,0]

def line_energy(p1, p2):
	return (p1 - p2) * (p1 - p2)


def line_energy_rgb(p1, p2):
	count = 0
	for i in range(3):
		count += line_energy(p1[i], p2[i])
	return count


# 找八邻域点，组成列表
# 参数：灰度矩阵，rgb矩阵，像素点坐标,邻域个数
# 得到：邻域点(值)列表,邻域点rgb的列表
def point_list(gray, rgb, i, j, num=8):
	lists = []
	addr = []  # 在gray中的坐标
	lists_rgb = []
	if num == 8:
		lists = []  # 八邻域灰度值从左上开始沿顺时针方向排列
		addr = []  # 在gray中的坐标
		lists_rgb = []
		lists.extend(
			[gray[i - 1, j - 1], gray[i - 1, j], gray[i - 1, j + 1], gray[i, j + 1], gray[i + 1, j + 1], gray[i + 1, j],
			 gray[i + 1, j - 1], gray[i, j - 1]])
		lists = [int(i) for i in lists]
		lists_rgb.extend(
			[rgb[i - 1, j - 1], rgb[i - 1, j], rgb[i - 1, j + 1], rgb[i, j + 1], rgb[i + 1, j + 1], rgb[i + 1, j],
			 rgb[i + 1, j - 1], rgb[i, j - 1]])
		lists_rgb = [[int(i[0]), int(i[1]), int(i[2])] for i in lists_rgb]
		addr.extend(((i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1), (i + 1, j + 1), (i + 1, j), (i + 1, j - 1),
		             (i, j - 1)))
	if num == 16:
		lists = []  # 八邻域灰度值从左上开始沿顺时针方向排列
		addr = []
		lists_rgb = []
		lists.extend([gray[i - 2, j - 2], gray[i - 2, j - 1], gray[i - 2, j], gray[i - 2, j + 1], gray[i - 2, j + 2],
		              gray[i - 1, j + 2], gray[i, j + 2], gray[i + 1, j + 2], gray[i + 2, j + 2], gray[i + 2, j + 1],
		              gray[i + 2, j], gray[i + 2, j - 1], gray[i + 2, j - 2], gray[i + 1, j - 2], gray[i, j - 2],
		              gray[i - 1, j - 2]])
		lists = [int(i) for i in lists]
		lists_rgb.extend([rgb[i - 2, j - 2], rgb[i - 2, j - 1], rgb[i - 2, j], rgb[i - 2, j + 1], rgb[i - 2, j + 2],
		                  rgb[i - 1, j + 2], rgb[i, j + 2], rgb[i + 1, j + 2], rgb[i + 2, j + 2], rgb[i + 2, j + 1],
		                  rgb[i + 2, j], rgb[i + 2, j - 1], rgb[i + 2, j - 2], rgb[i + 1, j - 2], rgb[i, j - 2],
		                  rgb[i - 1, j - 2]])
		lists_rgb = [[int(i[0]), int(i[1]), int(i[2])] for i in lists_rgb]
		addr.extend(((i - 2, j - 2), (i - 2, j - 1), (i - 2, j), (i - 2, j + 1), (i - 2, j + 2), (i - 1, j + 2),
		             (i, j + 2), (i + 1, j + 2), (i + 2, j + 2), (i + 2, j + 1), (i + 2, j), (i + 2, j - 1),
		             (i + 2, j - 2), (i + 1, j - 2), (i, j - 2), (i - 1, j - 2)))
	return lists, addr, lists_rgb


def least_energy(point_list, point_list_rgb):
	line = []  # 存放边的能量
	for p in range(-1, len(point_list) - 1):
		line.append(line_energy_rgb(point_list_rgb[p], point_list_rgb[p + 1]))
	line_1 = line[:]  # 副本
	a = []
	b = []
	a_index = []
	b_index = []
	del_large_index = []  # 存储边最大的index
	del_large_index_2 = []
	max_count = line.count(max(line))  # 最大值同时有几个
	max_diff = max(line)  # 最大的边的差值
	start = 0
	for i in range(len(line)):
		if line[i] == max_diff:  # 如果是最大的值
			del_large_index.append(i)
			start = i + 1
	# print(max_count, "max_index", del_large_index)
	line_1.sort(reverse=1)
	# print(line_1)
	flag = 0
	be = line_1[0]
	for i in range(1, len(line_1)):
		if line_1[i] == be:
			continue
		else:
			flag = 1
			break
	if flag == 0:  # 所有一个值
		# print("!!!!!!!!!")
		energy = 0
		a.append(point_list[0])
		b.append(point_list[1:])
		a_index.append(0)
		for ii in range(1, len(point_list)):
			b_index.append(ii)
		return energy, a, b, a_index, b_index
	else:
		max_diff_2 = line_1[max_count]
		max_count_2 = line_1.count(max_diff_2)

	for i in range(len(line)):
		if line[i] == max_diff_2:  # 如果是最大的值
			del_large_index_2.append(i)
			start = i + 1
	# print(max_count_2, "max_index_2", del_large_index_2)
	# print("!!!del_large_index,  del_large_index_2 ", del_large_index, del_large_index_2)
	energy = sum(line) - max_diff - max_diff_2

	a_b_diff = []  # 存储每种搭配下ab两区的差值
	if (len(del_large_index) >= 2):  # 最大的值不止一个
		for i in del_large_index:
			mm = del_large_index.index(i)
			for j in del_large_index[mm + 1:]:
				temp_a = []
				temp_b = []
				if i < j:
					temp_a.extend(point_list[i:j])
					temp_b.extend(point_list[0:i])
					temp_b.extend(point_list[j:len(point_list)])
				else:
					temp_a.extend(point_list[j:i])
					temp_b.extend(point_list[0:j])
					temp_b.extend(point_list[i:len(point_list)])
				# print(temp_a, temp_b)
				diff = abs(sum(temp_a) / len(temp_a) - sum(temp_b) / len(temp_b))
				a_b_diff.append((diff, i, j))
	else:
		for i in del_large_index:
			for j in del_large_index_2:
				temp_a = []
				temp_b = []
				if i < j:
					temp_a.extend(point_list[i:j])
					temp_b.extend(point_list[0:i])
					temp_b.extend(point_list[j:len(point_list)])
				else:
					temp_a.extend(point_list[j:i])
					temp_b.extend(point_list[0:j])
					temp_b.extend(point_list[i:len(point_list)])
				# print(temp_a, temp_b)
				diff = abs(sum(temp_a) / len(temp_a) - sum(temp_b) / len(temp_b))
				a_b_diff.append((diff, i, j))
	# print(a_b_diff)
	# 分区差别最大的一组
	max_index = a_b_diff.index(max(a_b_diff))
	# print(a_b_diff[max_index])
	max_i = a_b_diff[max_index][1]
	max_j = a_b_diff[max_index][2]
	if max_i < max_j:
		a.extend(point_list[max_i:max_j])
		for ii in range(max_i, max_j):
			a_index.append(ii)
		b.extend(point_list[0:max_i])
		for ii in range(0, max_i):
			b_index.append(ii)
		b.extend(point_list[max_j:len(point_list)])
		for ii in range(max_j, len(point_list)):
			b_index.append(ii)
	else:
		a.extend(point_list[max_j:max_i])
		for ii in range(max_j, max_i):
			a_index.append(ii)
		b.extend(point_list[0:max_j])
		for ii in range(0, max_j):
			b_index.append(ii)
		b.extend(point_list[max_i:len(point_list)])
		for ii in range(max_i, len(point_list)):
			b_index.append(ii)

	return energy, a, b, a_index, b_index


# 根据中心点像素和与之的相对位置求八邻域点内的坐标
# 参数：中心像素点坐标，相对位置（从左上为0顺指针标记）,邻域个数
# 得到：邻域点像素
def find_index(i, j, x, num=8):
	ii = 0
	jj = 0
	if num == 8:
		if ((x == 0) | (x == 1) | (x == 2)):
			ii = i - 1
		if ((x == 4) | (x == 5) | (x == 6)):
			ii = i + 1
		if ((x == 3) | (x == 7)):
			ii = i

		if ((x == 0) | (x == 6) | (x == 7)):
			jj = j - 1
		if ((x == 2) | (x == 3) | (x == 4)):
			jj = j + 1
		if ((x == 1) | (x == 5)):
			jj = j
	if num == 16:
		if ((x == 0) | (x == 1) | (x == 2) | (x == 3) | (x == 4)):
			ii = i - 2
		if ((x == 5) | (x == 15)):
			ii = i - 1
		if ((x == 6) | (x == 14)):
			ii = i
		if ((x == 7) | (x == 13)):
			ii = i + 1
		if ((x == 8) | (x == 9) | (x == 10) | (x == 11) | (x == 12)):
			ii = i + 2

		if ((x == 0) | (x == 15) | (x == 14) | (x == 13) | (x == 12)):
			jj = j - 2
		if ((x == 1) | (x == 11)):
			jj = j - 1
		if ((x == 2) | (x == 10)):
			jj = j
		if ((x == 3) | (x == 9)):
			jj = j + 1
		if ((x == 4) | (x == 5) | (x == 6) | (x == 7) | (x == 8)):
			jj = j + 2
	return ii, jj


# 邻域内定位最有可能的噪声
# 参数：灰度矩阵图，像素点坐标,邻域个数
# 得到：噪声像素在八邻域中的位置
def find_noise(gray, rgb, i, j, num=8):
	energy_list = []
	point_lists = point_list(gray, rgb, i, j, num)[0]
	rgb_lists = point_list(gray, rgb, i, j, num)[2]
	#     print("point_list",point_list)
	for x in range(len(point_lists)):
		li = point_lists[:]
		del li[x]
		#         print(li)
		#         print(least_energy(li)[0])
		energy_list.append(least_energy(li, rgb_lists)[0])
	#     print(energy_list)
	minn = energy_list.index(min(energy_list))
	#     print(point_lists)
	# 当只有一个数字不一样的时候（特殊情况）
	sorted_list = sorted(point_lists)
	flag = 1
	mid = sorted_list[1:-1]  # 除开第一个和最后一个
	avg = sum(mid) / len(mid)
	for men in mid:
		if men != avg:
			flag = 0
			break
	if flag == 1:
		if ((avg == sorted_list[0]) & (avg != sorted_list[-1])):
			minn = point_lists.index(sorted_list[-1])
		elif ((avg == sorted_list[-1]) & (avg != sorted_list[0])):
			minn = point_lists.index(sorted_list[0])
	return minn


# # 每个八邻域内定位3个最有可能噪声点
# # 参数：灰度矩阵图，中心像素坐标,假设八邻域中可能含有的噪声个数,3*3的八邻域或者是5*5的24邻域
# # 得到：三个噪声点，A,B区与中心像素的坐标
# # 如果噪声相同值多个,按顺序删除
# def point_classification(gray, i, j, count, num=8):
#     list_point = point_list(gray, i, j, num)[0]  # 初始的八邻域
#     e_point_1 = list_point[:]  # 副本
#     e_point = list_point[:]  # 副本
#     e_point.reverse()
#     point_lists = list_point[:]  # point_list作为副本，负责三次减去噪声
#     minn = []  # 获取定位到的噪声在gray中的坐标
#     rest_a = []  # 获取出3个噪声点外的a区点灰度值
#     rest_b = []  # 获取出3个噪声点外的b区点灰度值
#     a = []  # a区的index
#     b = []  # b区的index
#     noise = []  # 噪声的index
#     while (count > 0):  # 计数3次
#         energy_list = []  # 存储边的能量
#         # 获取一个噪声
#         for x in range(len(point_lists)):
#             li = point_lists[:]
#             lli = point_lists[:]
#             del li[x]
#             energy_list.append(least_energy(li)[0])
#         noise_index = energy_list.index(min(energy_list))  # 得到噪声的领域index
#         sorted_list = sorted(point_lists)
#         flag = 1
#         mid = sorted_list[1:-1]  # 除开第一个和最后一个
#         avg = sum(mid) / len(mid)
#         for men in mid:
#             if men != avg:
#                 flag = 0
#                 break
#         if flag == 1:
#             if ((avg == sorted_list[0]) & (avg != sorted_list[-1])):
#                 noise_index = point_lists.index(sorted_list[-1])
#             elif ((avg == sorted_list[-1]) & (avg != sorted_list[0])):
#                 noise_index = point_lists.index(sorted_list[0])
#         for ii in noise:
#             # print('i=',i)
#             if noise_index >= ii:
#                 noise_index = noise_index + 1
#             else:
#                 break
#         noise.append(noise_index)
#         noise.sort()
#         minn.append(find_index(i, j, noise_index, num))
#         del point_lists[energy_list.index(min(energy_list))]  # 删去定位噪声，剩下的邻域为下一次定位噪声做准备
#         count = count - 1
#         if count == 0:
#             least = least_energy(point_lists)
#             rest_a.extend(least[3])
#             rest_b.extend(least[4])
#             for ii in rest_a:
#                 for iii in noise:
#                     if ii >= iii:
#                         ii = ii + 1
#                 a.append(find_index(i, j, ii, num))
#             for ii in rest_b:
#                 for iii in noise:
#                     if ii >= iii:
#                         ii = ii + 1
#                 b.append(find_index(i, j, ii, num))
#     return minn, a, b


# 每个八邻域内定位3个最有可能噪声点
# 参数：灰度矩阵图，中心像素坐标
# 得到：三个噪声点，A,B区与中心像素的坐标
# 如果噪声相同值多个,会删除那个比较多的区域的像素点
def point_classification(gray, rgb, i, j, count, num=8):
	list_point = point_list(gray, rgb, i, j, num)[0]  # 初始的八邻域
	list_rgb = point_list(gray, rgb, i, j, num)[2]
	e_point_1 = list_point[:]  # 副本
	e_point = list_point[:]  # 副本
	e_point.reverse()
	point_lists = list_point[:]  # point_list作为副本，负责三次减去噪声
	minn = []  # 获取定位到的噪声在gray中的坐标
	rest_a = []  # 获取出3个噪声点外的a区点灰度值
	rest_b = []  # 获取出3个噪声点外的b区点灰度值
	a = []  # a区的index
	b = []  # b区的index
	noise = []  # 噪声的index
	while (count > 0):  # 计数3次
		energy_list = []  # 存储边的能量
		# 获取一个噪声
		for x in range(len(point_lists)):
			li = point_lists[:]
			lli = point_lists[:]
			del li[x]
			energy_list.append(least_energy(li, list_rgb)[0])
		noise_index = energy_list.index(min(energy_list))  # 得到噪声的领域index
		sorted_list = sorted(point_lists)
		flag = 1
		mid = sorted_list[1:-1]  # 除开第一个和最后一个
		avg = sum(mid) / len(mid)
		for men in mid:
			if men != avg:
				flag = 0
				break
		if flag == 1:
			if ((avg == sorted_list[0]) & (avg != sorted_list[-1])):
				noise_index = point_lists.index(sorted_list[-1])
			elif ((avg == sorted_list[-1]) & (avg != sorted_list[0])):
				noise_index = point_lists.index(sorted_list[0])
		for ii in noise:
			# print('i=',i)
			if noise_index >= ii:
				noise_index = noise_index + 1
			else:
				break
		noise.append(noise_index)
		noise.sort()
		minn.append(find_index(i, j, noise_index, num))
		temp = energy_list.index(min(energy_list))
		del point_lists[temp]  # 删去定位噪声，剩下的邻域为下一次定位噪声做准备
		del list_rgb[temp]
		count = count - 1
	if (count == 0):
		# print("point_list", point_lists)
		least = least_energy(point_lists, list_rgb)
		rest_a.extend(least[3])
		rest_b.extend(least[4])
		# 噪声count不为0的情况
		if noise is not None:
			for ii in rest_a:
				for iii in noise:
					if ii >= iii:
						ii = ii + 1
				a.append(find_index(i, j, ii, num))
			for ii in rest_b:
				for iii in noise:
					if ii >= iii:
						ii = ii + 1
				b.append(find_index(i, j, ii, num))
		# 噪声count为0的情况
		else:
			a = rest_a
			b = rest_b
	return minn, a, b


# 通过三通道计算像素点的区分度的绝对值
def gradient_average_abs_rgb(gray, rgb, count, num=8):
	re = np.zeros((gray.shape[0], gray.shape[1]))
	for k in range(1, gray.shape[0] - 1):
		for l in range(1, gray.shape[1] - 1):
			noise, a, b = point_classification(gray, rgb, k, l, count, num=8)
			sum_a_0 = 0
			sum_a_1 = 0
			sum_a_2 = 0
			sum_b_0 = 0
			sum_b_1 = 0
			sum_b_2 = 0
			for i in a:
				sum_a_0 += rgb[i[0]][i[1]][0]
				sum_a_1 += rgb[i[0]][i[1]][1]
				sum_a_2 += rgb[i[0]][i[1]][2]
			for i in b:
				sum_b_0 += rgb[i[0]][i[1]][0]
				sum_b_1 += rgb[i[0]][i[1]][1]
				sum_b_2 += rgb[i[0]][i[1]][2]
			diffa = ((sum_a_0 / len(a) - sum_b_0 / len(b)) + (sum_a_1 / len(a) - sum_b_1 / len(b)) + (
					sum_a_2 / len(a) - sum_b_2 / len(b))) / 3
			diffb = -((sum_a_0 / len(a) - sum_b_0 / len(b)) + (sum_a_1 / len(a) - sum_b_1 / len(b)) + (
					sum_a_2 / len(a) - sum_b_2 / len(b))) / 3
			re[k, l] = abs(int(diffa))
	return re


# 通过三通道计算像素点的区分度的绝对值
def gradient_average_rgb(gray, rgb, count, num=8):
	re = np.zeros((gray.shape[0], gray.shape[1]))
	for k in range(1, gray.shape[0] - 1):
		for l in range(1, gray.shape[1] - 1):
			noise, a, b = point_classification(gray, rgb, k, l, count, num=8)
			gray_a = 0
			gray_b = 0
			sum_a_0 = 0
			sum_a_1 = 0
			sum_a_2 = 0
			sum_b_0 = 0
			sum_b_1 = 0
			sum_b_2 = 0
			for i in a:
				gray_a += gray[i[0]][i[1]]
				sum_a_0 += rgb[i[0]][i[1]][0]
				sum_a_1 += rgb[i[0]][i[1]][1]
				sum_a_2 += rgb[i[0]][i[1]][2]
			for i in b:
				gray_b += gray[i[0]][i[1]]
				sum_b_0 += rgb[i[0]][i[1]][0]
				sum_b_1 += rgb[i[0]][i[1]][1]
				sum_b_2 += rgb[i[0]][i[1]][2]
			diffa = ((sum_a_0 / len(a) - sum_b_0 / len(b)) + (sum_a_1 / len(a) - sum_b_1 / len(b)) + (
					sum_a_2 / len(a) - sum_b_2 / len(b))) / 3
			if abs(gray_a / len(a) - gray[k, l]) < abs(gray_b / len(b) - gray[k, l]):
				if gray_a / len(a) >= gray_b / len(b):
					re[k, l] = abs(int(diffa))
				else:
					re[k, l] = -abs(int(diffa))
			if abs(gray_a / len(a) - gray[k, l]) > abs(gray_b / len(b) - gray[k, l]):
				if gray_a / len(a) >= gray_b / len(b):
					re[k, l] = -abs(int(diffa))
				else:
					re[k, l] = abs(int(diffa))
	# re[k, l] = abs(int(diffa))
	return re


####################################################################
####################################################################10.19

# 遍历灰度矩阵并计数标记，噪声点+0，内部点+1，小边点+10，大边点+100,num为邻域个数,count为每次取噪声个数
def score(gray, rgb, count, num=8):
	th = 10
	scores = np.zeros((gray.shape[0], gray.shape[1]))  # 初始化为0
	total_noise = []
	#     mark = [[[[]]*3]*width]*length
	#     print(gray.shape[0])
	for k in range(1, gray.shape[0] - 1):
		for l in range(1, gray.shape[1] - 1):
			#             print(i)
			noise, a, b = point_classification(gray, rgb, k, l, count, num)  # 根据中心像素点得到八邻域中的噪声，a,b区坐标
			#             print(a,b)
			total_noise.extend(noise)
			#             print(noise,a,b)
			num_a = []
			num_b = []
			for i in a:
				num_a.append(gray[i[0]][i[1]])
			for i in b:
				num_b.append(gray[i[0]][i[1]])
			#             print(num_a,num_b)
			#             if((len(num_b) == 0)|(len(num_a) == 0)):
			#                 print('AAAAAAAAA',k,l)
			# #                 gray[k][l] = 0
			# #                 continue
			#             print(num_a,num_b)
			#             print(type(a),type(max(num_a)),num_a ,num_b,type(int(max(num_a)-min(num_b))))
			if ((min(num_a) > max(num_b)) & (max(num_a) - min(num_b) > th)):  # a区的点设为大边点, b区为小边点, 5为假设！！！！！！！！！！！！！！！！！
				for i in a:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 100
				#                     mark[k][l][0].append(i)
				for i in b:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 10
			#                     mark[k][l][1].append(i)
			elif ((min(num_b) > max(num_a)) & (max(num_b) - min(num_a) > th)):  # b区的点设为大边点，a区为小边点
				for i in a:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 10
				#                     mark[k][l][1].append(i)
				for i in b:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 100
			#                     mark[k][l][0].append(i)
			elif (((min(num_a) >= max(num_b)) & (max(num_a) - min(num_b) <= th)) | (
					(min(num_b) >= max(num_a)) & (max(num_b) - min(num_a) <= th)) | (
					      (max(num_a) >= min(num_b)) & (min(num_b) >= min(num_a))) | (
					      (max(num_b) >= min(num_a)) & (min(num_a) >= min(num_b)))):  # a,b算内部点，
				for i in a:
					#                     print(scores[i[0]][i[1]])
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 1.0
				#                     mark[k][l][2].append(i)
				for i in b:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 1.0
		#                     mark[k][l][2].append(i)
	return scores, total_noise  # , mark


# 参数：灰度矩阵图,每次取噪声个数
# 得到：噪声矩阵，积分矩阵, 矛盾点二值矩阵,初始大边点二值矩阵,初始小边点二值矩阵
# 其中噪声矩阵是每个像素点被判断为噪声点的次数的矩阵
def noise_array(gray, rgb, ccount, th, num=8):
	#     count=0
	length = gray.shape[0]
	width = gray.shape[1]
	noise = np.zeros((length, width))  # 初始化为0

	start1 = time.clock()
	score_array_1 = score_new(gray, rgb, ccount, th, num)[0]  # 有值

	# np.savetxt("D:\\ score_array_1.csv", score_array_1, fmt="%d", delimiter=',')

	# end1 = time.clock()

	# print(str(end1 - start1))

	# start2 = time.clock()
	#     print(score_array_1)
	score_array_2 = np.zeros((length, width, 6))  # 全0
	contradiction_array = np.zeros((length, width))
	edge_big = np.zeros((length, width))
	inner = np.zeros((length, width))
	edge_small = np.zeros((length, width))
	for i in range(1, length - 1):
		for j in range(1, width - 1):
			#             print(i,j)
			score_array_2[i][j][0] = score_array_1[i][j] // 100  # [0, 0, 0]中第一个值 大边点
			score_array_2[i][j][1] = score_array_1[i][j] // 10 % 10  # 小边点
			score_array_2[i][j][2] = score_array_1[i][j] % 10  # 内部点
			score_array_2[i][j][5] = list(score_array_2[i][j]).index(max(score_array_2[i][j][0:3]))  # 三个系数哪个大，哪个做标记
			if (score_array_2[i][j][0] > 0) & (score_array_2[i][j][1] == 0):  # 大边点
				score_array_2[i][j][3] = 2
				edge_big[i][j] = 1
			if (score_array_2[i][j][1] > 0) & (score_array_2[i][j][0] == 0):  # 小边点
				score_array_2[i][j][3] = 1
				edge_small[i][j] = 1
			if (score_array_2[i][j][1] == 0) & (score_array_2[i][j][0] == 0):
				inner[i][j] = 1
			if score_array_2[i][j][0] * score_array_2[i][j][1] > 0:
				contradiction_array[i][j] = 1
				score_array_2[i][j][4] = 1  # 标记是否为矛盾点
			else:
				contradiction_array[i][j] = 0
			count_noise = num - score_array_2[i][j][0] - score_array_2[i][j][1] - score_array_2[i][j][2]
			noise[i][j] = count_noise
	#             if noise[i][j]<0:
	#                 count+=1
	#                 print( score_array_2[i][j])
	# end2 = time.clock()
	# print(str(end2 - start2))

	return noise, inner, contradiction_array, edge_big, edge_small  # ,count


# 遍历灰度矩阵并计数标记，噪声点+0，内部点+1，小边点+10，大边点+100,num为邻域个数,count为每次取噪声个数
def score_new(gray, rgb, count, th, num=8):
	# th = 5
	scores = np.zeros((gray.shape[0], gray.shape[1]))  # 初始化为0
	total_noise = []
	for k in range(1, gray.shape[0] - 1):
		for l in range(1, gray.shape[1] - 1):
			noise, a, b = point_classification(gray, rgb, k, l, count, num)  # 根据中心像素点得到八邻域中的噪声，a,b区坐标
			total_noise.extend(noise)
			num_a = []
			num_b = []
			sum_a_0 = 0
			sum_a_1 = 0
			sum_a_2 = 0
			sum_b_0 = 0
			sum_b_1 = 0
			sum_b_2 = 0
			for i in a:
				# num_a.append(gray[i[0]][i[1]])
				sumrgb = 0
				# for p in range(3):
				#     sumrgb+=rgb[i[0]][i[1]][p]
				sum_a_0 += rgb[i[0]][i[1]][0]
				sum_a_1 += rgb[i[0]][i[1]][1]
				sum_a_2 += rgb[i[0]][i[1]][2]
			# num_a.append(sumrgb)
			for i in b:
				# num_b.append(gray[i[0]][i[1]])
				sumrgb = 0
				# for p in range(3):
				#     sumrgb += rgb[i[0]][i[1]][p]
				# num_b.append(sumrgb)
				sum_b_0 += rgb[i[0]][i[1]][0]
				sum_b_1 += rgb[i[0]][i[1]][1]
				sum_b_2 += rgb[i[0]][i[1]][2]
			# avg_a = sum(num_a) / len(num_a)
			# avg_b = sum(num_b) / len(num_b)
			# avg_a = avg_a/3
			# avg_b = avg_b/3
			# diff = (abs(sum_a_0-sum_b_0)+abs(sum_a_1-sum_b_1)+abs(sum_a_2-sum_b_2))/3
			diffa = ((sum_a_0 / len(a) - sum_b_0 / len(b)) + (sum_a_1 / len(a) - sum_b_1 / len(b)) + (
					sum_a_2 / len(a) - sum_b_2 / len(b))) / 3
			diffb = -((sum_a_0 / len(a) - sum_b_0 / len(b)) + (sum_a_1 / len(a) - sum_b_1 / len(b)) + (
					sum_a_2 / len(a) - sum_b_2 / len(b))) / 3

			# if k == 16 and l == 8:
			#     for m in a:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     for m in b:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     print(avg_a, end=" ")
			#     print(avg_b, end=" ")
			#     print(avg_a - avg_b)
			#     print()
			#
			# if k == 16 and l == 9:
			#     for m in a:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     for m in b:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     print(avg_a, end=" ")
			#     print(avg_b, end=" ")
			#     print(avg_a - avg_b)
			#     print()
			#
			# if k == 16 and l == 10:
			#     for m in a:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     for m in b:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     print(avg_a, end=" ")
			#     print(avg_b, end=" ")
			#     print(avg_a - avg_b)
			#     print()
			#
			# if k == 17 and l == 8:
			#     for m in a:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     for m in b:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     print(avg_a, end=" ")
			#     print(avg_b, end=" ")
			#     print(avg_a - avg_b)
			#     print()
			#
			# if k == 17 and l == 10:
			#     for m in a:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     for m in b:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     print(avg_a, end=" ")
			#     print(avg_b, end=" ")
			#     print(avg_a - avg_b)
			#     print()
			#
			# if k == 18 and l == 8:
			#     for m in a:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     for m in b:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     print(avg_a, end=" ")
			#     print(avg_b, end=" ")
			#     print(avg_a - avg_b)
			#     print()
			#
			# if k == 18 and l == 9:
			#     for m in a:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     for m in b:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     print(avg_a, end=" ")
			#     print(avg_b, end=" ")
			#     print(avg_a - avg_b)
			#     print()
			#
			# if k == 18 and l == 10:
			#     for m in a:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     for m in b:
			#         print(gray[m[0]][m[1]], end=" ")
			#         print(m, end=" ")
			#     print()
			#     print(avg_a, end=" ")
			#     print(avg_b, end=" ")
			#     print(avg_a - avg_b)
			#     print()

			# if (min(num_a) >= max(num_b)) and (abs(avg_a - avg_b) > th):  # a区的点设为大边点, b区为小边点, 5为假设！！！！！！！！！！！！！！！！！
			# if avg_a - avg_b > th:  # a区的点设为大边点, b区为小边点, 5为假设！！！！！！！！！！！！！！！！！
			if diffa > th:  # a区的点设为大边点, b区为小边点, 5为假设！！！！！！！！！！！！！！！！！
				for i in a:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 100
					if i[0] == 17 and i[1] == 9:
						print("大")
				for i in b:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 10
					if i[0] == 17 and i[1] == 9:
						print("小")
			# if (min(num_b) >= max(num_a)) and (abs(avg_b - avg_a) > th):  # b区的点设为大边点，a区为小边点
			# elif avg_b - avg_a > th:  # b区的点设为大边点，a区为小边点
			elif diffb > th:  # b区的点设为大边点，a区为小边点
				for i in a:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 10
					if i[0] == 17 and i[1] == 9:
						print("小")
				for i in b:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 100
					if i[0] == 17 and i[1] == 9:
						print("大")
			# elif (((min(num_a) >= max(num_b)) and (abs(avg_a - avg_b) <= th)) | (
			#         (min(num_b) >= max(num_a)) and (abs(avg_b - avg_a) <= th)) | (
			#         (max(num_a) >= min(num_b)) and (min(num_b) >= min(num_a))) | (
			#         (max(num_b) >= min(num_a)) and (min(num_a) >= min(num_b)))):  # a,b算内部点，
			else:
				for i in a:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 1.0
				for i in b:
					scores[i[0]][i[1]] = scores[i[0]][i[1]] + 1.0
	return scores, total_noise
