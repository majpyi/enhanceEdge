import cv2
from M import *
import modify

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
                point_a.append(raws[a[k][0] - 1,a[k][1] - 1])
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

xx_tag = [-1, -1, -1, 0, +1, +1, +1, 0, 0]
yy_tag = [+1, 0, -1, -1, -1, 0, +1, +1, 0]
def gradient_tag(raws,x,y):
    re = raws.copy()
    tag = np.zeros((x,y))
    for i in range(1,x-1):
        for j in range(1,y-1):
            max_tag = []
            for k in range(9):
                max_tag.append(re[i+xx_tag[k],j+yy_tag[k]])
            for k in range(9):
                # if(re[i+xx_tag[k],j+yy_tag[k]]<max(max_tag)):
                    # re[i + xx_tag[k], j + yy_tag[k]] = 0
                # else:
                if(re[i+xx_tag[k],j+yy_tag[k]]==max(max_tag) and max(max_tag) > 5):
                    re[i + xx_tag[k], j + yy_tag[k]] = 0
                    tag[i + xx_tag[k], j + yy_tag[k]] = 255
    return  tag