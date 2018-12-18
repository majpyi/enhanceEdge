# from pylab import *
import numpy as np


# 将大于阈值的数统一一下便于分类处理+2-2,小于阈值的就是+1-1
def labels_matrix(ori_matrix, value):
    x, y = ori_matrix.shape
    new_matrix = np.zeros((x, y))
    for i in range(x):
        for j in range(y):
            if abs(ori_matrix[i][j]) <= value:
                if ori_matrix[i][j] > 0:  # 0继续保持
                    new_matrix[i][j] = 1
                elif ori_matrix[i][j] < 0:
                    new_matrix[i][j] = -1
            elif abs(ori_matrix[i][j]) > value:
                if ori_matrix[i][j] > 0:
                    new_matrix[i][j] = 2
                elif ori_matrix[i][j] < 0:
                    new_matrix[i][j] = -2
    return new_matrix


# 将大于阈值的数统一一下便于分类处理+2-2,小于阈值的就是+1-1
def labels_matrix_new(ori_matrix, value, low):
    x, y = ori_matrix.shape
    new_matrix = np.zeros((x, y))
    for i in range(x):
        for j in range(y):
            if low <= abs(ori_matrix[i][j]) <= value:
                if ori_matrix[i][j] > 0:  # 0继续保持
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


# 作用:验证local是不是大于阈值且是非交叉矛盾的
def isVerifi(mul_list):
    neg = 0
    pos = 0
    for i in range(4):
        if mul_list[i] == -4:
            neg += 1
        elif mul_list[i] == 4:
            pos += 1
    # if neg == 2 and pos == 2:
    if neg == 2:
        return True
    # if neg != 4 and (pos+neg) == 4:
    #     return True


# 作用:验证local即使包含有0但只要是可以画边的就进行
def isContinue(mul_list):
    neg = 0
    pos = 0
    for i in range(4):
        if mul_list[i] < 0:
            neg += 1
        elif mul_list[i] == 4:
            pos += 1
    # if neg == 2 and pos == 2:
    if neg == 2:
        return True



# 作用:验证-1+1交叉分布,特殊进行延伸
def equal4(mul_list):
    tag = 0
    for i in range(4):
        # if (mul_list[i] == -1):
        if (mul_list[i] < 0):
            tag += 1
    if tag == 4:
        return False
    else:
        return True


# 特殊的起始点,周围有两个大于阈值的并且相邻的点,那么那些+1-1的点可以当做正常点进行延伸
def isSpecial(mul_list):
    tag1 = 0
    tag2 = 0
    tagTack = 0
    tagPre = 0
    # for i in range(4):
    #     if mul_list[i] == -4:
    #         tag1 += 1
    # for i in range(4):
    #     if mul_list[i] < 0:
    #         tag2 += 1
    #         if mul_list[i] != -4:
    #             tagTack = i
    #         else:
    #             tagPre = i
    for i in range(4):
        if mul_list[i] == -4:
            tag1 += 1
            tagPre = i
    for i in range(4):
        if mul_list[i] == -2 or mul_list[i] == -1:
            tag2 += 1
            tagTack = i

    # if tag1 == 1 and tag2 == 2:
    if tag1 == 1 and tag2 == 1:
        # print(1)
        return tagTack, tagPre
    else:
        return 9, 9


# 根据当前的local的画边点的序号找到当前画边点的中点
# 参数: 当前local的边序号,当前local的坐标
# 返回: 当前local的画边的坐标中点
def point(k, i, j):
    if k == 0:
        return i + 0.5, j
    if k == 1:
        return i, j + 0.5
    if k == 2:
        return i + 0.5, j + 1
    if k == 3:
        return i + 1, j + 0.5


# 参数:当前local的边序号,当前local的坐标
# 返回值:下一个local的坐标值
# 作用:根据当前延伸的边,延伸的下一个local区域的左上角的坐标点
def next_local(list_n, i, j):
    if list_n == 0:
        return i, j - 1
    if list_n == 1:
        return i - 1, j
    if list_n == 2:
        return i, j + 1
    if list_n == 3:
        return i + 1, j


