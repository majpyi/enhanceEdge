import matplotlib.pyplot as plt

import modify
import numpy as np
import cv2

import sys

sys.setrecursionlimit(100000)

# gray = np.array([[10, 10, 10, 10], [10, 10, 11, 10], [10, 12, 5, 10], [10, 10, 10, 10]])
# gray = np.array([[87, 87, 87], [87, 87, 87], [87, 87, 85]])
gray = np.array([[100, 100, 100], [80, 80, 80], [80, 110, 80]])
gray1 = np.array([[80, 80, 80], [80, 80, 80], [80, 110, 80]])


def method_name(gray):
    a, b, c = modify.point_classification_new(gray, 1, 1, 1)
    for x in range(len(a)):
        print(gray[a[x][0], a[x][1]], end=" ")
        print(a[x], end=" ")
    print()
    for x in range(len(b)):
        print(gray[b[x][0], b[x][1]], end=" ")
        print(b[x], end=" ")
    print()
    for x in range(len(c)):
        print(gray[c[x][0], c[x][1]], end=" ")
        print(c[x], end=" ")
    print()


# 将list转换为map的函数
def listtomap(li):
    mp = {}
    for i in range(len(li)):
        mp[((li[i][0][0][0], li[i][0][0][1]), (li[i][0][1][0], li[i][0][1][1]))] = li[i][1]
    return mp


xx = [-1, -1, -1, 0, +1, +1, +1, 0]
yy = [+1, 0, -1, -1, -1, 0, +1, +1]

xxx = [-1, -1, -1, 0, +1, +1, +1, 0, -1, -1, -1, 0, +1, +1, +1, 0]
yyy = [+1, 0, -1, -1, -1, 0, +1, +1, +1, 0, -1, -1, -1, 0, +1, +1]


# 进行噪声的修复
def fix_noise(gray, i, j, x, y):
    for k in range(len(xx)):
        if x == i + xxx[k] and y == j + yyy[k]:
            if abs(gray[i + xxx[k + 1], j + yyy[k + 1]] - gray[x, y]) > abs(
                    gray[i + xxx[k - 1], j + yyy[k - 1]] - gray[x, y]):
                gray[x, y] = gray[i + xxx[k - 1], j + yyy[k - 1]]
            else:
                gray[x, y] = gray[i + xxx[k + 1], j + yyy[k + 1]]


