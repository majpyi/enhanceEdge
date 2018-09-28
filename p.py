import cv2
import modify
import matplotlib.pyplot as plt
import change
import numpy as np

# gray = np.array([[10, 10, 10, 10], [10, 10, 11, 10], [10, 12, 5, 10], [10, 10, 10, 10]])
# gray = np.array([[87, 87, 87], [87, 87, 87], [86, 85, 85]])

src="41004"
inpath = "D:\\in\\"
outpath = "D:\\out\\"

raw = cv2.imread(inpath + src + ".jpg")
raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)


raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)

# noise, a, b = modify.point_classification(raw2_Filter, 73, 253, 2)
# print(a)
#
# print(b)

#
# plt.plot([5, 10], [1, 2], [1, 2], [6, 20])
# plt.plot([5, 10], [6, 20])
# plt.plot([1, 2], [3, 4])
# plt.show()


# marching_filter = change.marching_filter(re, threshold_march)
# np.savetxt(outpath + src + "___" + str(threshold_march) + "__marching_" + ".csv", marching_filter, fmt="%d",
#            delimiter=',')
# marching_re, vector_re = change.marching_squares(marching_filter)
# cv2.imwrite(outpath + src + "___" + str(threshold_march) + "__marching_" + ".jpg", marching_re)
# np.savetxt(outpath + src + "___" + str(threshold_march) + "__marching_" + ".csv", marching_re, fmt="%d",
#            delimiter=',')
#
# for x in range(len(vector_re), 4):
#     plt.plot([vector_re[x], vector_re[x + 2]], [vector_re[x + 1], vector_re[x + 3]])
# plt.show()

# n, a, b = modify.point_classification(gray, 1, 1,2)
# print(a)
# print(b)