# 参数:前一个local的终止边序号,当前local的左上坐标
# 返回值: 当前local中新增加的两个点的坐标
def next_two_point(list_n, i, j):
    if list_n == 0:
        return i, j, i + 1, j
    if list_n == 1:
        return i, j, i, j + 1
    if list_n == 2:
        return i, j + 1, i + 1, j + 1
    if list_n == 3:
        return i + 1, j, i + 1, j + 1


# 参数:当前local的四个边的乘积,当前local中起始延伸边的序号
def next_mid(mul_list, n):
    for i in range(4):
        if mul_list[i] < 0 and i != n:
            return i


# 参数:上一个local的边序号
# 返回值:当前local的边序号
def local_side(n):
    if n == 0:
        return 2
    if n == 1:
        return 3
    if n == 2:
        return 0
    if n == 3:
        return 1


# 参数:矩阵,当前local的坐标
# 返回值: void
# 作用:修复当前local的所有标记,修复为正常值
def repair(matrix, i, j):
    for k in range(len(xx)):
        # if matrix[i + xx[k], j + yy[k]] > 0:
        if matrix[i + xx[k], j + yy[k]] == 1:
            matrix[i + xx[k], j + yy[k]] = 3
            # matrix[i + xx[k], j + yy[k]] = 2
        # elif matrix[i + xx[k], j + yy[k]] < 0:
        elif matrix[i + xx[k], j + yy[k]] == -1:
            matrix[i + xx[k], j + yy[k]] = -3
            # matrix[i + xx[k], j + yy[k]] = -2


# 追踪延伸
# 参数: 矩阵,上一个local的终止延伸点,当前新延伸的local的坐标点
def track(matrix, list_n, i, j, point_x, point_y,gray1):
    if i >= matrix.shape[0] - 1 or j >= matrix.shape[1] - 1 or i < 0 or j < 0:
        return
    # 根据上一个延伸终点边序号,找到当前local新增加的两个点的坐标
    x1, y1, x2, y2 = next_two_point(list_n, i, j)
    mul_list = []
    for k in range(len(xx)):
        mul_list.append(matrix[i + xx[k], j + yy[k]] * matrix[i + xx[k - 1], j + yy[k - 1]])

    if x1 >= matrix.shape[0] - 1 or y1 >= matrix.shape[1] - 1 or x1 < 0 or y1 < 0:
        return
    if x2 >= matrix.shape[0] - 1 or y2 >= matrix.shape[1] - 1 or x2 < 0 or y2 < 0:
        return

    # 新增加的两个点 1.不能满足终止的-2,2的情况,不能包含0,不能正负交叉
    # if matrix[x1, y1] * matrix[x2, y2] != -4 and matrix[x1, y1] * matrix[x2, y2] != 4 and matrix[x1, y1] * matrix[
    #     x2, y2] != 0 and equal4(mul_list) == False:

    if matrix[x1, y1] * matrix[x2, y2] != -4 and matrix[x1, y1] * matrix[x2, y2] != 4 and matrix[x1, y1] * matrix[
        x2, y2] != -9 and matrix[x1, y1] * matrix[x2, y2] != 9 and matrix[x1, y1] * matrix[
        x2, y2] != -6 and matrix[x1, y1] * matrix[x2, y2] != 6 and verify_mid(gray1,i,j) and equal4(mul_list):
        # if matrix[x1, y1] * matrix[x2, y2] == 1 or matrix[x1, y1] * matrix[x2, y2] == -1 or matrix[x1, y1] * matrix[
        #     x2, y2] == -2 or matrix[x1, y1] * matrix[x2, y2] == 2 or matrix[x1, y1] * matrix[x2, y2] == 3 or matrix[
        #     x1, y1] * matrix[x2, y2] == -3 and equal4(mul_list) == False:

        # if matrix[x1, y1] * matrix[x2, y2] != -4  and matrix[x1, y1] * matrix[x2, y2] != 0 and equal4(mul_list) == False:
        # 找到当前local的延伸终止边的序号
        n = next_mid(mul_list, local_side(list_n))
        # 根据当前local的延伸终点的边序号,找到下一个local的左上角坐标
        x, y = next_local(n, i, j)

        point_x.append(point(local_side(list_n), i, j)[0])
        point_y.append(point(local_side(list_n), i, j)[1])
        point_x.append(point(n, i, j)[0])
        point_y.append(point(n, i, j)[1])

        repair(matrix, i, j)
        track(matrix, n, x, y, point_x, point_y)

    # 第二种+1-1矛盾交叉的情况
    elif matrix[x1, y1] * matrix[x2, y2] != -4 and matrix[x1, y1] * matrix[x2, y2] != 4 and matrix[x1, y1] * matrix[
        x2, y2] != -9 and matrix[x1, y1] * matrix[x2, y2] != 9 and matrix[x1, y1] * matrix[
        x2, y2] != -6 and matrix[x1, y1] * matrix[x2, y2] != 6 and verify_mid(gray1,i,j) and not equal4(mul_list):
        # if matrix[x1, y1] * matrix[x2, y2] == 1 or matrix[x1, y1] * matrix[x2, y2] == -1 or matrix[x1, y1] * matrix[
        #     x2, y2] == -2 or matrix[x1, y1] * matrix[x2, y2] == 2 or matrix[x1, y1] * matrix[x2, y2] == 3 or matrix[
        #     x1, y1] * matrix[x2, y2] == -3 and equal4(mul_list) == True:

        # if matrix[x1, y1] * matrix[x2, y2] != -4  and matrix[x1, y1] * matrix[x2, y2] != 0 and equal4(mul_list) == True:
        n = (local_side(list_n) + 2) % 4
        x, y = next_local(n, i, j)
        repair(matrix, i, j)
        track(matrix, n, x, y, point_x, point_y,gray1)