# 区域分割的函数
# rgb三通道作为能量函数计算,
# 找到边能量最大的两个边,对该边进行记录
# 设置有两个阈值,分别为大小阈值,大于大阈值的存入一个数组,在大小阈值之间的放入另一个数组
def cut(gray, th, th2, rgb):
    re = []  # 存储符合条件的八邻域分割点
    re_weak = []
    noise_num = 0
    noise_pos = np.zeros((gray.shape[0], gray.shape[1]))
    for i in range(1, gray.shape[0] - 1):
        for j in range(1, gray.shape[1] - 1):
            mul_list = {}  # 存储每个边的能量值与坐标信息
            poit = {}  # 存储每个点的能量值与坐标信息
            for k in range(len(xx)):
                poit[(i + xx[k], j + yy[k])] = gray[i + xx[k], j + yy[k]]
                # if i == 1 and j == 1:
                #     # print(i + xx[k], j + yy[k])
                #     # print(i + xx[k - 1], j + yy[k - 1])
                # print(type(gray[i + xx[k], j + yy[k]]))
                # print(type(gray[i + xx[k - 1], j + yy[k - 1]]))
                #     # print((gray[i + xx[k], j + yy[k]] - gray[i + xx[k - 1], j + yy[k - 1]]))
                #     print(int(gray[i + xx[k], j + yy[k]]) - int(gray[i + xx[k - 1], j + yy[k - 1]]))
                mul_list[((i + xx[k], j + yy[k]), (i + xx[k - 1], j + yy[k - 1]))] = pow(
                    int(rgb[i + xx[k], j + yy[k], 0]) - int(rgb[i + xx[k - 1], j + yy[k - 1], 0]), 2) + pow(
                    int(rgb[i + xx[k], j + yy[k], 1]) - int(rgb[i + xx[k - 1], j + yy[k - 1], 1]), 2) + pow(
                    int(rgb[i + xx[k], j + yy[k], 2]) - int(rgb[i + xx[k - 1], j + yy[k - 1], 2]), 2)

            noise, a, b = modify.point_classification_new(gray, i, j, 1)  # 找到八邻域中的一个噪声点,后续判断噪声点是否影响分割点
            noise_pos[noise[0][0], noise[0][1]] = 1

            sum_a = 0
            num_a = 0
            sum_b = 0
            num_b = 0
            raws = gray
            point_a = []
            point_b = []
            for k in range(len(a)):
                sum_a += raws[a[k][0], a[k][1]]
                num_a += 1
                point_a.append(raws[a[k][0], a[k][1]])

            for k in range(len(b)):
                sum_b += raws[b[k][0], b[k][1]]
                num_b += 1
                point_b.append(raws[b[k][0], b[k][1]])

            maxa = max(point_a)  # 两个区域的的四个极值
            maxb = max(point_b)
            mina = min(point_a)
            minb = min(point_b)
            # if (maxa >= maxb and mina <= maxb):
            #     re[i, j] = 0
            # elif (maxb >= maxa and minb <= maxa):
            #     re[i, j] = 0

            # print(mul_list)
            # 将每条边的能量进行排序,得到能量最大的两条边为索引1和0,   但是得到的数据类型是列表
            mul_list = sorted(mul_list.items(), key=lambda item: item[1], reverse=True)
            # print(mul_list)

            # print(type(mul_list))

            # mina = min(mul_list[0][0][0][0], mul_list[1][0][0][0])
            # minb = min(mul_list[0][0][0][1], mul_list[1][0][0][1])

            # x1 = (mul_list[0][0][0][0], mul_list[0][0][0][1])
            # x2 = (mul_list[1][0][0][0], mul_list[1][0][0][1])
            n1 = mul_list[0][0]  # 两个含有噪声点的边的坐标信息(不一定含有噪声,只是能量边最大)
            n2 = mul_list[1][0]

            # if i == 1 and j == 1:
            #     print(mul_list)
            #     print(a)
            #     print(b)
            # print(n1)
            # print(n2)

            # print(gray[a, b])
            # del (poit[(a, b)])  # 删除是噪声点那个点
            # print(poit)

            noise_po, po1, po2 = find_(n1, n2)
            # print(noise_po)
            # print(po1)
            # print(po2)

            # if(a1[0][0]==a and a1[0][1]== b):
            # if noise[0] == (mina, minb):  # 判断噪声点影响了八邻域分隔

            if po1 != 0 and noise_po == noise[0]:
                noise_num += 1

                # while po1 != 0 and noise_po == noise[0]:
                #     fix_noise(gray, i, j, noise[0][0], noise[0][1])
                #     noise, a, b = modify.point_classification_new(gray, i, j, 1)  # 找到八邻域中的一个噪声点,后续判断噪声点是否影响分割点
                #     mul_list = {}
                #     for k in range(len(xx)):
                #         mul_list[((i + xx[k], j + yy[k]), (i + xx[k - 1], j + yy[k - 1]))] = (
                #             pow((gray[i + xx[k], j + yy[k]] - gray[i + xx[k - 1], j + yy[k - 1]]), 2))
                #     mul_list = sorted(mul_list.items(), key=lambda item: item[1], reverse=True)
                #     n1 = mul_list[0][0]  # 两个含有噪声点的边的坐标信息(不一定含有噪声,只是能量边最大)
                #     n2 = mul_list[1][0]
                #     noise_po, po1, po2 = find_(n1, n2)
                #     print("while")
                # print("fix")

                if mina > maxb or minb > maxa:
                    if abs((sum_a / num_a) - (sum_b / num_b)) > th:
                        # continue
                        re.append(n1)  # 如果噪声对八邻域分隔没有影响,那么把认为分割正确的两个点加入进去,两个tuple,一共四个坐标
                        re.append(n2)
                    elif th >= abs((sum_a / num_a) - (sum_b / num_b)) >= th2:
                        re_weak.append(n1)  # 如果噪声对八邻域分隔没有影响,那么把认为分割正确的两个点加入进去,两个tuple,一共四个坐标
                        re_weak.append(n2)

                # r1 = mul_list[0][0]
                # del mul_list[0]  # 删除最大能量的两条边
                # r2 = mul_list[0][0]
                # del mul_list[0]
                #
                #
                # m1, m2, m3 = find_(r1, r2)
                #
                # mul_list = listtomap(mul_list)  # 把相应的列表重新转为map类型
                #
                # mul_list[((m2), (m3))] = pow((gray[m2[0]][m2[1]] - gray[m3[0]][m3[1]]), 2)  # 去掉一个噪声点之后的边的能量加入进去

                # re.append(n1)  # 如果噪声对八邻域分隔没有影响,那么把认为分割正确的两个点加入进去,两个tuple,一共四个坐标
                # re.append(n2)


            else:
                if mina > maxb or minb > maxa:
                    if abs((sum_a / num_a) - (sum_b / num_b)) > th:
                        # continue
                        re.append(n1)  # 如果噪声对八邻域分隔没有影响,那么把认为分割正确的两个点加入进去,两个tuple,一共四个坐标
                        re.append(n2)
                    elif th >= abs((sum_a / num_a) - (sum_b / num_b)) >= th2:
                        re_weak.append(n1)  # 如果噪声对八邻域分隔没有影响,那么把认为分割正确的两个点加入进去,两个tuple,一共四个坐标
                        re_weak.append(n2)
    # print(noise_num)
    return re, re_weak, noise_pos


