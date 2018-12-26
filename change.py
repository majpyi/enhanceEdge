import cv2
from M import *
import modify
from numpy import *
import numpy as np
import cv2
import matplotlib.pyplot as plt
# from PIL import Image
from pylab import *

#  原始中心点左侧的六个点,和他的上下两个点一共八个点
nx = [-1, -1, -1, 0, 0, +1, +1, +1]
ny = [-2, -1, 0, -2, -1, -2, -1, 0]


# 处理过程,每当遇到被标记为矛盾的点就进行处理修正.
# 取其中的两块区域中的最大值与最小值,然后按照与哪个最接近进行分类处理
# 最后判断矛盾点的值与哪个值就接近就把值赋给他
def change(raw2, i, j, tagp):
    pos = 0
    min = 256
    max = -1
    minSum = 0
    maxSum = 0
    minNum = 0
    maxNum = 0
    for m in range(8):
        if tagp[i + nx[m], j + ny[m]] == 0:
            if (raw2[i + nx[m], j + ny[m]] > max):
                max = raw2[i + nx[m], j + ny[m]]
            if (raw2[i + nx[m], j + ny[m]] < min):
                min = raw2[i + nx[m], j + ny[m]]
    for m in range(8):
        if tagp[i + nx[m], j + ny[m]] == 0:
            if (abs(raw2[i + nx[m], j + ny[m]] - max) >= abs(raw2[i + nx[m], j + ny[m]] - min)):
                minSum += raw2[i + nx[m], j + ny[m]]
                minNum += 1
            if (abs(raw2[i + nx[m], j + ny[m]] - max) < abs(raw2[i + nx[m], j + ny[m]] - min)):
                maxSum += raw2[i + nx[m], j + ny[m]]
                maxNum += 1
    if (minNum == 0 and maxNum != 0):
        raw2[i, j] = maxSum / maxNum
        tagp[i, j] = 0
    if (maxNum == 0 and minNum != 0):
        raw2[i, j] = minSum / minNum
        tagp[i, j] = 0

    if (minNum != 0 and maxNum != 0):
        if (abs(raw2[i, j] - max) > abs(raw2[i, j] - min)):
            raw2[i, j] = minSum / minNum
            tagp[i, j] = 0
        else:
            raw2[i, j] = maxSum / maxNum
            tagp[i, j] = 0


#  测试输出change 函数的是否正确
def changeTest(raw2, i, j, tagp, test):
    pos = 0
    min = 256
    max = -1
    minSum = 0
    maxSum = 0
    minNum = 0
    maxNum = 0

    for m in range(8):
        print(raw2[i + nx[m], j + ny[m]])

    for m in range(8):
        if tagp[i + nx[m], j + ny[m]] == 0:
            if (raw2[i + nx[m], j + ny[m]] > max):
                max = raw2[i + nx[m], j + ny[m]]
            if (raw2[i + nx[m], j + ny[m]] < min):
                min = raw2[i + nx[m], j + ny[m]]
    for m in range(8):
        if (abs(raw2[i + nx[m], j + ny[m]] - max) >= abs(raw2[i + nx[m], j + ny[m]] - min)):
            minSum += raw2[i + nx[m], j + ny[m]]
            minNum += 1
        if (abs(raw2[i + nx[m], j + ny[m]] - max) < abs(raw2[i + nx[m], j + ny[m]] - min)):
            maxSum += raw2[i + nx[m], j + ny[m]]
            maxNum += 1
    if (minNum == 0):
        raw2[i, j] = maxSum / maxNum
    if (maxNum == 0):
        raw2[i, j] = minSum / minNum

    if (minNum != 0 and maxNum != 0):
        if (abs(raw2[i, j] - max) > abs(raw2[i, j] - min)):
            raw2[i, j] = minSum / minNum
            tagp[i, j] = 0
            print(raw2[i, j])
        else:
            raw2[i, j] = maxSum / maxNum
            tagp[i, j] = 0
            print(raw2[i, j])
    print(str(minSum) + "  " + str(minNum) + "  " + str(maxSum) + "  " + str(maxNum))


#  高权重区域代表上下左右四个像素值
hx = [-1, 0, 0, +1]
hy = [0, -1, +1, 0]
#  低权重区域代表区域的四个角
lx = [-1, -1, +1, +1]
ly = [-1, +1, -1, +1]


# 按照权重区域进行取值,如果发现权重比较多的区域有正确的值那么我们就取其为我买的修复值
# 否则取低权重部分的值
def change1(raw2, i, j, tagp):
    tag = 4
    min = 256
    for m in range(4):
        if tagp[i + hx[m], j + hy[m]] != 255:
            temp = abs(raw2[i + hx[m], j + hy[m]] - raw2[i, j])
            if temp < min:
                min = temp
                tag = m
    # if(tag==5):
    #     for m in range(4):
    #         if tagp[i + hx[m], j + hy[m]] != 255:
    #             temp = abs(raw2[i + hx[m], j + hy[m]] - raw2[i, j])
    #             if temp < min:
    #                 min = temp
    #                 tag = m

    # tag只能取到0到3,超过这个值说明周围没有合适的值
    if (tag < 4):
        raw2[i, j] = raw2[i + hx[tag], j + hy[tag]]
        tagp[i, j] = 0


