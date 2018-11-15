import numpy as np
import change
import cv2
import MyMarchingSquares
import marchingsquares2
import matplotlib.pyplot as plt
from PIL import Image

gray = np.array([[10, 10, 10, 10], [10, 10, 11, 10], [10, 12, 5, 10], [10, 10, 10, 10]])

path = "D:\\experiment\\pic\\"
path1 = "D:\\out\\bird.csv"
# path1 = "D:\\out\\2B9971ED33782C2C9F466FADAAB1A0C5__gradien.csv"
# path1 = "D:\\out\\2.csv"
src = "8068"  # 天鹅

re = np.loadtxt(path1, dtype=np.int, delimiter=",")
# x, y = MyMarchingSquares.traverse(re)

x, y = MyMarchingSquares.traverse(MyMarchingSquares.labels_matrix(re, 8))
# marchingsquares2.traverse(marchingsquares2.labels_matrix(re,10), "" + src)

print(x)
print(y)
print(re.shape[0])
print(re.shape[1])
length = re.shape[0]
width = re.shape[1]
while length > 10 or width > 10:
    length /= 10
    width /= 10

# ax = plt.gca()
# ax.invert_yaxis()  # y轴反向
# plt.figure(figsize=(8,6), dpi=80)
# plt.figure(figsize=(width, length))
# plt.xticks([])
# plt.yticks([])
# plt.figure(figsize=(width, length))
plt.figure( dpi=500)
# plt.figure(figsize=(width, length), dpi=500)
plt.gca().invert_yaxis()  # y轴反向

# plt.figure(figsize=(9, 3), dpi=100)
# ax.patch.set_facecolor('black')
# plt.rcParams['axes.facecolor']='red'
# plt.figure(facecolor='red',edgecolor='black')
# plt.axis('off')

for i in range(0, len(x), 2):
    # plt.plot([y[i], y[i + 1]], [x[i], x[i + 1]], color='white', lw=0.5)
    plt.plot([y[i], y[i + 1]], [x[i], x[i + 1]], color='black', lw=0.1)
    # print([x[i], x[i+1]], [y[i], y[i + 1]])


# ax = plt.gca()
# ax.invert_yaxis()  # y轴反向
# # plt.figure(figsize=(8,6), dpi=80)
# plt.figure( figsize=(3, 8),dpi=500)
# plt.xticks([])
# plt.yticks([])
# # plt.figure(figsize=(9, 3), dpi=100)
# # ax.patch.set_facecolor('black')
# # plt.rcParams['axes.facecolor']='red'
# # plt.figure(facecolor='red',edgecolor='black')
# plt.axis('off')


# plt.savefig("D:\\test", figsize=(width, length), facecolor='black', dpi=500)  # 指定分辨率保存
# plt.savefig("D:\\test", facecolor='black', dpi=500)  # 指定分辨率保存
plt.savefig("D:\\test",dpi=500)  # 指定分辨率保存
# plt.savefig("D:\\test", figsize=(3, 8), dpi=500)  # 指定分辨率保存
# plt.savefig("D:\\test", dpi=500)  # 指定分辨率保存
# plt.savefig("D:\\test", figsize=(re.shape[1]/100, re.shape[0]/100),facecolor='black', dpi=500)  # 指定分辨率保存
plt.show()