# 含有噪声点的两条边,共有三个点组成
# 如果返回 0 0 0 则表示两条边不相邻,也就是噪声不影响原始的区域分割点
def find_(x, y):  # 输入含有噪声的两条边的信息,返回第一个噪声点,和另外的两个点的信息
    x1 = x[0]
    x2 = x[1]
    y1 = y[0]
    y2 = y[1]
    if x1 == y1:
        return x1, x2, y2
    if x1 == y2:
        return x1, x2, y1
    if x2 == y1:
        return x2, x1, y2
    if x2 == y2:
        return x2, x1, y1
    else:
        return 0, 0, 0


# method_name(gray1)

# cut(gray1)

# src = "41004"
# inpath = "D:\\experiment\\pic\\q\\"
# outpath = "D:\\out\\"
#
# raw = cv2.imread(inpath + src + ".jpg")
# raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
#
# raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
# raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
#
# # re = []
# re = cut(raw2_Filter)
# print(re)
# plt_cs.point_show(raw2_Filter, re)
# print(gray.shape[0])
# print(gray.shape[1])
# print(xx[-2])
# a = [1, 2, 3]
# print(a)
# del a[0]
# print(a)


# b = (1,2,3)
# del b[1]
# print(b)

# 遍历二维数组,查找延伸的起始点,进行延伸处理
def find_weak(min_point, show):
    x = []
    y = []
    for i in range(min_point.shape[0]):
        for j in range(min_point.shape[1]):
            if min_point[i, j] == 2:  # 四邻域范围内存在明显的区域分割点
                if i % 2 == 0 and j % 2 != 0:  # 区域的分割点在行上
                    print((i / 2, j / 2))
                    # print("1,3")
                    find_next(i / 2, j / 2, 1, show, x, y)
                    find_next(i / 2, j / 2, 3, show, x, y)
                    # find_next(i / 2, (j-1) / 2, 0, show, x, y)
                    # find_next(i / 2, (j-1) / 2, 2, show, x, y)
                    # find_next(i / 2, j / 2, 0, show, x, y)
                    # find_next(i / 2, j / 2, 2, show, x, y)
                elif i % 2 != 0 and j % 2 == 0:  # 区域的分割点在列上
                    print((i / 2, j / 2))
                    # print("0,2")
                    find_next(i / 2, j / 2, 0, show, x, y)
                    find_next(i / 2, j / 2, 2, show, x, y)
                    # find_next((i-1) / 2, j / 2, 1, show, x, y)
                    # find_next((i-1) / 2, j / 2, 3, show, x, y)
                    # find_next(i / 2, j / 2, 1, show, x, y)
                    # find_next(i / 2, j / 2, 3, show, x, y)
    return x, y


