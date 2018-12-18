import rgb
import numpy as np
import cv2
import matplotlib.pyplot as plt

def fix_tag(gray, i, j):
    # if isinstance(j, int):
    #     gray[int(i + 0.5), j] = 1
    #     # gray[int(i - 0.5), j] = 1
    # if isinstance(i, int):
    #     gray[i, int(j + 0.5)] = 1
    #     # gray[i, int(j - 0.5)] = 1
    gray[i, j] = 1


gray = np.zeros((5, 5))
path1 = "D:\\cs.csv"


# gray = np.loadtxt(path1, dtype=np.int, delimiter=",", encoding='utf-8', usecols=range(4))

# print(gray)
# r1, r2 = p2.cut(gray, 10, 3)
# print(r1)
# print(r2)


# verify_close(gray)

# 输入 gray原始标记图,i,j 分别为横纵坐标
# 作用:原图分割点进行标记
def fix_tag(gray, i, j):
    # if isinstance(j, int):
    #     gray[int(i + 0.5), j] = 1
    #     # gray[int(i - 0.5), j] = 1
    # if isinstance(i, int):
    #     gray[i, int(j + 0.5)] = 1
    #     # gray[i, int(j - 0.5)] = 1
    gray[i, j] = 1


# 输入gray原始标记上图,i,j分别是横轴坐标,tag是区域划分的标记符号
# 作用:遍历25邻域,进行区域标记
def go_near(gray, i, j, tag, i_low, i_high, j_low, j_high, gray1):
    # if i + 1 > 4 or j + 1 > 4:
    #     return
    # if i - 1 < 0 or j - 1 < 0:
    #     return
    # show_area(gray,i,j)
    if i_low <= i + 1 <= i_high and j_low <= j <= j_high and gray[i + 1, j] == 0 and gray1[
        int((i + 0.5) * 2), j * 2] != 1:
        gray[i + 1, j] = tag
        print((i+1,j))
        go_near(gray, i + 1, j, tag, i_low, i_high, j_low, j_high, gray1)
    if i_low <= i <= i_high and j_low <= j + 1 <= j_high and gray[i, j + 1] == 0 and gray1[
        i * 2, int((j + 0.5) * 2)] != 1:
        gray[i, j + 1] = tag
        print((i,j+1))
        go_near(gray, i, j + 1, tag, i_low, i_high, j_low, j_high, gray1)
    if i_high >= i - 1 >= i_low and j_low <= j <= j_high and gray[i - 1, j] == 0 and gray1[
        int((i - 0.5) * 2), j * 2] != 1:
        gray[i - 1, j] = tag
        print((i-1,j))
        go_near(gray, i - 1, j, tag, i_low, i_high, j_low, j_high, gray1)
    if i_low <= i <= i_high and j_high >= j - 1 >= j_low and gray[i, j - 1] == 0 and gray1[
        i * 2, int((j - 0.5) * 2)] != 1:
        gray[i, j - 1] = tag
        print((i,j-1))
        go_near(gray, i, j - 1, tag, i_low, i_high, j_low, j_high, gray1)



# gray原始标记图,x,y是起始25邻域的左上坐标点
# 如果没有形成闭合的区域就去除该区域的标记
def fix_area(gray, x, y):
    for i in range(x, x + 5):
        for j in range(y, y + 5):
            gray[i, j] = 0


def fix_area1(gray1, x, y):
    tag = False
    # for i in range(x+2, x + 8):
    for i in range(x, x + 10):
        # for j in range(y+2, y + 8):
        for j in range(y, y + 10):
            if gray1[i,j]==1:
                tag = True
            # gray1[i, j] = 0
    if tag == True:
        return 1
            # print(gr)

def show_gray(gray, x, y):
    for i in range(x, x + 5):
        print()
        for j in range(y, y + 5):
            print(gray[i,j],end="  ")


def show_tag(gray, x, y):
    for i in range(x, x + 10):
        print()
        for j in range(y, y + 10):
            print(gray[i,j],end="  ")

def show_area(gray, x, y):
    for i in range(x, x + 5):
        print()
        for j in range(y, y + 5):
            print(gray[i,j],end="  ")


# gray原始的标记图,x,y起始25邻域的左上坐标点
# 判断该25邻域是给是有闭合区域
def verify_close(gray, x, y, gray1,raw):
    tag = 2
    i_low = x
    i_high = x + 4
    j_low = y
    j_high = y + 4
    for i in range(x, x + 5):
        for j in range(y, y + 5):
            # go_near(gray, i, j)
            # print((i, j))
            if gray[i, j] == 0:
                gray[i, j] = tag
                print((i,j,1,1,1,1))
                print(tag)
                go_near(gray, i, j, tag, i_low, i_high, j_low, j_high, gray1)
                tag += 1
    # print(gray)
    if tag == 3:
        # fix_area(gray, x, y)
        re_tag = fix_area1(gray1, x * 2, y * 2)
        if re_tag==1:
            show_gray(raw,x,y)
            show_tag(gray1,x * 2, y * 2)
            show_area(gray,x,y)
        # a = 1
    else:
        # print(gray)
        # fix_noise(gray, x * 2, y * 2, gray1)
        a = 1
        # fix_area(gray, x, y)
        # print("2222")
    # print(tag)


x_po = [-1, 0, 1, 0]
y_po = [0, 1, 0, -1]


# 作用:处理区域内部的八邻域多余分割点
# 过程: 查看该分割点前后区域是否被归为同一个区域,前后的判定是根据在横轴坐标的哪个轴上面
def fix_noise(gray, x, y, gray1):
    for i in range(x, x + 9):
        for j in range(y, y + 9):
            if gray1[i, j] == 1:
                # tag = 0
                # for k in range(1, len(x_po)):
                #     if gray1[i + x_po[0], j + y_po[0]] == gray1[i + x_po[k], j + y_po[k]] and (
                #             gray1[i + x_po[0], j + y_po[0]] != 1 or gray1[i + x_po[k], j + y_po[k]] != 1):
                #         tag += 1
                # if tag == 3:
                #     gray1[i, j] = 0
                if i % 2 == 0:
                    if gray[int(i / 2), int(j / 2 + 0.5)] == gray[int(i / 2), int(j / 2 - 0.5)]:
                        gray1[i, j] = 0
                        # print("fix__j")
                if j % 2 == 0:
                    if gray[int(i / 2 + 0.5), int(j / 2)] == gray[int(i / 2 - 0.5), int(j / 2)]:
                        gray1[i, j] = 0
                        # print("fix__i")


# print(gray)
gray1 = np.zeros((gray.shape[0] * 2, gray.shape[1] * 2))
# print(gray1)
fix_tag(gray1, 8, 9)
fix_tag(gray1, 9, 8)

# fix_tag(gray1, 0, 1)
# fix_tag(gray1, 1, 0)

# fix_tag(gray1, 2.5, 2)
# fix_tag(gray1, 2.5, 3)
# fix_tag(gray1, 2.5, 4)

# fix_tag(gray1, 5, 0)
# fix_tag(gray1, 5, 2)
# fix_tag(gray1, 5, 4)
# fix_tag(gray1, 5, 6)
# fix_tag(gray1, 5, 8)

# fix_tag(gray1, 2, 5)
# fix_tag(gray1, 4, 5)
# fix_tag(gray1, 6, 5)
# fix_tag(gray1, 8, 5)
# fix_tag(gray1, 0, 5)
# fix_tag(gray1, 1, 2)

print(gray1)
verify_close(gray, 0, 0, gray1,gray)
print(gray1)
# print(gray)