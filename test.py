import numpy as np
import change
import cv2
import MyMarchingSquares
import matplotlib.pyplot as plt

gray = np.array([[10, 10, 10, 10], [10, 10, 11, 10], [10, 12, 5, 10], [10, 10, 10, 10]])

path = "D:\\experiment\\pic\\"
# path1 = "D:\\out\\41004__gradien.csv"
path1 = "D:\\out\\4.csv"
src = "8068"  # 天鹅

re = np.loadtxt(path1, dtype=np.int, delimiter=",")
x, y = MyMarchingSquares.traverse(MyMarchingSquares.labels_matrix(re, 1))
print(x)
print(y)
for i in range(0, len(x), 2):
    plt.plot([y[i], y[i + 1]], [x[i], x[i + 1]], color='black', lw=0.1)
    # print([x[i], x[i+1]], [y[i], y[i + 1]])
ax = plt.gca()
ax.invert_yaxis()  # y轴反向
plt.xticks([])
plt.yticks([])
plt.axis('off')
plt.savefig("D:\\test", dpi=500)  # 指定分辨率保存
plt.show()