# 进行从边界旋转,每次增加一行和一列,并处理行列不相等,多余的部分
def solve(raw2, tagp, n, end, tag, gotag):
    # gotag = 0
    for i in range(2, n - 1):
        for k in range(i):
            # print(raw2[i, k], end=" ")
            if tagp[i, k] == 255:
                change(raw2, i, k, tagp)
                gotag = 1
        for k in range(i):
            # print(raw2[k, i], end=" ")
            if tagp[k, i] == 255:
                change(raw2, k, i, tagp)
                gotag = 1
        # print(raw2[i, i])
        if tagp[i, i] == 255:
            change(raw2, i, i, tagp)
            gotag = 1

    # 去除多余的行或者列
    for j in range(n, end - 1):
        if tag == 0:
            for k in range(1, n - 1):
                if tagp[j, k] == 255:
                    change(raw2, j, k, tagp)
                    gotag = 1
                # print(raw2[j, k], end=" ")
        if tag == 1:
            for k in range(1, n - 1):
                if tagp[k, j] == 255:
                    change(raw2, k, j, tagp)
                    gotag = 1
                # print(raw2[k, j], end=" ")
    return gotag


# 简单的原始从左向右从上到下的遍历处理方式
def solve1(x, y, raw2, tagp, gotag):
    for i in range(x - 1):
        for j in range(y - 1):
            if tagp[i, j] == 255:
                change(raw2, i, j, tagp)
                gotag = 1

    return gotag


# 从右上角进行的逆时针循环
xx = [-1, -1, -1, 0, +1, +1, +1, 0, -1]
yy = [+1, 0, -1, -1, -1, 0, +1, +1, +1]


# 查找孤立的噪声点,对单个像素点的判断有一部简单判断与两部再次判断的方式
def findSingleNoise(raw2, a, b):
    # re = np.zeros(raw2.shape[0], raw2.shape[1])
    re = np.zeros((a, b))
    # re = raw2.copy()
    # for i in range(1, a - 1):
    #     for j in range(1, b - 1):
    for i in range(3, a - 3):
        for j in range(3, b - 3):
            pos = [0, 0, 0, 0, 0, 0, 0, 0]
            for m in range(8):
                pos[m] = abs(raw2[i + xx[m + 1], j + yy[m + 1]] - raw2[i + xx[m], j + yy[m]])
            pos1 = pos.copy()
            pos1.sort()
            post1 = pos.index(pos1[7])
            pos[pos.index(pos1[7])] = -1
            post2 = pos.index(pos1[6])
            # print(pos)
            # print(pos1)
            # print(post1)
            # print(post2)
            Threshold = 200
            if (abs(post1 - post2) == 1):
                # if( abs ( raw2[i + xx[post1], j + yy[post1] ] -  raw2[i + xx[post2], j + yy[post2] ]  ) >50 ):
                # if (pos1[7] > Threshold and pos1[6] > Threshold):
                if (isolated(raw2, i + xx[max(post1, post2)], j + yy[max(post1, post2)], re) == 1):
                    re[i + xx[max(post1, post2)], j + yy[max(post1, post2)]] = 255
            if (abs(post1 - post2) == 7):
                # if( abs ( raw2[i + xx[post1], j + yy[post1] ] -  raw2[i + xx[post2], j + yy[post2] ]  ) >30 ):
                # if (pos1[7] > Threshold and pos1[6] > Threshold):
                if (isolated(raw2, i + xx[0], j + yy[0], re) == 1):
                    re[i + xx[0], j + yy[0]] = 255
    return re


#  5x5  周围25邻域的坐标信息,包括中心点的坐标,用于进行高斯滤波的处理
gx = [-2, -2, -2, -2, -2, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, +1, +1, +1, +1, +1, +2, +2, +2, +2, +2]
gy = [-2, -1, 0, +1, +2, -2, -1, 0, +1, +2, -2, -1, 0, +1, +2, -2, -1, 0, +1, +2, -2, -1, 0, +1, +2]
weight = [1, 4, 7, 4, 1, 4, 16, 26, 16, 4, 7, 26, 41, 26, 7, 4, 16, 26, 16, 4, 1, 4, 7, 4, 1]


# 对特点坐标点的像素值进行高斯滤波处理
def gaussian(raw2, x, y, re):
    sumweight = 0
    for k in range(len(gx)):
        sumweight += (raw2[x + gx[k], y + gy[k]] * weight[k]) / 273
    # re[x, y] = sumweight / 273
    re[x, y] = sumweight


#  3*3 周围八邻域的坐标,不包括中心点
xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
yyy = [+1, 0, -1, -1, -1, 0, +1, +1]


# 判断是否是孤立的噪声点,比较周围的八个邻域点,如果是突出或者是凹陷就可能是噪声点,处理之后图像更加平滑
def isolated(raws, x, y, tagp):
    tag1 = 0
    tag2 = 0
    for m in range(len(xxx)):
        if (raws[x, y] > raws[x + xxx[m], y + yyy[m]]):
            tag1 += 1
        if (raws[x, y] < raws[x + xxx[m], y + yyy[m]]):
            tag2 += 1
    if (tag1 == 8 or tag2 == 8):
        tagp[x, y] = 255
        return 1
    return 0


# 原始递归处理方法,对非孤立噪声点是用高斯滤波进行处理
def map(raws, x, y, noise):
    re = raws.copy()
    # print(type(re))
    for i in range(5, x - 5):
        for j in range(5, y - 5):
            if (noise[i, j] != 255):
                gaussian(raws, i, j, re)
    return re


# 对孤立噪声点进行修复处理,把周围八邻域中没有标记为噪声的元素的平均值赋给它.
def singleNoisefix(raws, x, y, noise, re):
    sum = 0
    num = 0
    for i in range(8):
        if (noise[x + xxx[i], y + yyy[i]] == 0):
            sum += raws[x + xxx[i], y + yyy[i]]
            num += 1
    if (num != 0):
        re[x, y] = sum / num
    # print(type(re))


