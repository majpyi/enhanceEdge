import numpy as np
import change
import cv2

gray = np.array([[10, 10, 10, 10], [10, 10, 11, 10], [10, 12, 5, 10], [10, 10, 10, 10]])

path = ""
src = "example"
raw = cv2.imread(path + src + ".jpg")
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
rows = raw2.shape
np.savetxt('原图.csv', raw2, fmt="%d", delimiter=',')

# 原始的方法,大区域的最小值与小区域中的最大值进行相减
# re = change.gradient(raw2, rows[0], rows[1])
# np.savetxt('gradient.csv', re, fmt="%d", delimiter=',')


re = change.gradient_average(raw2, rows[0], rows[1])
np.savetxt('gradient.csv', re, fmt="%d", delimiter=',')

# 标记周围邻域小,而中心点大的边缘点
# re_tag = change.gradient_tag(re, rows[0], rows[1])
#
# cv2.imwrite("gradient_tag.jpg", re_tag)


# 判断这个点如果是边缘点的话,那么以他为中心的点的周围像素点的区分度的大小应该比他自身要小,因为只有在边缘处的区分度才是最大的
xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
yyy = [+1, 0, -1, -1, -1, 0, +1, +1]

re_tag = np.zeros((rows[0], rows[1]))

for i in range(1, rows[0] - 1):
    for j in range(1, rows[1] - 1):
        num = 0
        for k in range(8):
            if (re[i, j] > re[i + xxx[k], j + yyy[k]] and re[i, j] > 30):
                num += 1
        if (num >= 5):
            re_tag[i, j] = 255
        else:
            re_tag[i, j] = 0
cv2.imwrite("re_tag" + src + ".jpg", re_tag)
np.savetxt("re_tag" + src + ".csv", re_tag, fmt="%d", delimiter=',')

#  简单粗暴的只要区分度值大于一定的阈值就认为这个点事边缘点
# for i in range(1,rows[0]-1):
#     for j in range(1,rows[1]-1):
#         if (re[i, j] > 30):
#             re[i,j] = 255
#         else:
#             re[i,j] = 0


edge = change.extend_edge(re, 20)

cv2.imwrite("edge" + src + ".jpg", edge)
np.savetxt('edge.csv', edge, fmt="%d", delimiter=',')
