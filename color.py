import change
import numpy as np
import MyMarchingSquares
import matplotlib.pyplot as plt
import cv2
import modify

inpath = "D:\\in\\"
outpath = "D:\\out\\"
src = "2"

raw = cv2.imread(inpath + src + ".jpg")

raw = cv2.bilateralFilter(raw, 7, 50, 50)

# raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# cv2.imwrite(outpath + src + "__srcBil" + ".jpg", raw_Filter)
# raw = raw_Filter
# raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw2 = cv2.bilateralFilter(raw2, 7, 50, 50)

print(0)
# np.savetxt("D:\\noise\\gray.csv", raw2, fmt="%d", delimiter=',')

# cv2.imwrite("D:\\noise\\Canny.jpg", cv2.Canny(raw2, 100, 200))
# np.savetxt("D:\\noise\\Canny.csv", cv2.Canny(raw2, 100, 200), fmt="%d", delimiter=',')

# raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
# cv2.imwrite(outpath + src + "_grayBil" + ".jpg", raw2_Filter)
# np.savetxt(outpath + src + '__grayBil' + '.csv', raw2_Filter, fmt="%d", delimiter=',')
# raw2 = raw2_Filter
noise_num = 1
# a, b, c, d, e = modify.noise_array(raw2, noise_num)
# np.savetxt("D:\\noise\\noise.csv", a, fmt="%d", delimiter=',')

# raw3 = change.fix_noise(raw2, a, 1)
# cv2.imwrite("D:\\noise\\Canny_fix_noise.jpg", cv2.Canny(raw3, 100, 200))
# np.savetxt("D:\\noise\\re.csv", raw3, fmt="%d", delimiter=',')
#
# rows = raw2.shape

re = np.zeros((5,5,3))
print(1)
# 矛盾点   蓝色
for i in range(5):
    for j in range(5):
            re[i, j][0] = 255
# 内部点
# print(2)
# for i in range(c.shape[0]):
#     for j in range(c.shape[1]):
#         if c[i,j]!=1 and d[i,j]!=1 and e[i,j]!=1:
#             re[i,j][1]=255
# print(3)
# # 边缘点
# for i in range(d.shape[0]):
#     for j in range(d.shape[1]):
#         if d[i, j] == 1:
#             re[i, j][2] = 255
#         if e[i, j] == 1:
#             re[i, j][2] = 255
# # for i in range(e.shape[0]):
# #     for j in range(e.shape[1]):
# #         if e[i, j] == 1:
# #             re[i, j][2] = 255
# print(4)
cv2.imwrite("D:\\guodu.jpg", re)

# re = change.gradient_average(raw2, rows[0], rows[1], 1)
# re[0, :] = re[rows[0] - 1, :] = re[:, 0] = re[:, rows[1] - 1] = 0
# re1 = MyMarchingSquares.find_cross(MyMarchingSquares.labels_matrix_new(re, 30, 20))
# cv2.imwrite("D:\\cross.jpg", re1)
