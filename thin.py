import cv2 as cv
import numpy as np
import sys

sys.setrecursionlimit(100000)


def VThin(image, array):
    # h = image.height
    # w = image.width
    h = image.shape[0]
    w = image.shape[1]
    NEXT = 1
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if NEXT == 0:
                NEXT = 1
            else:
                M = image[i, j - 1] + image[i, j] + image[i, j + 1] if 0 < j < w - 1 else 1
                if image[i, j] == 0 and M != 0:
                    a = [0] * 9
                    for k in range(3):
                        for l in range(3):
                            if -1 < (i - 1 + k) < h and -1 < (j - 1 + l) < w and image[i - 1 + k, j - 1 + l] == 255:
                                a[k * 3 + l] = 1
                    sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                    image[i, j] = array[sum] * 255
                    if array[sum] == 1:
                        NEXT = 0
    return image


def HThin(image, array):
    # h = image.height
    # w = image.width
    h = image.shape[0]
    w = image.shape[1]
    NEXT = 1
    for j in range(1, w - 1):
        for i in range(1, h - 1):
            if NEXT == 0:
                NEXT = 1
            else:
                M = image[i - 1, j] + image[i, j] + image[i + 1, j] if 0 < i < h - 1 else 1
                if image[i, j] == 0 and M != 0:
                    a = [0] * 9
                    for k in range(3):
                        for l in range(3):
                            if -1 < (i - 1 + k) < h and -1 < (j - 1 + l) < w and image[i - 1 + k, j - 1 + l] == 255:
                                a[k * 3 + l] = 1
                    sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                    image[i, j] = array[sum] * 255
                    if array[sum] == 1:
                        NEXT = 0
    return image


def Xihua(image, array, num=10):
    # iXihua = cv.CreateImage(cv.GetSize(image), 8, 1)
    # cv.Copy(image, iXihua)
    iXihua = image.copy()
    for i in range(num):
        VThin(iXihua, array)
        HThin(iXihua, array)
    return iXihua


def Two(image):
    w = image.shape[0]
    h = image.shape[1]
    # size = (w, h)
    # iTwo = cv.CreateImage(size, 8, 1)
    iTwo = np.zeros((w, h))
    for i in range(w):
        for j in range(h):
            iTwo[i, j] = 0 if image[i, j] > 200 else 255
    return iTwo


array = [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, \
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, \
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, \
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, \
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, \
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, \
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, \
         1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0]



#
# # image = cv.LoadImage('D://blurblur.jpg', 0)
# # src = "blur1041004"
# # src = "blur1041004ththth10noisenum1"
# # src = "41004ththth5noisenum1"
# # src = "blur541004ththth5noisenum1"
# # src = "blur58068ththth10noisenum1"
# src = "blur541004ththth10noisenum1"
# # image = np.loadtxt("D:\\dilat.csv", dtype=np.int, delimiter=",", encoding='utf-8')
# image = np.loadtxt("D:\\out\\dilat\\" + src + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')
#
# # raw = cv.imread("D://"+src+".jpg")
# # image= cv.cvtColor(raw, cv.COLOR_BGR2GRAY)
#
# iTwo = Two(image)
# iThin = Xihua(iTwo, array)
# # cv.imshow('image', image)
# # cv.imshow('iTwo', iTwo)
# # cv.imshow('iThin', iThin)
#
#
# cv.imwrite("D:\\out\\thin\\" + src + ".jpg", iThin)
# np.savetxt("D:\\out\\thin\\" + src + ".csv", iThin, fmt="%d", delimiter=',')
# # cv.waitKey(0)
#
#
#
#
#
#
# # 预处理
# xx_tag = [-1, -1, -1, 0, +1, +1, +1, 0]
# yy_tag = [+1, 0, -1, -1, -1, 0, +1, +1]
# iThin[:, 0] = 255
# iThin[0, :] = 255
# iThin[:, iThin.shape[1] - 1] = 255
# iThin[iThin.shape[0] - 1, :] = 255
#
# # 划分区域
# re_count = iThin.copy()
# count = 1
#
#
# def start_count(re_count, i, j, count):
#     for k in range(8):
#         if re_count[i + xx_tag[k], j + yy_tag[k]] == 0 and iThin[i + xx_tag[k], j + yy_tag[k]] == 0:
#             re_count[i + xx_tag[k], j + yy_tag[k]] = count
#             # start_count(re_count,i+xx_tag[k],j+yy_tag[k],count=+1)
#             start_count(re_count, i + xx_tag[k], j + yy_tag[k], count)
#         # count+=1
#
#
# for i in range(1, iThin.shape[0] - 1):
#     for j in range(1, iThin.shape[1] - 1):
#         if re_count[i, j] == 0:
#             re_count[i, j] = count
#             # count += 1
#             start_count(re_count, i, j, count)
#             count += 1
# np.savetxt("D:\\out\\thin\\count_" + src + ".csv", re_count, fmt="%d", delimiter=',')
#
# dict = {}
# #   准找区域起始点
# re = np.zeros((iThin.shape[0], iThin.shape[1]))
# for i in range(1, iThin.shape[0] - 1):
#     for j in range(1, iThin.shape[1] - 1):
#         if iThin[i, j] == 0:
#             sum0 = 0
#             for k in range(8):
#                 if iThin[i + xx_tag[k], j + yy_tag[k]] == 0:
#                     sum0 += 1
#             if sum0 == 1:
#                 re[i, j] = 255
#                 dict[(i, j)] = re_count[i, j]
#             else:
#                 re[i, j] = 100
# cv.imwrite("D:\\out\\thin\\start_" + src + ".jpg", re)
# np.savetxt("D:\\out\\thin\\start_" + src + ".csv", re, fmt="%d", delimiter=',')
#
# print(dict)
# sorted_dict = sorted(dict.items(), key=lambda item: item[1])
# print(sorted_dict)
# num = 1
# list_region = []
#
# # def count_length(re_count, i, j, count):
# #     count_num = 0
# #     for k in range(8):
# #         if re_count[i + xx_tag[k], j + yy_tag[k]] == 0 and iThin[i + xx_tag[k], j + yy_tag[k]] == 0:
# #             re_count[i + xx_tag[k], j + yy_tag[k]] = count
# #             # start_count(re_count,i+xx_tag[k],j+yy_tag[k],count=+1)
# #             start_count(re_count, i + xx_tag[k], j + yy_tag[k], count)
# #             count_num+=1
# #         if count_num==0:
# #
# #
# #
# # def find_length(re,start_point):
# #     re[start_point[0],start_point[1]]=1
# #     count_length()
# #
# #
# # def find_max_length(list_region):
# #     max_length = 0
# #     for i in range(len(list_region)):
# #         temp,other_point = find_length(iThin,list_region[i])
# #         if temp > max_length:
# #             max_length = temp
# #
# #
# # while len(sorted_dict) != 0:
# #     if sorted_dict[0][1] == num:
# #         list_region.append((sorted_dict[0][0]))
# #         sorted_dict.pop(0)
# #     else:
# #         s1, s2 = find_max_length(list_region)
# #         # retain_max_length(iThin,s1,s2)
# #         print(list_region)
# #         list_region = []
# #         num += 1
