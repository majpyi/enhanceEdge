import MyMarchingSquares
import matplotlib.pyplot as plt
import numpy as np

th = 15
src2 = "lu1.csv"
path1 = "D:\\out\\" + src2

re = np.loadtxt(path1, delimiter=',')

x, y = MyMarchingSquares.traverse_new(MyMarchingSquares.labels_matrix(re, 15))
print(x)
print(y)
length = re.shape[0]
width = re.shape[1]
while length > 10 or width > 10:
    length /= 10
    width /= 10
plt.xticks([])
plt.yticks([])
plt.figure(figsize=(width, length), dpi=500)
plt.gca().invert_yaxis()  # y轴反向
plt.axis('off')
for i in range(0, len(x), 2):
    plt.plot([y[i], y[i + 1]], [x[i], x[i + 1]], color='white', lw=0.5)
plt.savefig("D:\\noise\\extendCs__" + str(th) + "__", figsize=(width, length), facecolor='black',
            dpi=500)  # 指定分辨率保存
plt.show()
