import matplotlib.pyplot as plt
import numpy as np
import cv2
import p2

# plt.scatter(1.5, 2.5, c='r')
# plt.scatter(1.5, 2.5, c='b')
# plt.show()

# gray = np.array([[100, 100, 100], [80, 80, 80], [80, 110, 80]])
# gray12 = np.array([[80, 80, 80], [80, 80, 80], [80, 110, 80]])


xx = [-1, -1, -1, 0, +1, +1, +1, 0]
yy = [+1, 0, -1, -1, -1, 0, +1, +1]


# gray = np.zeros((3, 3))


def point_show(gray, re, rey, rex):
    # print(re)
    x = []
    xx = []
    y = []
    yy = []
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            # plt.scatter(i, j + 0.5, c='b')
            # plt.scatter(j, i + 0.5, c='b')
            x.append(j)
            y.append(i + 0.5)
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            # plt.scatter(i, j + 0.5, c='b')
            x.append(j + 0.5)
            y.append(i)
            # plt.scatter(j + 0.5, i, c='b')

    # for m in range(0, len(re), 2):
    for m in range(0, len(re)):
        x1 = re[m][0][0]
        y1 = re[m][0][1]
        x2 = re[m][1][0]
        y2 = re[m][1][1]
        # plt.scatter((x1 + x2) / 2, (y1 + y2) / 2, c='r')
        xx.append(((y1 + y2) / 2))
        yy.append(((x1 + x2) / 2))

        # for m in range(0, len(re_weak), 2):
    #     x1 = re_weak[m][0][0]
    #     y1 = re_weak[m][0][1]
    #     x2 = re_weak[m][1][0]
    #     y2 = re_weak[m][1][1]
    #     xx.append(((y1 + y2) / 2))
    #     yy.append(((x1 + x2) / 2))

    print(len(x))
    print(len(y))
    print(len(xx))
    print(xx)
    print(len(yy))
    print(yy)
    print(len(rex))
    print(len(rey))
    # plt.xlim((0, 500))
    # plt.xlim(0, 500,1)
    # plt.xticks(np.linspace(0, 500, 1))
    # plt.ylim(0, 500,1)
    # plt.yticks(np.linspace(0, 300, 300))
    # plt.xticks(np.linspace(0, 500, 500))
    # plt.scatter(x, y, c='b', s=0.01, marker=',')
    # plt.scatter(xx, yy, c='r', s=0.01, marker=',')
    # plt.scatter(rex, rey, c='black', s=0.01, marker=',')

    # 所有两两像素点的中点
    plt.scatter(x, y, s=0.1, c='b')

    # 明显区域分割点的中点
    plt.scatter(xx, yy, s=0.1, c='r')

    # 画出延伸点
    plt.scatter(rex, rey, s=0.1, c='black')
    plt.gca().invert_yaxis()
    plt.savefig("D:\\new" + src,
                dpi=1000)  # 指定分辨率保存
    plt.show()
    print("over")


def point_noise(noise):
    x = []
    y = []
    for i in range(noise.shape[0]):
        for j in range(noise.shape[1]):
            if noise[i, j] == 1:
                x.append(i)
                y.append(j)
    plt.scatter(y, x, s=0.1, c='r')
    plt.gca().invert_yaxis()
    plt.savefig("D:\\noise" + src,
                dpi=1000)  # 指定分辨率保存


#

# point_show(gray)


# src = "41004"
src = "beibu"
# inpath = "D:\\experiment\\pic\\q\\"
inpath = "D:\\in\\"
outpath = "D:\\out\\"

# gray = np.array([[100, 100, 100], [80, 80, 80], [80, 110, 80]])
raw = cv2.imread(inpath + src + ".jpg")
raw_Filter = raw
# raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = raw2
# raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
cv2.imwrite("D:\\gray.jpg", raw2_Filter)
np.savetxt("D:\\gray" + ".csv", raw2_Filter, fmt="%d", delimiter=',')

# re, re_weak = p2.cut(raw2_Filter, 20, 3)
# 大小两个阈值
re, re_weak, noise = p2.cut(raw2_Filter, 0, 1)
np.savetxt("D:\\fix_gray" + ".csv", raw2_Filter, fmt="%d", delimiter=',')
np.savetxt("D:\\noise" + ".csv", noise, fmt="%d", delimiter=',')

show = np.zeros((raw2.shape[0] * 2, raw2.shape[1] * 2))
# for m in range(0, len(re), 2):
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
    yy = ((y1 + y2))
    # xx = ((y1 + y2))
    # yy = ((x1 + x2))
    xx = ((x1 + x2))
    show[xx, yy] = 2
for k in range(0, len(re_weak)):
    x1 = re_weak[k][0][0]
    x2 = re_weak[k][1][0]
    y1 = re_weak[k][0][1]
    y2 = re_weak[k][1][1]
    # x2 = re[m + 1][1][0]
    # x2 = re[m + 1][1][0]
    # y2 = re[m + 1][1][1]
    # y2 = re[m + 1][1][1]
    # plt.scatter((x1 + x2) / 2, (y1 + y2) / 2, c='r')
    yy = ((y1 + y2))
    # xx = ((y1 + y2))
    # yy = ((x1 + x2))
    xx = ((x1 + x2))
    show[xx, yy] = 1

# x, y = p2.find_weak(show, show)
# print(x)
# print(y)
x = []
y = []
point_show(raw2_Filter, re, x, y)

np.savetxt("D:\\show" + ".csv", show, fmt="%d", delimiter=',')

point_noise(noise)
# plt.scatter([1, 2, 3], [2, 3, 4])
# plt.plot([1,2,2,4],[2,3,4,6])
# plt.show()
