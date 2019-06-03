import cv2

for i in range(5, 6, 3):
	# 主函数
	# src = "41004"
	# src = "113016"
	# src = "8068"
	# src = "296059"
	# src = "precise1"
	# src = "bodleian_000000"
	# src = "ashmolean_000350"
	src = "square"
	src = "blur"
	inpath = "D:\\experiment\\pic\\batch\\"
	# outpath = "D:\\out\\"
	raw = cv2.imread(inpath + src + ".jpg")
	th = 10
	# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
	# raw_Filter = cv2.GaussianBlur(raw, 7, 50, 50)
	# raw_Filter = cv2.medianBlur(raw,5)
	# raw_Filter = cv2.blur(raw,(th,th))
	# raw_Filter = raw
	# raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
	raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
	# raw2_Filter = cv2.GaussianBlur(raw2, (th, th), 0)
	raw2_Filter = cv2.blur(raw2,(th,th))
	# raw2_Filter = cv2.medianBlur(raw2, th)

	# cv2.imwrite("D:\\experiment\\pic\\batch\\" + str(th) + "GaussianBlur" + src + ".jpg", raw2_Filter)
	cv2.imwrite("D:\\experiment\\pic\\batch\\" + str(th) + "blur1" + src + ".jpg", raw2_Filter)
	cv2.imwrite("D:\\experiment\\pic\\batch\\" + str(th) + "gray" + src + ".jpg", raw2)

# raw2_Filter = cv2.GaussianBlur(raw2, 7, (th,th))
# raw2_Filter = cv2.medianBlur(raw2,5)

# raw2_Filter = cv2.blur(raw2, (th, th))
# cv2.imwrite("D:\\experiment\\pic\\batch\\" + str(th)+"blur" + src + ".jpg", raw2_Filter)
