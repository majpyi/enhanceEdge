# threshold_march = 10
# import matplotlib.pyplot as plt
#
# # ax = plt.gca(figsize=(9, 3), dpi=100)
# # ax.figure()
# plt.figure(figsize=(3, 8),)
# # plt.figure(figsize=(6, 4),)
# # plt.figure(figsize(8, 6))
# plt.plot([1, 2], [3, 4])
# # plt.figure(figsize=(9, 3), dpi=100)
# plt.savefig("D:\\testconfig", figsize=(3.1, 8.1), dpi=500)  # 指定分辨率保存
# plt.show()
#
import numpy as np
import change
import cv2
import MyMarchingSquares
import matplotlib.pyplot as plt
import marchingsquares2


# gray = np.array([[10, 10, 10, 10], [10, 10, 11, 10], [10, 12, 5, 10], [10, 10, 10, 11],[10, 10, 10, 11]])
# print(len(gray))
# print(gray[:, -1] > 10)
# print(np.delete(gray, 2, 0))
# print(np.delete(gray, 1, 1))
# print(gray)
#
# path = "D:\\experiment\\pic\\"
# # path1 = "D:\\out\\41004__gradien.csv"
# path1 = "D:\\out\\2B9971ED33782C2C9F466FADAAB1A0C5__gradien.csv"
# # path1 = "D:\\out\\2.csv"
# src = "8068"  # 天鹅
#
# re = np.loadtxt(path1, dtype=np.int, delimiter=",")
# print(re.shape[0])
# print(re.shape[1])
# x = re.shape[0]
# y = re.shape[1]
# while x > 10 or y > 10:
#     x /= 10
#     y /= 10
# print(x)
# print(y)

















#
# path = "D:\\experiment\\pic\\"
# path1 = "D:\\out\\acs.csv"
# # path1 = "D:\\out\\2B9971ED33782C2C9F466FADAAB1A0C5__gradien.csv"
# # path1 = "D:\\out\\2.csv"
# src = "acs"
#
# re = np.loadtxt(path1, delimiter=",")
# # re = np.loadtxt(path1, delimiter=',', usecols=range(48))
# # re = np.genfromtxt(path1, delimiter=',')[:, :-1]
#
# x, y = MyMarchingSquares.traverse(MyMarchingSquares.labels_matrix(re, 20))
#
# length = re.shape[0]
# width = re.shape[1]
# while length > 10 or width > 10:
#     length /= 10
#     width /= 10
#
# # plt.xticks([])
# # plt.yticks([])
# plt.figure(figsize=(width, length), dpi=500)
# plt.gca().invert_yaxis()  # y轴反向
# # plt.axis('off')
#
# for i in range(0, len(x), 2):
#     # plt.plot([y[i], y[i + 1]], [x[i], x[i + 1]], color='white', lw=0.5)
#     plt.plot([y[i], y[i + 1]], [x[i], x[i + 1]], color='black', lw=0.5)
#
# # plt.savefig("D:\\fix_noise__" + src + "___noise_num:"+str(noise_num), figsize=(width, length), facecolor='black',
# #             dpi=500)  # 指定分辨率保存
# plt.savefig("D:\\cs____" + src, figsize=(width, length), facecolor='black',
#             dpi=500)  # 指定分辨率保存
# plt.show()
