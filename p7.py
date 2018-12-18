import cv2
import numpy as np
import p6rgb
import matplotlib.pyplot as plt

# src = "41004"
# inpath = "D:\\experiment\\pic\\q\\"

# raw = cv2.imread(inpath + src + ".jpg")
# np.savetxt("D:\\sample\\" + src + "1.csv", raw[:, :, 0], fmt="%d", delimiter=',')
# np.savetxt("D:\\sample\\" + src + "2.csv", raw[:, :, 1], fmt="%d", delimiter=',')
# np.savetxt("D:\\sample\\" + src + "3.csv", raw[:, :, 2], fmt="%d", delimiter=',')
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
# np.savetxt("D:\\sample\\" + src + "gray.csv", raw2, fmt="%d", delimiter=',')


# raw2_Filter = np.loadtxt("D:\\cs.csv", dtype=np.int, delimiter=",", encoding='utf-8')
# print(raw2_Filter)
# p6rgb.fix_transition(raw2_Filter,0,0)
# np.savetxt("D:\\csfix" + ".csv", raw2_Filter, fmt="%d", delimiter=',')
# print(raw2_Filter)


# x = [6, 6, 6, 7, 5, 8, 1, 2]
# y = [0, 1, 1, 3, 3, 5, 1, 2]
#
# plt_x = []
# plt_y = []
# plt_x.append(x[0])
# plt_x.append(x[1])
# plt_y.append(y[0])
# plt_y.append(y[1])
# for i in range(2, len(x) - 1, 2):
#     if x[i - 1] == x[i] and y[i - 1] == y[i]:
#         plt_x.append(x[i])
#         plt_x.append(x[i + 1])
#         plt_y.append(y[i])
#         plt_y.append(y[i + 1])
#     else:
#         print(1)
#         plt.plot(plt_y, plt_x, lw=0.5)
#         plt_x = []
#         plt_y = []
#         plt_x.append(x[i])
#         plt_x.append(x[i + 1])
#         plt_y.append(y[i])
#         plt_y.append(y[i + 1])
# plt.plot(plt_y, plt_x, lw=0.5)
# plt.show()



src = "41004"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\"

raw = cv2.imread(inpath + src + ".jpg")

# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)

raw_Filter = cv2.bilateralFilter(raw, 7, 5000, 50)
# raw_Filter = raw
# raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
# raw2_Filter = raw2
# raw2_Filter = cv2.bilateralFilter(raw2, 7, 150, 50)

cv2.imwrite("D:\\cs_bil" + src + ".jpg", raw_Filter)