# 递归遍历剩余的孤立噪声点,进行单独处理
def fixSingleNoise(raws, x, y, noise):
    re = raws.copy()  # 忘记加()
    # print(type(re))
    for i in range(2, x - 1):
        for j in range(2, y - 1):
            if (noise[i, j] == 255):
                singleNoisefix(raws, i, j, noise, re)
    return re


# 在根据最小能量的方法去掉一个最大概率矛盾点的情况下,按照划分的两个区域中大区域的最小值与小区域的最大值的差作为区分度
def gradient(raws, x, y):
    re = raws.copy()
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            noise, a, b = modify.point_classification(raws, i, j, 1)
            # print(a)
            # print(b)
            point_a = []
            point_b = []
            for k in range(len(a)):
                # point_a.append(raws[i + a[k][0] - 1, j + a[k][1] - 1])
                point_a.append(raws[a[k][0] - 1, a[k][1] - 1])
            for k in range(len(b)):
                # point_b.append(raws[i + b[k][0] - 1, j + b[k][1] - 1])
                point_b.append(raws[b[k][0] - 1, b[k][1] - 1])

            maxa = max(point_a)
            maxb = max(point_b)
            mina = min(point_a)
            minb = min(point_b)
            if (mina > maxb):
                re[i, j] = mina - maxb
            elif (minb > maxa):
                re[i, j] = minb - maxa
            else:
                re[i, j] = 0
    return re


# 在根据最小能量的方法去掉一个最大概率矛盾点的情况下,再按照两个区域的均值差,得到区分度值
# 如果区域进行交叉那么就把像素点的过渡区的值改为0
def gradient_average(raws, x, y, noise_num):
    re = np.zeros((x, y))
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            noise, a, b = modify.point_classification_new(raws, i, j, noise_num)  # 在八邻域中找到一个矛盾点剩余部分划分为两个部分
            # print(b)
            point_a = []
            point_b = []

            sum_a = 0
            num_a = 0
            sum_b = 0
            num_b = 0
            min_a = 255  # 获取中心点离两个区间的的最近差值
            min_b = 255
            for k in range(len(a)):
                # point_a.append(raws[i + a[k][0] - 1, j + a[k][1] - 1])  //  这里使用的相对地址,但是前面的函数传入的是绝对地址
                point_a.append(raws[a[k][0], a[k][1]])
                # sum_a += raws[a[k][0] - 1, a[k][1] - 1]
                sum_a += raws[a[k][0], a[k][1]]
                num_a += 1

            for k in range(len(b)):
                # point_b.append(raws[i + b[k][0] - 1, j + b[k][1] - 1])
                point_b.append(raws[b[k][0], b[k][1]])
                # sum_b += raws[b[k][0] - 1, b[k][1] - 1]
                sum_b += raws[b[k][0], b[k][1]]
                num_b += 1
            maxa = max(point_a)  # 两个区域的的四个极值
            maxb = max(point_b)
            mina = min(point_a)
            minb = min(point_b)
            if (maxa >= maxb and mina <= maxb):
                re[i, j] = 0
            elif (maxb >= maxa and minb <= maxa):
                re[i, j] = 0
            else:
                avg_a = sum_a / num_a
                avg_b = sum_b / num_b
                if (abs(raws[i, j] - avg_a) > abs(raws[i, j] - avg_b)):
                    # if (avg_a > avg_b):
                    re[i, j] = avg_b - avg_a
                    if (i == 87 and j == 205):
                        print(a)
                        print(avg_a)
                        print(b)
                        print(avg_b)
                # else:
                #     re[i,j] = avg_b - avg_a
                if (abs(raws[i, j] - avg_a) < abs(raws[i, j] - avg_b)):
                    # if (avg_a > avg_b):
                    re[i, j] = avg_a - avg_b
                    if (i == 87 and j == 205):
                        print(a)
                        print(avg_a)
                        print(b)
                        print(avg_b)
                # else:
                #     re[i,j] = avg_a - avg_b

            # for k in range(len(a)):
            #     temp = abs(raws[i, j] - raws[a[k][0] - 1, a[k][1] - 1])
            #     if (min_a > temp):
            #         min_a = temp
            # for k in range(len(b)):
            #     temp = abs(raws[i, j] - raws[b[k][0] - 1, b[k][1] - 1])
            #     if (min_b > temp):
            #         min_b = temp
            #
            # re[i, j] = abs(sum_a / num_a - sum_b / num_b)
            #
            # if (min_a > min_b):
            #     if (sum_a / num_a > sum_b / num_b):
            #         re[i, j] = -re[i, j]
            #     else:
            #         re[i, j] = re[i, j]
            # if (min_a < min_b):
            #     if (sum_a / num_a > sum_b / num_b):
            #         re[i, j] = re[i, j]
            #     else:
            #         re[i, j] = -re[i, j]
            # if( abs(sum_a / num_a - sum_b / num_b) >5):
            #     re[i, j] = abs(sum_a - sum_b)

            # re[i,j] = abs(avg_a-avg_b)
    return re


