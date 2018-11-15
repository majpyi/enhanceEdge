import numpy as np
import modify
import changeTest
import cv2

inpath = "D:\\in\\"
outpath = "D:\\out\\"
src = "a"

# raw = cv2.imread(inpath + src + ".jpg")
# raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# cv2.imwrite(outpath + src + "__srcBil" + ".jpg", raw_Filter)
# raw = raw_Filter
# raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
# re = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)

# re = np.loadtxt(path1, dtype=np.int, delimiter=",")
# re = np.array([[120, 120, 120], [120, 100, 170], [140, 130, 160]])
re = np.array([[150, 150, 150], [120, 120, 120], [120, 140, 130]])

# no, a, b = modify.point_classification_new(re, 7, 72, 1)
# no, a, b = modify.point_classification_new(re, 1, 1, 2)
no, a, b = modify.point_classification_new(re, 1, 1, 6)
for x in no:
    print(re[x[0], x[1]], end=" ")
print()
# print(a)
for x in a:
    print(re[x[0], x[1]], end=" ")
print()
for x in b:
    print(re[x[0], x[1]], end=" ")
# print(b)
print()
# changeTest.gradient_average(re, re.shape[0], re.shape[1])