# 开始延伸处理
# 横纵坐标i,j  n 当前四邻域的边的序号(i,j所在边的序号)
def find_next(i, j, n, show, x, y):
    print("find")
    next = []  # 四邻域中四个中点的数值
    point = []  # 四邻域的四个中点的坐标
    next_point = []  # 下一个邻域的边的索引编号
    if i < 0.5 or i > (show.shape[0]) / 2 - 1.5:
        return
    if j < 0.5 or j > (show.shape[1]) / 2 - 1.5:
        return
    if n == 0:
        next.append(-1)
        next.append(show[int((i - 0.5) * 2), int((j - 0.5) * 2)])
        next.append(show[int(i * 2), int((j - 1) * 2)])
        next.append(show[int((i + 0.5) * 2), int((j - 0.5) * 2)])
        point.append((-1, -1))
        point.append(((i - 0.5), (j - 0.5)))
        point.append((i, j - 1))
        point.append(((i + 0.5), (j - 0.5)))
        next_point = [-1, 3, 0, 1]
    if n == 1:
        next.append(show[int((i + 0.5) * 2), int((j + 0.5) * 2)])
        next.append(-1)
        next.append(show[int((i + 0.5) * 2), int((j - 0.5) * 2)])
        next.append(show[int((i + 1) * 2), int(j * 2)])
        point.append(((i + 0.5), (j + 0.5)))
        point.append((-1, -1))
        point.append(((i + 0.5), (j - 0.5)))
        point.append(((i + 1), j))
        next_point = [2, -1, 0, 1]
    if n == 2:
        next.append(show[int(i * 2), int((j + 1) * 2)])
        next.append(show[int((i - 0.5) * 2), int((j + 0.5) * 2)])
        next.append(-1)
        next.append(show[int((i + 0.5) * 2), int((j + 0.5) * 2)])
        point.append((i, (j + 1)))
        point.append(((i - 0.5), (j + 0.5)))
        point.append((-1, -1))
        point.append(((i + 0.5), (j + 0.5)))
        next_point = [2, 3, -1, 1]
    if n == 3:
        next.append(show[int((i - 0.5) * 2), int((j + 0.5) * 2)])
        next.append(show[int((i - 1) * 2), int(j * 2)])
        next.append(show[int((i - 0.5) * 2), int((j - 0.5) * 2)])
        next.append(-1)
        point.append(((i - 0.5), (j + 0.5)))
        point.append(((i - 1), j))
        point.append(((i - 0.5), (j - 0.5)))
        point.append((-1, -1))
        next_point = [2, 3, 0, -1]
    flag = 0
    print(next)
    for k in range(4):
        if next[k] == 2 or next[k] == 3:
            print("2222")
            flag = 1
            return
    for k in range(4):
        if next[k] == 1 and flag == 0:
            print("11111")
            x.append(point[k][0])
            y.append(point[k][1])
            show[int(point[k][0] * 2), int(point[k][1] * 2)] = 3  # 延伸之后将标记进行修改
            find_next(point[k][0], point[k][1], next_point[k], show, x, y)


# cut(gray,1,1)