# 在根据最小能量的方法去掉一个最大概率矛盾点的情况下,再按照两个区域的均值差,得到区分度值
# 如论是否有区域交叉都会有一个区分度值
def gradient_average_new(raws, x, y, noise_num):
    re = np.zeros((x, y))
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            noise, a, b = modify.point_classification_new(raws, i, j, noise_num)  # 在八邻域中找到一个矛盾点剩余部分划分为两个部分
            # print(b)
            point_a = []
            point_b = []

            sum_a = 0
            num_a = 0
            sum_b = 0
            num_b = 0
            min_a = 255  # 获取中心点离两个区间的的最近差值
            min_b = 255
            for k in range(len(a)):
                # point_a.append(raws[i + a[k][0] - 1, j + a[k][1] - 1])  //  这里使用的相对地址,但是前面的函数传入的是绝对地址
                point_a.append(raws[a[k][0], a[k][1]])
                # sum_a += raws[a[k][0] - 1, a[k][1] - 1]
                sum_a += raws[a[k][0], a[k][1]]
                num_a += 1

            for k in range(len(b)):
                # point_b.append(raws[i + b[k][0] - 1, j + b[k][1] - 1])
                point_b.append(raws[b[k][0], b[k][1]])
                # sum_b += raws[b[k][0] - 1, b[k][1] - 1]
                sum_b += raws[b[k][0], b[k][1]]
                num_b += 1
            maxa = max(point_a)  # 两个区域的的四个极值
            maxb = max(point_b)
            mina = min(point_a)
            minb = min(point_b)
            if maxa >= maxb >= mina:
                avg_a = sum_a / num_a
                avg_b = sum_b / num_b
                if (abs(raws[i, j] - avg_a) > abs(raws[i, j] - avg_b)):
                    # if (avg_a > avg_b):
                    re[i, j] = avg_b - avg_a
                # else:
                #     re[i,j] = avg_b - avg_a
                if (abs(raws[i, j] - avg_a) < abs(raws[i, j] - avg_b)):
                    # if (avg_a > avg_b):
                    re[i, j] = avg_a - avg_b
            elif maxb >= maxa >= minb:
                avg_a = sum_a / num_a
                avg_b = sum_b / num_b
                if (abs(raws[i, j] - avg_a) > abs(raws[i, j] - avg_b)):
                    # if (avg_a > avg_b):
                    re[i, j] = avg_b - avg_a
                # else:
                #     re[i,j] = avg_b - avg_a
                if (abs(raws[i, j] - avg_a) < abs(raws[i, j] - avg_b)):
                    # if (avg_a > avg_b):
                    re[i, j] = avg_a - avg_b
            else:
                avg_a = sum_a / num_a
                avg_b = sum_b / num_b
                if (abs(raws[i, j] - avg_a) > abs(raws[i, j] - avg_b)):
                    # if (avg_a > avg_b):
                    re[i, j] = avg_b - avg_a
                # else:
                #     re[i,j] = avg_b - avg_a
                if (abs(raws[i, j] - avg_a) < abs(raws[i, j] - avg_b)):
                    # if (avg_a > avg_b):
                    re[i, j] = avg_a - avg_b
    return re


def gradient_average_abs(raws, x, y):
    re = np.zeros((x, y))
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            noise, a, b = modify.point_classification(raws, i, j, 2)
            # print(a)
            # print(b)
            # point_a = []
            # point_b = []

            sum_a = 0
            num_a = 0
            sum_b = 0
            num_b = 0
            min_a = 255
            min_b = 255
            for k in range(len(a)):
                # point_a.append(raws[i + a[k][0] - 1, j + a[k][1] - 1])
                # point_a.append(raws[a[k][0] - 1, a[k][1] - 1])
                # sum_a += raws[a[k][0] - 1, a[k][1] - 1]
                sum_a += raws[a[k][0], a[k][1]]
                num_a += 1

            for k in range(len(b)):
                # point_b.append(raws[i + b[k][0] - 1, j + b[k][1] - 1])
                # point_b.append(raws[b[k][0] - 1, b[k][1] - 1])
                # sum_b += raws[b[k][0] - 1, b[k][1] - 1]
                sum_b += raws[b[k][0], b[k][1]]
                num_b += 1
            re[i, j] = abs(sum_a / num_a - sum_b / num_b)
    return re


xx_tag = [-1, -1, -1, 0, +1, +1, +1, 0, 0]
yy_tag = [+1, 0, -1, -1, -1, 0, +1, +1, 0]


# 根据梯度值,只标记八邻域中区分度值最大的点,而且这个点的区分度值要大于一个阈值
def gradient_tag(raws, x, y):
    re = raws.copy()
    tag = np.zeros((x, y))
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            max_tag = []
            for k in range(9):
                max_tag.append(re[i + xx_tag[k], j + yy_tag[k]])
            for k in range(9):
                # if(re[i+xx_tag[k],j+yy_tag[k]]<max(max_tag)):
                # re[i + xx_tag[k], j + yy_tag[k]] = 0
                # else:
                if (re[i + xx_tag[k], j + yy_tag[k]] == max(max_tag) and max(max_tag) > 5):
                    re[i + xx_tag[k], j + yy_tag[k]] = 0
                    tag[i + xx_tag[k], j + yy_tag[k]] = 255
    return tag