# 画边
def traverse(matrix):
    w, h = matrix.shape
    points_x = []
    points_y = []
    for i in range(w - 1):
        for j in range(h - 1):
            mid_x = []
            mid_y = []
            mul_list = []
            for k in range(len(xx)):
                mul_list.append(matrix[i + xx[k], j + yy[k]] * matrix[i + xx[k - 1], j + yy[k - 1]])
            n, n1 = isSpecial(mul_list)
            if isVerifi(mul_list):
                for k in range(len(xx)):
                    if mul_list[k] == -4:
                        mid_x.append(point(k, i, j)[0])
                        mid_y.append(point(k, i, j)[1])
                repair(matrix, i, j)  # 修复起始延伸点
            elif n != 9:
                x, y = next_local(n, i, j)
                track(matrix, n, x, y, points_x, points_y)
                repair(matrix, i, j)  # 修复起始延伸点
                points_x.append(point(n, i, j)[0])
                points_y.append(point(n, i, j)[1])
                points_x.append(point(n1, i, j)[0])
                points_y.append(point(n1, i, j)[1])
            if len(mid_x) == 2:
                points_x.append(mid_x[0])
                points_x.append(mid_x[1])
                points_y.append(mid_y[0])
                points_y.append(mid_y[1])

    return points_x, points_y


# 不加入延伸
def traverse1(matrix):
    w, h = matrix.shape
    points_x = []
    points_y = []
    for i in range(w - 1):
        for j in range(h - 1):
            mid_x = []
            mid_y = []
            mul_list = []
            for k in range(len(xx)):
                mul_list.append(matrix[i + xx[k], j + yy[k]] * matrix[i + xx[k - 1], j + yy[k - 1]])
            if isVerifi(mul_list):
                for k in range(len(xx)):
                    if mul_list[k] == -4:
                        mid_x.append(point(k, i, j)[0])
                        mid_y.append(point(k, i, j)[1])
            if len(mid_x) == 2:
                points_x.append(mid_x[0])
                points_x.append(mid_x[1])
                points_y.append(mid_y[0])
                points_y.append(mid_y[1])

    return points_x, points_y


