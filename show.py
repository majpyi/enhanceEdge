import numpy as np
import cv2

# src = "blur541004"
# src = "blur5precise1"
# src = "blur11precise1"
# src = "blur5bodleian_000000"
# src = "blur11ashmolean_000350"
#
# # src = "blur58068"
# # src = "blur8296059"
# guodu = np.loadtxt("D:\\out" + src + ".csv", dtype=np.int, delimiter=",", encoding='utf-8')
# # np.savetxt("D:\\out" + src + ".csv", re, fmt="%d", delimiter=',')
# for i in range(guodu.shape[0]):
#     for j in range(guodu.shape[1]):
#         guodu[i,j] = guodu[i,j]
# cv2.imwrite("D:\\out\\ex\\"+src+"out.jpg",guodu)

src = "8068"
# src = "41004"
# src = "241004"
# src = "296059"
# src = "ashmolean_000350"
# src = "blur8precise1"
# src = "circle2"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\tranrgb\\"
raw = cv2.imread(inpath + src + ".jpg")
raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# raw_Filter = cv2.bilateralFilter(raw, 7, 150, 150)
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)

tag = np.zeros((raw2.shape[0], raw2.shape[1]))


def smooth(tag, raw):
	xxx = [-1, -1, -1, 0, +1, +1, +1, 0]
	yyy = [+1, 0, -1, -1, -1, 0, +1, +1]
	for i in range(1, tag.shape[0] - 1):
		for j in range(1, tag.shape[1] - 1):
			sumr = 0
			sumg = 0
			sumb = 0
			num = 0
			if tag[i, j] == 0:
				sumr += raw[i, j][0]
				sumg += raw[i, j][1]
				sumb += raw[i, j][2]
				num += 1
				for k in range(8):
					if tag[i + xxx[k], j + yyy[k]] == tag[i, j]:
						sumr += raw[i + xxx[k], j + yyy[k]][0]
						sumg += raw[i + xxx[k], j + yyy[k]][1]
						sumb += raw[i + xxx[k], j + yyy[k]][2]
						num += 1
			if sumr != 0 or sumg != 0 or sumb != 0:
				raw[i, j][0] = int(sumr / num)
				raw[i, j][1] = int(sumg / num)
				raw[i, j][2] = int(sumb / num)


for i in range(100):
	smooth(tag, raw)

cv2.imencode('.jpg', raw)[1].tofile("D:\\out\\try\\直接平滑" + "___" + src + ".jpg")