# transition = 1
#
#
# def extend_edge(raws, th):
#     tag = np.zeros((raws.shape[0], raws.shape[1]))
#     for i in range(1, raws.shape[0] - 1):
#         for j in range(1, raws.shape[1] - 1):
#             if (raws[i, j] > th and tag[i, j] != transition):
#                 tag[i, j] = 255
#                 find_next_edge(raws, i, j, th, tag)
#     return tag
#
#
# def find_next_edge(raws, x, y, th, tag):
#     pos = []
#     extend = []
#     for k in range(8):
#         if (x == 0 or x == raws.shape[0] or y == 0 or y == raws.shape[1]):
#             return
#         pos.append(raws[x + xxx[k], y + yyy[k]])
#     for k in range(8):
#         if (x == 0 or x == raws.shape[0] or y == 0 or y == raws.shape[1]):
#             return
#         elif (raws[x + xxx[k], y + yyy[k]] == max(pos) and tag[x + xxx[k], y + yyy[k]] != 255):
#             extend.append(xxx[k])
#             extend.append(yyy[k])
#         elif (tag[x + xxx[k], y + yyy[k]] != 255):
#             tag[x + xxx[k], y + yyy[k]] = transition
#     if (len(extend) >= 2):
#         for l in range(len(extend), 2):
#             if (tag[x + extend[l], y + extend[l + 1]] != transition and raws[x + extend[l], y + extend[l + 1]] > th):
#                 tag[x + extend[l], y + extend[l + 1]] = 255
#                 find_next_edge(raws, x + extend[l], y + extend[l + 1], tag)


transition = 1


def extend_edge(raws, th):
    tag = np.zeros((raws.shape[0], raws.shape[1]))
    for i in range(1, raws.shape[0] - 1):
        for j in range(1, raws.shape[1] - 1):
            if (abs(raws[i, j]) > th and tag[i, j] != transition):
                tag[i, j] = 255
                find_next_edge(raws, i, j, th, tag)
    return tag


def find_next_edge(raws, x, y, th, tag):
    pos_positive = []
    pos_negative = []
    extend = []
    pos_x = 0
    pos_y = 0
    neg_x = 0
    neg_y = 0
    for k in range(8):
        if (x == 0 or x == raws.shape[0] or y == 0 or y == raws.shape[1]):
            return
        if (tag[x + xxx[k], y + yyy[k]] != transition):
            if (raws[x + xxx[k], y + yyy[k]] > 0):
                pos_positive.append(raws[x + xxx[k], y + yyy[k]])
            else:
                pos_negative.append(raws[x + xxx[k], y + yyy[k]])

    for k in range(8):
        if (x == 0 or x == raws.shape[0] or y == 0 or y == raws.shape[1]):
            return
        if (len(pos_positive) > 0 and raws[x + xxx[k], y + yyy[k]] == max(pos_positive)):
            pos_x = xxx[k]
            pos_y = yyy[k]
        elif (len(pos_negative) > 0 and raws[x + xxx[k], y + yyy[k]] == min(pos_negative)):
            neg_x = xxx[k]
            neg_y = yyy[k]
        # else:
        #     tag[x + xxx[k], y + yyy[k]] = transition

    if (abs(pos_x - neg_x) <= 1 and abs(pos_y - neg_y) <= 1):
        extend.append(pos_x)
        extend.append(pos_y)
        extend.append(neg_x)
        extend.append(neg_y)
    # else:
    #     tag[x + pos_x, y + pos_y] = transition
    #     tag[x + neg_x, y + neg_y] = transition

    if (len(extend) >= 2):
        for l in range(len(extend), 2):
            if (tag[x + extend[l], y + extend[l + 1]] != transition and abs(
                    raws[x + extend[l], y + extend[l + 1]]) > th):
                tag[x + extend[l], y + extend[l + 1]] = 255
                find_next_edge(raws, x + extend[l], y + extend[l + 1], tag)


# def extend_edge(raws, th):
#     tag = np.zeros((raws.shape[0], raws.shape[1]))
#
#     for x in range(1, raws.shape[0] - 1):
#         for y in range(1, raws.shape[1] - 1):
#
#             if(abs(raws[x,y]) > th):
#                 pos_positive = []
#                 pos_negative = []
#                 extend = []
#                 pos_x = 0
#                 pos_y = 0
#                 neg_x = 0
#                 neg_y = 0
#                 for k in range(8):
#                     if (x == 0 or x == raws.shape[0] or y == 0 or y == raws.shape[1]):
#                         return
#                     if (raws[x + xxx[k], y + yyy[k]] > 0 and):
#                         pos_positive.append(raws[x + xxx[k], y + yyy[k]])
#                     else:
#                         pos_negative.append(raws[x + xxx[k], y + yyy[k]])
#
#                 for k in range(8):
#                     if (x == 0 or x == raws.shape[0] or y == 0 or y == raws.shape[1]):
#                         return
#                     if (len(pos_positive) > 0 and raws[x + xxx[k], y + yyy[k]] == max(pos_positive)):
#                         pos_x = xxx[k]
#                         pos_y = yyy[k]
#                     elif (len(pos_negative) > 0 and raws[x + xxx[k], y + yyy[k]] == min(pos_negative)):
#                         neg_x = xxx[k]
#                         neg_y = yyy[k]
#                     else:
#                         tag[x + xxx[k], y + yyy[k]] = transition
#
#                 if (abs(pos_x - neg_x) <= 1 and abs(pos_y - neg_y) <= 1 and raws[x + pos_x, y + pos_y]>th and abs(raws[x + neg_x, y + neg_y]) > th ):
#                     extend.append(pos_x)
#                     extend.append(pos_y)
#                     extend.append(neg_x)
#                     extend.append(neg_y)
#                     tag[x + pos_x, y + pos_y] = 255
#                     tag[x + neg_x, y + neg_y] = 255
#                 else:
#                     tag[x + pos_x, y + pos_y] = transition
#                     tag[x + neg_x, y + neg_y] = transition
#     return  tag

marchX = [0, 0, 1, 1, 0]
marchY = [0, 1, 1, 0, 0]