def tag_cross(matrix, i, j):
    for k in range(len(xx)):
        matrix[i + xx[k], j + yy[k]] = 255


def find_cross(matrix):
    re = np.zeros((matrix.shape[0], matrix.shape[1]))
    for i in range(matrix.shape[0] - 1):
        for j in range(matrix.shape[1] - 1):
            mul_list = []
            for k in range(len(xx)):
                mul_list.append(matrix[i + xx[k], j + yy[k]] * matrix[i + xx[k - 1], j + yy[k - 1]])
            if not equal4(mul_list):
                tag_cross(re, i, j)
    return re


# 画边
def traverse_new(matrix, gray1):
    w, h = matrix.shape
    points_x = []
    points_y = []
    extend_n = []
    extend_n1 = []
    extend_i = []
    extend_j = []
    for i in range(w - 1):
        for j in range(h - 1):
            mid_x = []
            mid_y = []
            mul_list = []
            for k in range(len(xx)):
                mul_list.append(matrix[i + xx[k], j + yy[k]] * matrix[i + xx[k - 1], j + yy[k - 1]])
            n, n1 = isSpecial(mul_list)
            # if isVerifi(mul_list) or verify_mid(matrix_tag, i, j):
            if verify_mid(gray1, i, j):
                for k in range(len(xx)):
                    if mul_list[k] == -4:
                        mid_x.append(point(k, i, j)[0])
                        mid_y.append(point(k, i, j)[1])
                repair(matrix, i, j)  # 修复起始延伸点
            elif n != 9:
                extend_n1.append(n1)
                extend_n.append(n)
                # print(2)
                extend_i.append(i)
                extend_j.append(j)
            if len(mid_x) == 2:
                points_x.append(mid_x[0])
                points_x.append(mid_x[1])
                points_y.append(mid_y[0])
                points_y.append(mid_y[1])

    # return points_x, points_y, extend_n, extend_n1, extend_i, extend_j
    return extend_new(matrix, points_x, points_y, extend_n, extend_n1, extend_i, extend_j,gray1)


def extend_new(matrix, points_x, points_y, extend_n, extend_n1, extend_i, extend_j,gray1):
    print(extend_i)
    print(extend_j)
    print(points_x)
    print(points_y)
    for m in range(len(extend_i)):
        i = extend_i[m]
        j = extend_j[m]
        n = extend_n[m]
        n1 = extend_n1[m]
        x, y = next_local(n, i, j)
        track(matrix, n, x, y, points_x, points_y,gray1)
        repair(matrix, i, j)  # 修复起始延伸点
        points_x.append(point(n, i, j)[0])
        points_y.append(point(n, i, j)[1])
        points_x.append(point(n1, i, j)[0])
        points_y.append(point(n1, i, j)[1])
    return points_x, points_y


def verify_mid(gray1, x, y):
    tag = 0
    re_list_x = []
    re_list_y = []
    if gray1[x * 2, 2 * y + 1] == 1:
        tag += 1
        re_list_x.append(x)
        re_list_y.append(y+0.5)
    if gray1[x * 2 + 1, 2 * y + 2] == 1:
        tag += 1
        re_list_x.append(x+0.5)
        re_list_y.append(y+1)
    if gray1[x * 2 + 2, 2 * y + 1] == 1:
        tag += 1
        re_list_x.append(x+1)
        re_list_y.append(y+0.5)
    if gray1[x * 2 + 1, 2 * y] == 1:
        tag += 1
        re_list_x.append(x+0.5)
        re_list_y.append(y)
    if tag >= 2:
        return re_list_x,re_list_y
    else:
        return 0,0



# 四个像素的local 的坐标
# xx = [0, 0, 1, 1]
# yy = [0, 1, 1, 0]



def show_line(gray,gray1):
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            x ,y =verify_mid(gray1, i, j)
            return x,y



