import cv2

src = "101085"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\try\\" + src + "\\"
img01 = cv2.imread(inpath + src + ".jpg")
img01 = cv2.cvtColor(img01, cv2.COLOR_BGR2GRAY)

# 中值滤波
temp = img01
for i in range(20):
	img_medianBlur = cv2.medianBlur(temp, 5)
	temp = img_medianBlur
cv2.imwrite(outpath + "img_medianBlur ___" + src + ".jpg",temp)

# font = cv2.FONT_HERSHEY_SIMPLEX
# 均值滤波
temp = img01
for i in range(20):
	img_Blur = cv2.blur(temp , (5, 5))
	temp = img_Blur
cv2.imwrite(outpath + "img_Blur ___" + src + ".jpg", temp)

# 高斯滤波
temp = img01
for i in range(20):
	img_Blur = cv2.blur(temp , (5, 5))
	temp = img_Blur
img_GaussianBlur = cv2.GaussianBlur(img01, (7, 7), 0)
cv2.imwrite(outpath + "img_GaussianBlur ___" + src + ".jpg", temp)

# 高斯双边滤波
# img_bilateralFilter = cv2.bilateralFilter(img01, 40, 75, 75)
