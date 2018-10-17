# from pylab import *
import numpy as np


# 将大于阈值的数统一一下便于分类处理+2-2,小于阈值的就是+1-1
def labels_matrix(ori_matrix, value):
    x, y = ori_matrix.shape
    new_matrix = np.zeros((x, y))
    for i in range(x):
        for j in range(y):
            if abs(ori_matrix[i][j]) <= value:
                if ori_matrix[i][j] >= 0:  # 0继续保持
                    new_matrix[i][j] = 1
                elif ori_matrix[i][j] < 0:
                    new_matrix[i][j] = -1
            elif abs(ori_matrix[i][j]) > value:
                if ori_matrix[i][j] > 0:
                    new_matrix[i][j] = 2
                elif ori_matrix[i][j] < 0:
                    new_matrix[i][j] = -2
    return new_matrix


# 四个像素的local 的坐标
xx = [0, 0, 1, 1]
yy = [0, 1, 1, 0]


# 验证local是不是大于阈值且是非交叉矛盾的
def isVerifi(mul_list):
    neg = 0
    pos = 0
    for i in range(4):
        if mul_list[i] == -4:
            neg += 1
        elif mul_list[i] == 4:
            pos += 1
    if neg == 2 and pos == 2:
        return True


# -1+1交叉分布,特殊进行延伸
def equal4(mul_list):
    tag = 0
    for i in range(4):
        if (mul_list[i] == -1):
            tag += 1
    if tag == 4:
        return True
    else:
        return False


# 特殊的起始点,周围有两个大于阈值的并且相邻的点,那么那些+1-1的点可以当做正常点进行延伸
def isSpecial(mul_list):
    tag1 = 0
    tag2 = 0
    tagTack = 0
    for i in range(4):
        if mul_list[i] == -4:
            tag1 += 1
    for i in range(4):
        if mul_list[i] < 0:
            tag2 += 1
            if mul_list[i] != -4:
                tagTack = i
    if tag1 == 1 and tag2 == 2:
        return tagTack
    else:
        return 9


# 根据当前的local的画边点的序号找到当前画边点的中点
def point(k, i, j):
    if k == 0:
        return i + 0.5, j
    if k == 1:
        return i, j + 0.5
    if k == 2:
        return i + 0.5, j + 1
    if k == 3:
        return i + 1, j + 0.5


# 根据当前延伸的边,延伸的下一个local区域的左上角的坐标点
def next_local(list_n, i, j):
    if list_n == 0:
        return i, j - 1
    if list_n == 1:
        return i - 1, j
    if list_n == 2:
        return i, j + 1
    if list_n == 3:
        return i + 1, j


# 根据当前延伸的边,延伸下两个坐标点的坐标信息
def next_point(list_n, i, j):
    if list_n == 0:
        return i, j - 1, i + 1, j - 1
    if list_n == 1:
        return i - 1, j, i - 1, j + 1
    if list_n == 2:
        return i, j + 2, i + 1, j + 2
    if list_n == 3:
        return i + 2, j, i + 2, j + 1


def next_mid(mul_list, n):
    for i in range(4):
        if mul_list[i] < 0 and i != n:
            return i


def local_side(n):
    if n == 0:
        return 2
    if n == 1:
        return 3
    if n == 2:
        return 0
    if n == 3:
        return 1


def repair(matrix, i, j):
    for k in range(len(xx)):
        if matrix[i + xx[k], j + yy[k]] > 0:
            matrix[i + xx[k], j + yy[k]] = 2
        elif matrix[i + xx[k], j + yy[k]] < 0:
            matrix[i + xx[k], j + yy[k]] = -2


# 追踪延伸
def track(matrix, list_n, i, j, point_x, point_y):
    if i >= matrix.shape[0] - 1 or j >= matrix.shape[1] - 1 or i <= 0 or j <= 0:
        return
    mul_list = []
    for k in range(len(xx)):
        mul_list.append(matrix[i + xx[k], j + yy[k]] * matrix[i + xx[k - 1], j + yy[k - 1]])
    x1, y1, x2, y2 = next_point(list_n, i, j)
    if x1 >= matrix.shape[0] - 1 or y1 >= matrix.shape[1] - 1 or x1 <= 0 or y1 <= 0:
        return
    if x2 >= matrix.shape[0] - 1 or y2 >= matrix.shape[1] - 1 or x2 <= 0 or y2 <= 0:
        return
    if matrix[x1, y1] * matrix[x2, y2] != -4 and matrix[x1, y1] * matrix[x2, y2] != 0 and equal4(mul_list) == False:
        x, y = next_local(list_n, i, j)
        n = next_mid(mul_list, local_side(list_n))
        point_x.append(point(list_n, i, j)[0])
        point_y.append(point(list_n, i, j)[1])
        point_x.append(point(local_side(list_n), i, j)[0])
        point_y.append(point(local_side(list_n), i, j)[1])
        track(matrix, n, x, y, point_x, point_y)


# 画边
def traverse(matrix):
    w, h = matrix.shape
    points_x = []
    points_y = []
    special_x = []
    special_y = []
    for i in range(w - 1):
        for j in range(h - 1):
            mid_x = []
            mid_y = []
            mul_list = []
            for k in range(len(xx)):
                mul_list.append(matrix[i + xx[k], j + yy[k]] * matrix[i + xx[k - 1], j + yy[k - 1]])
                # if (matrix[i + xx[k], j + yy[k]] * matrix[i + xx[k - 1], j + yy[k - 1]] < 0 and abs(
                #         matrix[i + xx[k], j + yy[k]]) == 2
                #         and abs(matrix[i + xx[k - 1], j + yy[k - 1]]) == 2):
                #     mid_x.append(i + (xx[k] + xx[k - 1]) / 2)
                #     mid_y.append(j + (yy[k] + yy[k - 1]) / 2)
                # elif()
                # if(isHigh(mul_list) and isVerifi(mul_list)):
            n = isSpecial(mul_list)
            if isVerifi(mul_list):
                for k in range(len(xx)):
                    if mul_list[k] == -4:
                        mid_x.append(point(k, i, j)[0])
                        mid_y.append(point(k, i, j)[1])
            elif n != 9:
                track(matrix, n, i, j, points_x, points_x)
            if len(mid_x) == 2:
                points_x.append(mid_x[0])
                points_x.append(mid_x[1])
                points_y.append(mid_y[0])
                points_y.append(mid_y[1])

    return points_x, points_y
