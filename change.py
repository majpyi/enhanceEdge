import cv2
from M import *

src=cv2.imread("2.jpg")
GaussianBlur = cv2.GaussianBlur(src,(5,5),0,0)
medianBlur = cv2.medianBlur(src,5)
cv2.imwrite("GaussianBlur.jpg",GaussianBlur)
cv2.imwrite("medianBlur.jpg",medianBlur)



# path = "/home/m/Desktop/"
# raw = cv2.imread(path + "4.jpg")
raw = cv2.imread("a.jpg")
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
a, b, tagp = noise_array(raw2)
rows = raw2.shape

cv2.imwrite("gray.jpg", raw2)
cv2.imwrite("tagp.jpg", tagp)

tag = 0
n = 0
end = 0
if rows[0] > rows[1]:
    tag = 0
    n = rows[1]
    end = rows[0]
else:
    tag = 1
    n = rows[0]
    end = rows[1]

nx = [-1, -1, -1, 0, 0, +1, +1, +1]
ny = [-2, -1, 0, -2, -1, -2, -1, 0]


# 处理过程,每当遇到被标记为矛盾的点就进行处理修正.
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
    if (minNum == 0):
        raw2[i, j] = maxSum / maxNum
    if (maxNum == 0):
        raw2[i, j] = minSum / minNum

    if (minNum != 0 and maxNum != 0):
        if (abs(raw2[i, j] - max) > abs(raw2[i, j] - min)):
            raw2[i, j] = minSum / minNum
            tagp[i, j] = 0
        else:
            raw2[i, j] = maxSum / maxNum
            tagp[i, j] = 0



def changeTest(raw2, i, j, tagp,test):
    pos = 0
    min = 256
    max = -1
    minSum = 0
    maxSum = 0
    minNum = 0
    maxNum = 0

    for m in range(8):
        print(raw2[i+nx[m],j+ny[m]])

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
            print(raw2[i,j])
        else:
            raw2[i, j] = maxSum / maxNum
            tagp[i, j] = 0
            print(raw2[i, j])
    print(str(minSum)+"  "+str(minNum)+"  "+str(maxSum)+"  "+str(maxNum))





hx = [-1, 0, 0, +1]
hy = [0, -1, +1, 0]

lx = [-1, -1, +1, +1]
ly = [-1, +1, -1, +1]


def change2(raw2, i, j, tagp):
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
    if (tag < 4):
        raw2[i, j] = raw[i + hx[tag], j + hy[tag]]
        tagp[i, j] = 0


# 进行从边界旋转,每次增加一行,并处理行列不相等,多余的空行
def solve(raw2):
    gotag = 0
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
            for k in range(1, rows[1] - 1):
                if tagp[j, k] == 255:
                    change(raw2, j, k, tagp)
                    gotag = 1
                # print(raw2[j, k], end=" ")
        if tag == 1:
            for k in range(1, rows[0] - 1):
                if tagp[k, j] == 255:
                    change(raw2, k, j, tagp)
                    gotag = 1
                # print(raw2[k, j], end=" ")
    return gotag



#
# def solve(raw2):
#     for i in range(8):
#






