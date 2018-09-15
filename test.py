import modify
import numpy as np
import change
import cv2

gray = np.array([[10, 10, 10, 10], [10, 10, 11, 10], [10, 12, 5, 10], [10, 10, 10, 10]])

# noise ,a ,b= modify.point_classification(gray,2,2,1)
# print(noise)
# print(a)
# print(b)
# print(b[0])
# print(type(b[0][0]))
# print((b[0][0]))

path = ""
raw = cv2.imread(path + "4.jpg")
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
rows = raw2.shape

re = change.gradient(raw2, rows[0], rows[1])
np.savetxt('gradient.csv', re, fmt="%d", delimiter=',')

re_tag = change.gradient_tag(re, rows[0], rows[1])

cv2.imwrite("gradient_tag.jpg", re_tag)

for i in range(rows[0]):
    for j in range(rows[1]):
        if (re[i, j] > 5):
            re[i, j] = 255
        else:
            re[i, j] = 0

cv2.imwrite("gradient_re.jpg", re)