def marching_squares(src):
    re = np.zeros((src.shape[0] * 2, src.shape[1] * 2))
    vector_re = []
    for x in range(src.shape[0] - 1):
        for y in range(src.shape[1] - 1):
            for k in range(len(marchX) - 1):
                if ((src[x + marchX[k], y + marchY[k]] * src[x + marchX[k + 1], y + marchY[k + 1]]) < 0):
                    vector_re.append(x + (marchX[k] + marchX[k + 1]) / 2)
                    vector_re.append(y + (marchY[k] + marchY[k + 1]) / 2)
                    re[2 * x + (marchX[k] + marchX[k + 1]), 2 * y + (marchY[k] + marchY[k + 1])] = 255
    return re, vector_re


def marching_filter(src, th):
    re = np.zeros((src.shape[0], src.shape[1]))
    for x in range(src.shape[0]):
        for y in range(src.shape[1]):
            if (abs(src[x, y]) > th):
                if (src[x, y] > 0):
                    re[x, y] = 1
                elif (src[x, y] < 0):
                    re[x, y] = -1
    return re


# xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
# yyy = [+1, 0, -1, -1, -1, 0, +1, +1]

# def isnext(a, b, src, tag):
#     if ((abs(a[0] - b[0]) + abs(a[1] - b[1])) == 1 and tag[a[0], a[1]] == 0 and tag[b[0], b[1]] == 0 and src[
#         a[0], a[1]] < 0 and src[b[0], b[1] ] > 0):
#         return True
#     else:
#         return False
#
#
# def extend_double1(x1, y1, x2, y2, src, tag):
#     if (x1 >= src.shape[0] - 2 or x1 <= 2 or x2 >= src.shape[0] - 2 or x2 <= 2):
#         return
#     if (y1 >= src.shape[1] - 2 or y1 <= 2 or y2 >= src.shape[1] - 2 or y2 <= 2):
#         return
#     min_x = min(x1, x2)
#     max_x = max(x1, x2)
#     min_y = min(y1, y2)
#     max_y = max(y1, y2)
#     list_4 = {}
#     for m in range(min_x - 1, max_x + 2):
#         if (tag[m, min_y] == 0):
#             list_4[(m, min_y)] = src[m, min_y]
#         if (tag[m, max_y] == 0):
#             list_4[(m, max_y)] = src[m, max_y]
#     for m in range(min_y - 1, max_y + 2):
#         if (tag[min_x, m] == 0):
#             list_4[(min_x, m)] = src[min_x, m]
#         if (tag[max_x, m] == 0):
#             list_4[(max_x, m)] = src[max_x, m]
#     # f = zip(list_4.values(), list_4.keys())
#     list1 = sorted(list_4.items(), key=lambda x: x[1])
#     sorted(list1)  # 从小到大进行排序
#     if (len(list1) >= 2 and isnext(list1[0][0], list1[len(list_4) - 1][0], src, tag) == True):
#         print(1)
#         tag[list1[0][0][0], list1[0][0][1]] = -1
#         tag[list1[len(list1) - 1][0][0], list1[len(list1) - 1][0][1]] = 1
#         extend_double1(list1[0][0][0], list1[0][0][1], list1[len(list1) - 1][0][0], list1[len(list1) - 1][0][1], src,
#                        tag)
#     else:
#         return
#
#
# def extend_double(tag, src):
#     for x in range(1, tag.shape[0] - 1):
#         for y in range(1, tag.shape[1] - 1):
#             if tag[x, y] > 0:
#                 for k in range(len(xxx)):
#                     if (tag[x + xxx[k], y + yyy[k]] < 0):
#                         extend_double1(x, y, x + xxx[k], y + yyy[k], src, tag)
#     return tag


# def isnext(a, b, src, tag):
#     if ((abs(a[0] - b[0]) + abs(a[1] - b[1])) == 1 and tag[a[0], a[1]] == 0 and tag[b[0], b[1]] == 0 and src[
#         a[0], a[1]] < 0 and src[b[0], b[1]] > 0):
#         return True
#     else:
#         return False
#
#
# def extend_double1(x1, y1, x2, y2, src, tag):
#     if (x1 > src.shape[0] - 2 or x1 < 1 or x2 > src.shape[0] - 2 or x2 < 1):
#         return
#     if (y1 > src.shape[1] - 2 or y1 < 1 or y2 > src.shape[1] - 2 or y2 < 1):
#         return
#     min_x = min(x1, x2)
#     max_x = max(x1, x2)
#     min_y = min(y1, y2)
#     max_y = max(y1, y2)
#     list_4 = {}
#     for m in range(min_x - 1, max_x + 2):
#         if (tag[m, min_y - 1] == 0):
#             list_4[(m, min_y - 1)] = src[m, min_y - 1]
#         if (tag[m, max_y + 1] == 0):
#             list_4[(m, max_y + 1)] = src[m, max_y + 1]
#     for m in range(min_y - 1, max_y + 2):
#         if (tag[min_x - 1, m] == 0):
#             list_4[(min_x - 1, m)] = src[min_x - 1, m]
#         if (tag[max_x, m] == 0):
#             list_4[(max_x + 1, m)] = src[max_x + 1, m]
#     # f = zip(list_4.values(), list_4.keys())
#     list1 = sorted(list_4.items(), key=lambda x: x[1])
#     sorted(list1)  # 从小到大进行排序
#     if (len(list1) >= 2 and isnext(list1[0][0], list1[len(list_4) - 1][0], src, tag) == True):
#         print(1)
#         tag[list1[0][0][0], list1[0][0][1]] = -1
#         tag[list1[len(list1) - 1][0][0], list1[len(list1) - 1][0][1]] = 1
#         extend_double1(list1[0][0][0], list1[0][0][1], list1[len(list1) - 1][0][0], list1[len(list1) - 1][0][1], src,
#                        tag)
#     else:
#         return
#
#
# def extend_double(tag, src):
#     for x in range(1, tag.shape[0] - 1):
#         for y in range(1, tag.shape[1] - 1):
#             if tag[x, y] > 0:
#                 for k in range(len(xxx)):
#                     if (tag[x + xxx[k], y + yyy[k]] < 0):
#                         extend_double1(x, y, x + xxx[k], y + yyy[k], src, tag)
#     return tag


