# import p2
# import numpy as np
# import cv2
#
# # gray = np.loadtxt("D:\\cs.csv", dtype=np.int, delimiter=",", encoding='utf-8')
# # gray = np.loadtxt("D:\\cs.csv", dtype=np.int, delimiter=",", encoding='utf-8', usecols=range(5))
#
# # a, b, c = p2.cut(gray, 0, 1)
# # print(a)
# a = cv2.imread("D:\\experiment\\pic\\q\\8068.jpg")
# # print(a)
# # print(a[0])
# # print(a[1])
# # print(a[2])
# np.savetxt("D:\\a0" + ".csv", a[:, :, 0], fmt="%d", delimiter=',')
# np.savetxt("D:\\a1" + ".csv", a[:, :, 1], fmt="%d", delimiter=',')
# np.savetxt("D:\\a2" + ".csv", a[:, :, 2], fmt="%d", delimiter=',')


# 以像素点之间的中点向量作为分割边界

import rgb
import numpy as np
import cv2
import matplotlib.pyplot as plt

# gray = np.array([[100, 100, 100], [80, 80, 80], [80, 110, 80]])
# gray = np.array([[80, 80, 80], [80, 80, 80], [80, 110, 80]])
# gray = np.array([[80, 80, 80], [80, 80, 80], [80, 110, 80]])
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
    if i_low <= i + 1 <= i_high and j_low <= j <= j_high and gray[i + 1, j] == 0 and gray1[
        int((i + 0.5) * 2), j * 2] != 1:
        gray[i + 1, j] = tag
        go_near(gray, i + 1, j, tag, i_low, i_high, j_low, j_high, gray1)
    if i_low <= i <= i_high and j_low <= j + 1 <= j_high and gray[i, j + 1] == 0 and gray1[
        i * 2, int((j + 0.5) * 2)] != 1:
        gray[i, j + 1] = tag
        go_near(gray, i, j + 1, tag, i_low, i_high, j_low, j_high, gray1)
    if i_high >= i - 1 >= i_low and j_low <= j <= j_high and gray[i - 1, j] == 0 and gray1[
        int((i - 0.5) * 2), j * 2] != 1:
        gray[i - 1, j] = tag
        go_near(gray, i - 1, j, tag, i_low, i_high, j_low, j_high, gray1)
    if i_low <= i <= i_high and j_high >= j - 1 >= j_low and gray[i, j - 1] == 0 and gray1[
        i * 2, int((j - 0.5) * 2)] != 1:
        gray[i, j - 1] = tag
        go_near(gray, i, j - 1, tag, i_low, i_high, j_low, j_high, gray1)


# gray原始标记图,x,y是起始25邻域的左上坐标点
# 如果没有形成闭合的区域就去除该区域的标记
def fix_area(gray, x, y):
    for i in range(x, x + 5):
        for j in range(y, y + 5):
            gray[i, j] = 0


def fix_area1(gray1, x, y):
    for i in range(x, x + 10):
        for j in range(y, y + 10):
            gray1[i, j] = 0


# gray原始的标记图,x,y起始25邻域的左上坐标点
# 判断该25邻域是给是有闭合区域
def verify_close(gray, x, y, gray1):
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
                go_near(gray, i, j, tag, i_low, i_high, j_low, j_high, gray1)
                tag += 1
    # print(gray)
    if tag == 3:
        fix_area(gray, x, y)
        fix_area1(gray1, x * 2, y * 2)
    else:
        # print(gray)
        fix_noise(gray, x * 2, y * 2, gray1)
        fix_area(gray, x, y)
        print("2222")
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


src = "41004"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\"

raw = cv2.imread(inpath + src + ".jpg")

# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)

raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
# raw_Filter = raw
# raw2_Filter = raw2

raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)

cv2.imwrite("D:\\gray" + src + ".jpg", raw2_Filter)
np.savetxt("D:\\gray" + src + ".csv", raw2_Filter, fmt="%d", delimiter=',')

raw2_Filter = np.loadtxt("D:\\cs.csv", dtype=np.int, delimiter=",", encoding='utf-8')
raw_Filter = np.zeros((5, 5, 3))
raw_Filter[:, :, 1] = raw2_Filter
raw_Filter[:, :, 0] = raw2_Filter
raw_Filter[:, :, 2] = raw2_Filter

raw = raw_Filter
raw2 = raw2_Filter

