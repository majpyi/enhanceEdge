# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# def nothing(x):
#     pass
#
#
# cv2.namedWindow('image')
#
# img = cv2.imread('D:\\experiment\\pic\\q\\tran41004_2.jpg')
# cv2.namedWindow('image')
# cv2.createTrackbar('Er/Di', 'image', 0, 1, nothing)
# # 创建腐蚀或膨胀选择滚动条，只有两个值
# cv2.createTrackbar('size', 'image', 0, 21, nothing)
# # 创建卷积核大小滚动条
#
#
# while (1):
#     s = cv2.getTrackbarPos('Er/Di', 'image')
#     si = cv2.getTrackbarPos('size', 'image')
#     # 分别接收两个滚动条的数据
#     k = cv2.waitKey(1)
#
#     kernel = np.ones((si, si), np.uint8)
#     # 根据滚动条数据确定卷积核大小
#     erroding = cv2.erode(img, kernel)
#     dilation = cv2.dilate(img, kernel)
#     if k == 27:
#         break
#     # esc键退出
#     if s == 0:
#         cv2.imshow('image', erroding)
#     else:
#         cv2.imshow('image', dilation)
#         # 判断是腐蚀还是膨胀


import cv2
import numpy as np
import matplotlib.pyplot as plt


def nothing(x):
    pass


# src = "blur1041004ththth5noisenum1"
# src = "blur541004ththth10noisenum1"
src = "blur541004ththth10noisenum1"
# src = "41004ththth5noisenum1"
# src = "blur541004"
# img = cv2.imread("D:\\experiment\\pic\\q\\"+src+".jpg")

# src = "blur1041004ththth5noisenum1"
img = cv2.imread("D:\\out\\tranrgb\\"+src+".jpg")
raw2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(type(raw2))
print(type(raw2[0,0]))
# raw2 = np.loadtxt("D:\\out\\try\\guodu1____L0.csv", dtype=np.int, delimiter=",", encoding='utf-8')
raw2 = np.loadtxt("D:\\out\\try\\guodu1____L0.csv",dtype=np.uint8, delimiter=",", encoding='utf-8')
print(type(raw2))
print(type(raw2[0,0]))


img = raw2

si = 2

kernel = np.ones((si, si), np.uint8)
# 根据滚动条数据确定卷积核大小
erroding = cv2.erode(img, kernel)
dilation = cv2.dilate(img, kernel)
# 膨胀之后腐蚀


si = 0
kernel = np.ones((si, si), np.uint8)
dilationerroding = cv2.erode(dilation, kernel)


si = 0
kernel = np.ones((si, si), np.uint8)
errodingdilation = cv2.dilate(erroding, kernel)



cv2.imwrite("D:\\out\\errod\\"+src+".jpg", erroding)
cv2.imwrite("D:\\out\\dilaterrod\\"+src+".jpg", dilationerroding)
cv2.imwrite("D:\\out\\erroddiate\\"+src+".jpg", errodingdilation)
cv2.imwrite("D:\\out\\dilat\\"+src+".jpg", dilation)
np.savetxt("D:\\out\\errod\\"+src+".csv", erroding,fmt="%d", delimiter=',')
np.savetxt("D:\\out\\dilaterrod\\"+src+".csv", dilationerroding,fmt="%d", delimiter=',')
np.savetxt("D:\\out\\erroddiate\\"+src+".csv", errodingdilation,fmt="%d", delimiter=',')
np.savetxt("D:\\out\\dilat\\"+src+".csv", dilation,fmt="%d", delimiter=',')