def mid_point(num, ax, ay, bx, by, cx, cy, dx, dy):  # 0,1,2,3
    if num == 0:
        return ay, (ax + dx) / 2
    if num == 1:
        return (ay + by) / 2, ax
    if num == 2:
        return by, (bx + cx) / 2
    if num == 3:
        return (ay + by) / 2, dx


def squares_1(a, b, c, d, ax, ay, bx, by, cx, cy, dx, dy):
    # plt.rcParams['figure.figsize'] = (matrix.shape[0]/100,matrix.shape[1]/100)
    labels = [a, b, c, d]
    #     print(labels)
    mul_list = [0] * 4
    for i in range(4):
        mul_list[i] = labels[i - 1] * labels[i]  # 乘前一个
    #     print(mul_list)
    if mul_list.count(-1) < 2:
        return
    else:
        indexs = []  # 记录-1存在的index
        for j in range(len(mul_list)):
            if mul_list[j] == -1:
                indexs.append(j)
        #         print(indexs)
        if len(indexs) == 2:  # 中点不是2个就是4个
            mid_x1, mid_y1 = mid_point(indexs[0], ax, ay, bx, by, cx, cy, dx, dy)
            mid_x2, mid_y2 = mid_point(indexs[1], ax, ay, bx, by, cx, cy, dx, dy)
            x = [[mid_x1, mid_x2]]
            y = [[mid_y1, mid_y2]]
        else:  # 4个中点的情况
            mid_x1, mid_y1 = mid_point(indexs[0], ax, ay, bx, by, cx, cy, dx, dy)
            mid_x2, mid_y2 = mid_point(indexs[1], ax, ay, bx, by, cx, cy, dx, dy)
            mid_x3, mid_y3 = mid_point(indexs[2], ax, ay, bx, by, cx, cy, dx, dy)
            mid_x4, mid_y4 = mid_point(indexs[3], ax, ay, bx, by, cx, cy, dx, dy)
            x = [[mid_x1, mid_x2], [mid_x2, mid_x3], [mid_x3, mid_x4], [mid_x4, mid_x1]]
            y = [[mid_y1, mid_y2], [mid_y2, mid_y3], [mid_y3, mid_y4], [mid_y4, mid_y1]]
        #         print(x,y)
        for i in range(len(x)):
            plt.plot(x[i], y[i], color='black', lw=0.1)
            # plt.scatter(x[i], y[i], color='b')


def get_squares(matrix, x, y):  # 找到以该点为左上角点的四边形,参数：矩阵，坐标
    return matrix[x][y], matrix[x][y + 1], matrix[x + 1][y + 1], matrix[x + 1][
        y], x, y, x, y + 1, x + 1, y + 1, x + 1, y


def traverse(matrix):
    # plt.rcParams['figure.figsize'] = (matrix.shape[0]/100,matrix.shape[1]/100)
    w, h = matrix.shape
    for i in range(w - 1):
        for j in range(h - 1):
            a, b, c, d, ax, ay, bx, by, cx, cy, dx, dy = get_squares(matrix, i, j)
            #             print(a,b,c,d,ax,ay,bx,by,cx,cy,dx,dy)
            squares_1(a, b, c, d, ax, ay, bx, by, cx, cy, dx, dy)
    ax = plt.gca()
    ax.invert_yaxis()  # y轴反向
    # plt.grid()  # 生成网格
    plt.xlim(0, matrix.shape[1] - 1, 1)
    plt.ylim(matrix.shape[0] - 1, 0, 1)

    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    #     xs = [0, 5, 9, 10, 15]
    #     ys = [0, 1, 2, 3, 4]
    # plt.plot(xs, ys)
    # plt.xticks([x for x in range(max(xs) + 1) if x % 2 == 0])  # x标记step设置为2
    # plt.yticks([y for y in range(max(ys) + 1)])  # y标记step设置为1
    plt.savefig('D:\\plot123_2.png', dpi=500)  # 指定分辨率保存
    plt.show()
    # return

# 测试plt的函数
def pltshow():
    plt.plot([1, 2], [3, 4], color='r', lw=0.1)
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    # y 轴不可见
    # frame = plt.gca()
    # frame.axes.get_yaxis().set_visible(False)
    # # x 轴不可见
    # frame.axes.get_xaxis().set_visible(False)
    plt.show()


def isnext(a, b, src, tag):
    if ((abs(a[0] - b[0]) + abs(a[1] - b[1])) == 1 and tag[a[0], a[1]] == 0 and tag[b[0], b[1]] == 0 and src[
        a[0], a[1]] < 0 and src[b[0], b[1]] > 0):
        return True
    else:
        return False