# re, re_weak = p2.cut(raw2_Filter, 20, 3)
# 大小两个阈值
re, re_weak, noise = rgb.cut(raw2_Filter, 5, 2, raw_Filter)
# np.savetxt("D:\\fix_gray" + src + ".csv", raw2_Filter, fmt="%d", delimiter=',')

print(re)

gray = np.zeros((raw2.shape[0], raw2.shape[1]))

gray1 = np.zeros((raw2.shape[0] * 2, raw2.shape[1] * 2))

print((raw2.shape[0], raw2.shape[1]))
for m in range(0, len(re)):
    x1 = re[m][0][0]
    x2 = re[m][1][0]
    y1 = re[m][0][1]
    y2 = re[m][1][1]
    # x2 = re[m + 1][1][0]
    # x2 = re[m + 1][1][0]
    # y2 = re[m + 1][1][1]
    # y2 = re[m + 1][1][1]
    # plt.scatter((x1 + x2) / 2, (y1 + y2) / 2, c='r')
    yy = (y1 + y2)
    xx = (x1 + x2)
    # if yy % 2 == 0:
    #     yy = int((y1 + y2) / 2)
    #     xx = (x1 + x2) / 2
    # if xx % 2 == 0:
    #     xx = int((x1 + x2) / 2)
    #     yy = (y1 + y2) / 2
    # print((xx, yy))
    fix_tag(gray1, xx, yy)

np.savetxt("D:\\tag" + src + ".csv", gray1, fmt="%d", delimiter=',')

re1 = np.zeros((gray.shape[0], gray.shape[1]))
for i in range(gray1.shape[0]):
    for j in range(gray1.shape[1]):
        if gray1[i, j] == 1:
            re1[int(i / 2), int(j / 2)] = 255
cv2.imwrite("D:\\re_local_raw" + src + ".jpg", re1)

for i in range(0, gray.shape[0] - 5, 5):
    for j in range(0, gray.shape[1] - 5, 5):
        verify_close(gray, i, j, gray1)
np.savetxt("D:\\re_local" + src + ".csv", gray, fmt="%d", delimiter=',')

# for i in range(9, gray1.shape[1], 10):
#     for j in range(0, gray1.shape[0]):
#         gray1[j, i] = 0
#
# for i in range(9, gray1.shape[0], 10):
#     for j in range(0, gray1.shape[1]):
#         gray1[i, j] = 0

re = np.zeros((gray.shape[0], gray.shape[1]))
for i in range(gray1.shape[0]):
    for j in range(gray1.shape[1]):
        if gray1[i, j] == 1:
            re[int(i / 2), int(j / 2)] = 255
cv2.imwrite("D:\\re_local" + src + ".jpg", re)

re_x = []
re_y = []
# print(re)
# for m in range(0, len(re)):
#     x1 = re[m][0][0]
#     x2 = re[m][1][0]
#     y1 = re[m][0][1]
#     y2 = re[m][1][1]
#     # x2 = re[m + 1][1][0]
#     # x2 = re[m + 1][1][0]
#     # y2 = re[m + 1][1][1]
#     # y2 = re[m + 1][1][1]
#     # plt.scatter((x1 + x2) / 2, (y1 + y2) / 2, c='r')
#     yy = (y1 + y2)
#     xx = (x1 + x2)
#     if yy % 2 == 0:
#         yy = int((y1 + y2) / 2)
#         xx = (x1 + x2) / 2
#     # xx = ((y1 + y2))
#     # yy = ((x1 + x2))
#     if xx % 2 == 0:
#         xx = int((x1 + x2) / 2)
#         yy = (y1 + y2) / 2
#     if isinstance(yy, int) and gray[int(xx + 0.5), yy] == 255 and gray[int(xx - 0.5), yy] == 255:
#         # gray[int(xx + 0.5), yy] = 0
#         # gray[int(xx - 0.5), yy] = 0
#         print(1)
#         re_x.append(xx)
#         re_y.append(yy)
#     if isinstance(xx, int) and gray[xx, int(yy + 0.5)] == 255 and gray[xx, int(yy - 0.5)] == 255:
#         # gray[xx, int(yy + 0.5)] = 0
#         # gray[xx, int(yy - 0.5)] = 0
#         print(2)
#         re_x.append(xx)
#         re_y.append(yy)


# 全图的存储
for i in range(gray1.shape[0]):
    for j in range(gray1.shape[1]):
        if gray1[i, j] == 1:
            re_x.append(i / 2)
            re_y.append(j / 2)

