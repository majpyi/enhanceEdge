# 以像素点作为分割边界
# 测试主函数
import p2
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
    if isinstance(j, int):
        gray[int(i + 0.5), j] = 1
        # gray[int(i - 0.5), j] = 1
    if isinstance(i, int):
        gray[i, int(j + 0.5)] = 1
        # gray[i, int(j - 0.5)] = 1


# 输入gray原始标记上图,i,j分别是横轴坐标,tag是区域划分的标记符号
# 作用:遍历25邻域,进行区域标记
def go_near(gray, i, j, tag, i_low, i_high, j_low, j_high):
    # if i + 1 > 4 or j + 1 > 4:
    #     return
    # if i - 1 < 0 or j - 1 < 0:
    #     return
    if i_low <= i + 1 <= i_high and j_low <= j <= j_high and gray[i + 1, j] == 0:
        gray[i + 1, j] = tag
        go_near(gray, i + 1, j, tag, i_low, i_high, j_low, j_high)
    if i_low <= i <= i_high and j_low <= j + 1 <= j_high and gray[i, j + 1] == 0:
        gray[i, j + 1] = tag
        go_near(gray, i, j + 1, tag, i_low, i_high, j_low, j_high)
    if i_high >= i - 1 >= i_low and j_low <= j <= j_high and gray[i - 1, j] == 0:
        gray[i - 1, j] = tag
        go_near(gray, i - 1, j, tag, i_low, i_high, j_low, j_high)
    if i_low <= i <= i_high and j_high >= j - 1 >= j_low and gray[i, j - 1] == 0:
        gray[i, j - 1] = tag
        go_near(gray, i, j - 1, tag, i_low, i_high, j_low, j_high)


# gray原始标记图,x,y是起始25邻域的左上坐标点
# 如果没有形成闭合的区域就去除该区域的标记
def fix_area(gray, x, y):
    for i in range(x, x + 5):
        for j in range(y, y + 5):
            gray[i, j] = 0


# gray原始的标记图,x,y起始25邻域的左上坐标点
# 判断该25邻域是给是有闭合区域
def verify_close(gray, x, y):
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
                go_near(gray, i, j, tag, i_low, i_high, j_low, j_high)
                tag += 1
    if tag == 3:
        fix_area(gray, x, y)
    else:
        print("2222")
    # print(tag)


src = "41004"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\"

raw = cv2.imread(inpath + src + ".jpg")
raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)

raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)

cv2.imwrite("D:\\gray.jpg", raw2_Filter)
np.savetxt("D:\\gray" + ".csv", raw2_Filter, fmt="%d", delimiter=',')

# re, re_weak = p2.cut(raw2_Filter, 20, 3)
# 大小两个阈值
re, re_weak, noise = p2.cut(raw2_Filter, 5, 6)
np.savetxt("D:\\fix_gray" + ".csv", raw2_Filter, fmt="%d", delimiter=',')

print(re)

gray = np.zeros((raw2.shape[0], raw2.shape[1]))

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
    if yy % 2 == 0:
        yy = int((y1 + y2) / 2)
        xx = (x1 + x2) / 2
    # xx = ((y1 + y2))
    # yy = ((x1 + x2))
    if xx % 2 == 0:
        xx = int((x1 + x2) / 2)
        yy = (y1 + y2) / 2
    print((xx, yy))
    fix_tag(gray, xx, yy)

np.savetxt("D:\\tag" + ".csv", gray, fmt="%d", delimiter=',')

for i in range(0, gray.shape[0] - 4, 4):
    for j in range(0, gray.shape[1] - 4, 4):
        verify_close(gray, i, j)
np.savetxt("D:\\re_local" + ".csv", gray, fmt="%d", delimiter=',')

for i in range(gray.shape[0]):
    for j in range(gray.shape[1]):
        if gray[i, j] == 1:
            gray[i, j] = 255
cv2.imwrite("D:\\re_local.jpg", gray)

re_x = []
re_y = []
print(re)
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
    if yy % 2 == 0:
        yy = int((y1 + y2) / 2)
        xx = (x1 + x2) / 2
    # xx = ((y1 + y2))
    # yy = ((x1 + x2))
    if xx % 2 == 0:
        xx = int((x1 + x2) / 2)
        yy = (y1 + y2) / 2
    if isinstance(yy, int) and gray[int(xx + 0.5), yy] == 255 and gray[int(xx - 0.5), yy] == 255:
        # gray[int(xx + 0.5), yy] = 0
        # gray[int(xx - 0.5), yy] = 0
        print(1)
        re_x.append(xx)
        re_y.append(yy)
    if isinstance(xx, int) and gray[xx, int(yy + 0.5)] == 255 and gray[xx, int(yy - 0.5)] == 255:
        # gray[xx, int(yy + 0.5)] = 0
        # gray[xx, int(yy - 0.5)] = 0
        print(2)
        re_x.append(xx)
        re_y.append(yy)

print(re_x)
print(re_y)
plt.scatter(re_y, re_x, s=0.1, c='r')
plt.gca().invert_yaxis()
plt.savefig("D:\\re_local_line" + src,
            dpi=1000)  # 指定分辨率保存



    # if gray[xx,yy] == 1:

# print(gray)
# fix_tag(gray, 2.5, 0)
# fix_tag(gray, 2.5, 1)
# fix_tag(gray, 2.5, 2)
# fix_tag(gray, 2.5, 3)
# fix_tag(gray, 2.5, 4)
# print(gray)
# verify_close(gray, 0, 0)
# print(gray)
