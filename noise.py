import change
import numpy as np
import MyMarchingSquares
import matplotlib.pyplot as plt
import cv2
import modify

inpath = "D:\\in\\"
outpath = "D:\\out\\"
src = "a"

raw = cv2.imread(inpath + src + ".jpg")

raw = cv2.bilateralFilter(raw, 7, 50, 50)

# raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# cv2.imwrite(outpath + src + "__srcBil" + ".jpg", raw_Filter)
# raw = raw_Filter
# raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
np.savetxt("D:\\noise\\gray.csv", raw2, fmt="%d", delimiter=',')

cv2.imwrite("D:\\noise\\Canny.jpg", cv2.Canny(raw2, 100, 200))
# np.savetxt("D:\\noise\\Canny.csv", cv2.Canny(raw2, 100, 200), fmt="%d", delimiter=',')

raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
# cv2.imwrite(outpath + src + "_grayBil" + ".jpg", raw2_Filter)
# np.savetxt(outpath + src + '__grayBil' + '.csv', raw2_Filter, fmt="%d", delimiter=',')
raw2 = raw2_Filter
noise_num = 1
a, b, c, d, e = modify.noise_array(raw2, noise_num)
np.savetxt("D:\\noise\\noise.csv", a, fmt="%d", delimiter=',')

raw3 = change.fix_noise(raw2, a, 1)
cv2.imwrite("D:\\noise\\Canny_fix_noise.jpg", cv2.Canny(raw3, 100, 200))
np.savetxt("D:\\noise\\re.csv", raw3, fmt="%d", delimiter=',')

# for i in range(c.shape[0]):
#     for j in range(c.shape[1]):
#         if c[i, j] == 1:
#             c[i, j] = 255
# cv2.imwrite("D:\\guodu.jpg", c)

rows = raw2.shape

# raw3_f = cv2.bilateralFilter(raw2, 7, 50, 50)
# cv2.imwrite(outpath + src + "_grayBil" + ".jpg", raw2_Filter)
# np.savetxt(outpath + src + '__grayBil' + '.csv', raw2_Filter, fmt="%d", delimiter=',')
# raw2 = raw2_Filter

re = change.gradient_average(raw2, rows[0], rows[1], 1)
re[0, :] = re[rows[0] - 1, :] = re[:, 0] = re[:, rows[1] - 1] = 0
np.savetxt(outpath + src + "__gradien" + ".csv", re, fmt="%d", delimiter=',')

x, y = MyMarchingSquares.traverse(MyMarchingSquares.labels_matrix_new(re, 100, 0))

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

# plt.savefig("D:\\fix_noise__" + src + "___noise_num:"+str(noise_num), figsize=(width, length), facecolor='black',
#             dpi=500)  # 指定分辨率保存
plt.savefig("D:\\fix_noise" + src, figsize=(width, length), facecolor='black',
            dpi=500)  # 指定分辨率保存
plt.show()