# 只针对5*5的区域进行存储
# x_in = 130 * 2
# y_in = 110 * 2
# for i in range(x_in, x_in + 9):
#     for j in range(y_in, y_in + 9):
#         if gray1[i, j] == 1:
#             re_x.append(i / 2)
#             re_y.append(j / 2)
#
# cs_gray = np.zeros((5, 5))
# for i in range(int(x_in / 2), int(x_in / 2) + 5):
#     for j in range(int(y_in / 2), int(y_in / 2) + 5):
#         cs_gray[i - int(x_in / 2), j - int(y_in / 2)] = raw2_Filter[i, j]
# np.savetxt("D:\\cs_gray" + src + ".csv", cs_gray, fmt="%d", delimiter=',')
#
# x8 = 1
# y8 = 1
x_in = 0
y_in = 0
for x8 in range(1, 4):
    for y8 in range(1, 4):
        rgb.show_cut(raw2_Filter, 10, 5, raw_Filter, int(x_in / 2) + x8, int(y_in / 2) + y8)

print(re_x)
print(re_y)
plt.scatter(re_y, re_x, s=1, c='r')
plt.gca().invert_yaxis()
plt.savefig("D:\\re_local_line" + src,
            dpi=1000)  # 指定分辨率保存

re, re_weak, noise = rgb.cut(raw2, 10, 5, raw)
show = np.zeros((raw2.shape[0] * 2, raw2.shape[1] * 2))
for m in range(0, len(re)):
    x1 = re[m][0][0]
    x2 = re[m][1][0]
    y1 = re[m][0][1]
    y2 = re[m][1][1]
    yy = ((y1 + y2))
    xx = ((x1 + x2))
    show[xx, yy] = 2
for k in range(0, len(re_weak)):
    x1 = re_weak[k][0][0]
    x2 = re_weak[k][1][0]
    y1 = re_weak[k][0][1]
    y2 = re_weak[k][1][1]
    yy = ((y1 + y2))
    xx = ((x1 + x2))
    show[xx, yy] = 1

x, y = rgb.find_weak(show, show)

gray = np.zeros((raw2.shape[0], raw2.shape[1]))
gray1 = np.zeros((raw2.shape[0] * 2, raw2.shape[1] * 2))
for m in range(0, len(re)):
    x1 = re[m][0][0]
    x2 = re[m][1][0]
    y1 = re[m][0][1]
    y2 = re[m][1][1]
    yy = (y1 + y2)
    xx = (x1 + x2)
    fix_tag(gray1, xx, yy)
for m in range(0, len(x)):
    xx = int(x[m] * 2)
    yy = int(y[m] * 2)
    fix_tag(gray1, xx, yy)

for i in range(0, gray.shape[0] - 5, 5):
    for j in range(0, gray.shape[1] - 5, 5):
        verify_close(gray, i, j, gray1)

re_x = []
re_y = []
for i in range(gray1.shape[0]):
    for j in range(gray1.shape[1]):
        if gray1[i, j] == 1:
            re_x.append(i / 2)
            re_y.append(j / 2)
plt.scatter(re_y, re_x, s=1, c='r')
# plt.gca().invert_yaxis()
plt.savefig("D:\\re_extend" + src,
            dpi=1000)  # 指定分辨率保存

# print(gray)
# gray1 = np.zeros((gray.shape[0] * 2, gray.shape[1] * 2))
# print(gray1)
# fix_tag(gray1, 1, 0)
# fix_tag(gray1, 0, 1)
# # fix_tag(gray1, 2.5, 2)
# # fix_tag(gray1, 2.5, 3)
# # fix_tag(gray1, 2.5, 4)
#
# # fix_tag(gray1, 5, 0)
# # fix_tag(gray1, 5, 2)
# # fix_tag(gray1, 5, 4)
# # fix_tag(gray1, 5, 6)
# # fix_tag(gray1, 5, 8)
#
# # fix_tag(gray1, 2, 5)
# # fix_tag(gray1, 4, 5)
# # fix_tag(gray1, 6, 5)
# # fix_tag(gray1, 8, 5)
# # fix_tag(gray1, 0, 5)
# # fix_tag(gray1, 1, 2)
#
# print(gray1)
# verify_close(gray, 0, 0, gray1)
# print(gray1)
# print(gray)
