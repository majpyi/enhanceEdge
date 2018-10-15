import numpy as np

# import math
xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
yyy = [+1, 0, -1, -1, -1, 0, +1, +1]


def isnext(a, b, src, tag):
    if ((abs(a[0] - b[0]) + abs(a[1] - b[1])) == 1 and tag[a[0], a[1]] == 0 and tag[b[0], b[1]] == 0 and src[
        a[0], a[1]] < 0 and src[b[0], b[1]] > 0):
        return True
    else:
        return False


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


tag = np.zeros((6, 7))
tag[1, 1] = 1
tag[1, 2] = 1
tag[2, 1] = -1
tag[2, 2] = -1
print(tag)
src = np.zeros((6, 7))
src[1, 3] = 8
src[2, 3] = -7
src[2, 4] = 8
src[3, 4] = -7
src[2, 5] = 6
src[1, 5] = -3
print(src)
a = extend_double(tag, src)
print(a)
