import numpy as np
import cv2

inpath = "D:\\out\\"
outpath = "D:\\out\\"

gradient = np.loadtxt(inpath + "bd.csv", dtype=np.int, delimiter=",", encoding='utf-8')
print(type(gradient))
print(gradient)
for i in range(gradient.shape[0]):
	for j in range(gradient.shape[1]):
		# print(gradient[i, j])
		# print(type(gradient[i, j]))
		# print(type(1))
		# if gradient[i, j] == 3:
		# 	gradient = 0
		if gradient[i, j] == 2:
			gradient[i, j] = 255
		elif gradient[i, j] == 1:
			gradient[i, j] = 0
		else:
			gradient[i, j] = 127
cv2.imwrite(outpath + "outpic" + ".jpg", gradient)
np.savetxt(outpath + "outpic.csv", gradient, fmt="%d", delimiter=',')


# def func(pa):
# 	def foo(n):
# 		return pa ** n
#
# 	return foo
#
#
# print (func(3)(3))