# 在正的周围找正的,在负的周围找负的
def extend_double1(x1, y1, x2, y2, src, tag):
    if (x1 > src.shape[0] - 2 or x1 < 1 or x2 > src.shape[0] - 2 or x2 < 1):
        return
    if (y1 > src.shape[1] - 2 or y1 < 1 or y2 > src.shape[1] - 2 or y2 < 1):
        return
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)
    list_4 = {}
    for m in range(min_x - 1, max_x + 2):
        if (tag[m, min_y - 1] == 0):
            list_4[(m, min_y - 1)] = src[m, min_y - 1]
        if (tag[m, max_y + 1] == 0):
            list_4[(m, max_y + 1)] = src[m, max_y + 1]
    for m in range(min_y - 1, max_y + 2):
        if (tag[min_x - 1, m] == 0):
            list_4[(min_x - 1, m)] = src[min_x - 1, m]
        if (tag[max_x, m] == 0):
            list_4[(max_x + 1, m)] = src[max_x + 1, m]
    # f = zip(list_4.values(), list_4.keys())
    list1 = sorted(list_4.items(), key=lambda x: x[1])
    sorted(list1)  # 从小到大进行排序
    if (len(list1) >= 2 and isnext(list1[0][0], list1[len(list_4) - 1][0], src, tag) == True):
        print(1)
        tag[list1[0][0][0], list1[0][0][1]] = -1
        tag[list1[len(list1) - 1][0][0], list1[len(list1) - 1][0][1]] = 1
        extend_double1(list1[0][0][0], list1[0][0][1], list1[len(list1) - 1][0][0], list1[len(list1) - 1][0][1], src,
                       tag)
    else:
        return


def extend_double(tag, src):
    for x in range(1, tag.shape[0] - 1):
        for y in range(1, tag.shape[1] - 1):
            if tag[x, y] > 0:
                for k in range(len(xxx)):
                    if (tag[x + xxx[k], y + yyy[k]] < 0):
                        extend_double1(x, y, x + xxx[k], y + yyy[k], src, tag)
    return tag


def absabs(re):
    for i in range(re.shape[0]):
        for j in range(re.shape[1]):
            if (re[i, j] < 0):
                re[i, j] = abs(re[i, j])
    return re


# 从右上角开始,逆时针旋转
# 通过判断像素点是否为噪声点,然后对其八邻域进行分区,把属于其分区的像素区域的均值赋予中心点
# xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
# yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
def fix_noise(src1, tag, noise_num):
    src = src1.copy()
    for i in range(tag.shape[0]):
        for j in range(tag.shape[1]):
            if tag[i, j] > 1:
                a_sum = 0
                a_num = 0
                b_sum = 0
                b_num = 0
                minn, a, b = modify.point_classification_new(src1, i, j, 1)
                for aa in a:
                    # if tag[aa[0], aa[1]] == 0:
                    if tag[aa[0], aa[1]] <= noise_num:
                        a_sum += src[aa[0], aa[1]]
                        a_num += 1
                for bb in b:
                    # if tag[bb[0], bb[1]] == 0:
                    if tag[bb[0], bb[1]] <= noise_num:
                        b_sum += src[bb[0], bb[1]]
                        b_num += 1
                if b_num > 0 and a_num > 0:
                    if abs(src[i, j] - a_sum / a_num) > abs(src[i, j] - b_sum / b_num):
                        src[i, j] = b_sum / b_num
                    else:
                        src[i, j] = a_sum / a_num
                # 输出测试结果
                # if (i == 7 and j == 72 and b_num != 0):
                #     print(b_sum / b_num)
                # if (i == 7 and j == 72 and a_num != 0):
                #     print(a_sum / a_num)
                # if (i == 7 and j == 72):
                #     print(b_num)
                #     print(a_num)
                #     print(b_sum)
                #     print(a_sum)
    return src


#  高权重区域代表上下左右四个像素值
# hx = [-1, 0, 0, +1]
# hy = [0, -1, +1, 0]
def transition_area(src, tag):
    flag_t = 0
    for i in range(1, src.shape[0] - 1):
        for j in range(1, src.shape[1] - 1):
            tag1 = 0
            tag2 = 0
            list_neg = []
            list_pos = []
            if tag[i, j] == 0:
                flag_t = 1
                for x in range(4):
                    if tag[i + hx[x], j + hy[x]] == 1:
                        tag1 = 1
                        list_pos.append(src[i + hx[x], j + hy[x]])
                    if tag[i + hx[x], j + hy[x]] == -1:
                        tag2 = 1
                        list_neg.append(src[i + hx[x], j + hy[x]])
                if tag1 == 1 and tag2 == 1:
                    src[i, j] = sum(list_neg) / len(list_neg)
                    tag[i, j] = -2
                elif tag1 == 1 and tag2 == 0:
                    src[i, j] = sum(list_pos) / len(list_pos)
                    tag[i, j] = 2
                elif tag1 == 0 and tag2 == 1:
                    src[i, j] = sum(list_neg) / len(list_neg)
                    tag[i, j] = -2
    tag = for_next(tag)
    if flag_t == 0:
        print(src)
        return src
    elif flag_t == 1:
        print(1)
        transition_area(src, tag)
        return src  # 很关键,如果不在这里加入返回,则得到的的src为None


def for_next(tag):
    for i in range(tag.shape[0]):
        for j in range(tag.shape[1]):
            if tag[i, j] == 2:
                tag[i, j] = 1
            elif tag[i, j] == -2:
                tag[i, j] = -1
    return tag


def transition_tag(tag1, tag2):
    for i in range(tag1.shape[0]):
        for j in range(tag1.shape[1]):
            if tag1[i, j] == 1:
                tag1[i, j] = 0
            elif tag1[i, j] == 0:
                if tag2[i, j] < 0:
                    tag1[i, j] = -1
                else:
                    tag1[i, j] = 1
    return tag1
