import modify
import numpy as np


def gradient_average(raws, x, y):
    re = np.zeros((x, y))
    i = 87
    j = 205
    noise, a, b = modify.point_classification(raws, i, j, 1)
    point_a = []
    point_b = []
    sum_a = 0
    num_a = 0
    sum_b = 0
    num_b = 0
    for k in range(len(a)):
        point_a.append(raws[a[k][0], a[k][1]])
        sum_a += raws[a[k][0], a[k][1]]
        num_a += 1
    for k in range(len(b)):
        point_b.append(raws[b[k][0], b[k][1]])
        sum_b += raws[b[k][0], b[k][1]]
        num_b += 1
    maxa = max(point_a)  # 两个区域的的四个极值
    maxb = max(point_b)
    mina = min(point_a)
    minb = min(point_b)
    if maxa >= maxb and mina <= maxb:
        re[i, j] = 0
    elif maxb >= maxa and minb <= maxa:
        re[i, j] = 0
    else:
        avg_a = sum_a / num_a
        avg_b = sum_b / num_b
        if abs(raws[i, j] - avg_a) > abs(raws[i, j] - avg_b):
            re[i, j] = avg_b - avg_a
            if i == 87 and j == 205:
                print(a)
                print(avg_a)
                print(b)
                print(avg_b)
        if abs(raws[i, j] - avg_a) < abs(raws[i, j] - avg_b):
            re[i, j] = avg_a - avg_b
            if i == 87 and j == 205:
                print(a)
                print(avg_a)
                print(b)
                print(avg_b)
    return re
