import cv2
import numpy as np
import modify_rgb
from thin import Two, Xihua, array


#  获取原始数据
# src = "8068"
# src = "f"
# src = "41004"
# src = "241004"
# src = "296059"
src = "L0"
# src = "ashmolean_000350"
# src = "blur8precise1"
# src = "circle2"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\tranrgb\\"
raw = cv2.imread(inpath + src + ".jpg")
raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# raw_Filter = cv2.bilateralFilter(raw, 7, 150, 150)
# raw_Filter = raw
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
# raw2_Filter = raw2
# raw2_Filter = cv2.bilateralFilter(raw2, 7, 150, 150)
cv2.imwrite("D:\\out\\try\\raw_Filter" + "___" + src + ".jpg", raw_Filter)
cv2.imwrite("D:\\out\\try\\raw2" + "___" + src + ".jpg", raw2)
cv2.imwrite("D:\\out\\try\\raw2_Filter" + "___" + src + ".jpg", raw2_Filter)

# 获取过渡区域
noise_num = 2
th = 20
a, b, guodu, d, e = modify_rgb.noise_array(raw2_Filter, raw_Filter, noise_num, th)
th2 = 20
# a2, b2, guodu2, d2, e2 = modify_rgb.noise_array(raw2_Filter, raw_Filter, noise_num, th2)
guodu2 = guodu

for i in range(guodu.shape[0]):
	for j in range(guodu.shape[1]):
		if guodu[i, j] == 1:
			guodu[i, j] = 255
for i in range(guodu2.shape[0]):
	for j in range(guodu2.shape[1]):
		if guodu2[i, j] == 1:
			guodu2[i, j] = 255

cv2.imencode('.jpg', guodu)[1].tofile("D:\\out\\try\\寻找过渡区域" + str(th) + "___" + src + ".jpg")
cv2.imencode('.jpg', guodu)[1].tofile("D:\\out\\try\\寻找过渡区域22222" + str(th2) + "___" + src + ".jpg")

#  进行腐蚀和膨胀
si = 3
kernel = np.ones((si, si), np.uint8)
dilation = cv2.dilate(guodu, kernel)
cv2.imencode('.jpg', dilation)[1].tofile("D:\\out\\try\\膨胀" + str(th) + "___" + src + ".jpg")
np.savetxt("D:\\out\\try\\膨胀" + str(th) + "___" + src + ".csv", dilation, fmt="%d", delimiter=',')



si2 = 2
kernel2 = np.ones((si2, si2), np.uint8)
dilation2 = cv2.dilate(guodu2, kernel2)
iTwo = Two(dilation2)
iThin = Xihua(iTwo, array)
# iThin = cv2.dilate(iThin, kernel)
np.savetxt("D:\\out\\try\\iThin" + str(th) + "___" + src + ".csv", iThin, fmt="%d", delimiter=',')
cv2.imencode('.jpg', iThin)[1].tofile("D:\\out\\try\\iThin" + str(th) + "___" + src + ".jpg")
#
# for i in range(iTwo.shape[0]):
# 	for j in range(iTwo.shape[1]):
# 		if iThin[i, j] == 0:
# 			dilation[i, j] = 255
# 	# else:
# 	# 	dilation[i, j] = 0
# cv2.imencode('.jpg', dilation)[1].tofile("D:\\out\\try\\膨胀加瘦身结合" + str(th) + "___" + src + ".jpg")
# np.savetxt("D:\\out\\try\\膨胀加瘦身结合" + str(th) + "___" + src + ".csv", dilation, fmt="%d", delimiter=',')