def show_cut(gray, th, th2, rgb, i, j):
    re = []  # 存储符合条件的八邻域分割点
    re_weak = []
    noise_num = 0
    noise_pos = np.zeros((gray.shape[0], gray.shape[1]))
    # for i in range(1, gray.shape[0] - 1):
    #     for j in range(1, gray.shape[1] - 1):
    mul_list = {}  # 存储每个边的能量值与坐标信息
    poit = {}  # 存储每个点的能量值与坐标信息
    for k in range(len(xx)):
        poit[(i + xx[k], j + yy[k])] = gray[i + xx[k], j + yy[k]]
        # if i == 1 and j == 1:
        #     # print(i + xx[k], j + yy[k])
        #     # print(i + xx[k - 1], j + yy[k - 1])
        # print(type(gray[i + xx[k], j + yy[k]]))
        # print(type(gray[i + xx[k - 1], j + yy[k - 1]]))
        #     # print((gray[i + xx[k], j + yy[k]] - gray[i + xx[k - 1], j + yy[k - 1]]))
        #     print(int(gray[i + xx[k], j + yy[k]]) - int(gray[i + xx[k - 1], j + yy[k - 1]]))
        mul_list[((i + xx[k], j + yy[k]), (i + xx[k - 1], j + yy[k - 1]))] = pow(
            int(rgb[i + xx[k], j + yy[k], 0]) - int(rgb[i + xx[k - 1], j + yy[k - 1], 0]), 2) + pow(
            int(rgb[i + xx[k], j + yy[k], 1]) - int(rgb[i + xx[k - 1], j + yy[k - 1], 1]), 2) + pow(
            int(rgb[i + xx[k], j + yy[k], 2]) - int(rgb[i + xx[k - 1], j + yy[k - 1], 2]), 2)

    noise, a, b = modify.point_classification_new(gray, i, j, 1)  # 找到八邻域中的一个噪声点,后续判断噪声点是否影响分割点
    noise_pos[noise[0][0], noise[0][1]] = 1

    sum_a = 0
    num_a = 0
    sum_b = 0
    num_b = 0
    raws = gray
    point_a = []
    point_b = []
    for k in range(len(a)):
        sum_a += raws[a[k][0], a[k][1]]
        num_a += 1
        point_a.append(raws[a[k][0], a[k][1]])

    for k in range(len(b)):
        sum_b += raws[b[k][0], b[k][1]]
        num_b += 1
        point_b.append(raws[b[k][0], b[k][1]])

    maxa = max(point_a)  # 两个区域的的四个极值
    maxb = max(point_b)
    mina = min(point_a)
    minb = min(point_b)
    # if (maxa >= maxb and mina <= maxb):
    #     re[i, j] = 0
    # elif (maxb >= maxa and minb <= maxa):
    #     re[i, j] = 0

    # print(mul_list)
    # 将每条边的能量进行排序,得到能量最大的两条边为索引1和0,   但是得到的数据类型是列表
    mul_list = sorted(mul_list.items(), key=lambda item: item[1], reverse=True)
    # print(mul_list)

    # print(type(mul_list))

    # mina = min(mul_list[0][0][0][0], mul_list[1][0][0][0])
    # minb = min(mul_list[0][0][0][1], mul_list[1][0][0][1])

    # x1 = (mul_list[0][0][0][0], mul_list[0][0][0][1])
    # x2 = (mul_list[1][0][0][0], mul_list[1][0][0][1])
    n1 = mul_list[0][0]  # 两个含有噪声点的边的坐标信息(不一定含有噪声,只是能量边最大)
    n2 = mul_list[1][0]
    print(n1,end="")
    print(n2)
    # print("noise",end="")
    # print(noise,end="  ")
    # print(gray[noise[0][0],noise[0][1]])




def fix_transition(gray, x, y):
    sum_tr = 0
    for i in range(x, x + 5):
        for j in range(y, y + 5):
            sum_tr+=gray[i,j]
    avg = sum_tr/25
    low_tr = 0
    low_low = 255
    high_tr = 0
    high_high = 0
    for i in range(x, x + 5):
        for j in range(y, y + 5):
            if gray[i,j] < avg:
                low_tr+=1
                if gray[i,j] < low_low:
                    low_low = gray[i,j]
            if gray[i,j] > avg:
                high_tr+=1
                if gray[i,j] >high_high:
                    high_high = gray[i,j]
    if low_tr>=8 and high_tr>=8 :
        for i in range(x, x + 5):
            for j in range(y, y + 5):
                if gray[i,j] > avg:
                    gray[i,j] = avg
                else:
                    gray[i,j] = avg


def merge_tag(tag1,tag2):
    for i in range(tag1.shape[0]):
        for j in range(tag1.shape[1]):
            if tag1[i,j]==1:
                tag2[i,j]=1
    return tag2

# xx_t = [-1, -1, -1, 0, +1, +1, +1, 0,0]
# yy_t = [+1, 0, -1, -1, -1, 0, +1, +1,0]
def transition_verify(gray,i,j):
    ls_pixel = []
    ls_pixel.append(gray[i,j])
    for k in range(len(xx)):
        ls_pixel.append(gray[i+xx[k],j+yy[k]])
    sorted(ls_pixel)
    ls_pixel.sort()
    print(ls_pixel)
