import change
import modify
import cv2
import numpy as np
import MyMarchingSquares
import matplotlib.pyplot as plt

inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\"
# src2 = "135069"
src2 = "41004"
# src2 = "cs"

# 双边滤波处理
raw = cv2.imread(inpath + src2 + ".jpg")
raw = cv2.bilateralFilter(raw, 7, 50, 50)
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw2 = cv2.bilateralFilter(raw2, 7, 50, 50)
np.savetxt(r"D:\\noise\\原始灰度图__" + src2 + ".csv", raw2, fmt="%d", delimiter=',')
raw2 = raw2

# 像素点进行分类处理
noise_num = 1
a, b, c, d, e = modify.noise_array(raw2, noise_num)
np.savetxt(r"D:\\noise\\原始的标记过渡区域__" + src2 + ".csv", c, fmt="%d", delimiter=',')

rows = raw2.shape
re = change.gradient_average(raw2, rows[0], rows[1], 1)
re[0, :] = re[rows[0] - 1, :] = re[:, 0] = re[:, rows[1] - 1] = 0
# 把不是矛盾点的并且区分度大于阈值的点标记为正负一
c = change.transition_tag(c, MyMarchingSquares.labels_matrix(re, 20))
np.savetxt(r"D:\\noise\\结合标记__" + src2 + ".csv", c, fmt="%d", delimiter=',')

# src = raw2.copy()
src1 = change.transition_area(raw2, c)
print(src1)
src = raw2
np.savetxt(r"D:\\noise\\c__" + src2 + ".csv", c, fmt="%d", delimiter=',')
np.savetxt(r"D:\\noise\\改变后的灰度图__" + src2 + ".csv", src, fmt="%d", delimiter=',')

# 对噪声点进行周围八邻域分区然后进行区域均值处理
src = change.fix_noise(src, a, 1)

re = change.gradient_average_new(src, rows[0], rows[1], 1)
re[0, :] = re[rows[0] - 1, :] = re[:, 0] = re[:, rows[1] - 1] = 0
np.savetxt(r"D:\\noise\\区分度图__" + src2 + ".csv", re, fmt="%d", delimiter=',')
th = 15
x, y = MyMarchingSquares.traverse_new(MyMarchingSquares.labels_matrix_new(re, 30, 0))

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
plt.savefig("D:\\noise\\fix_tran__" + str(th) + "__" + src2, figsize=(width, length), facecolor='black',
            dpi=500)  # 指定分辨率保存
plt.show()
