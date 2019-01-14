import modify_rgb
import cv2
import numpy as np

src = "blur1041004"
inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\geodesic_distance\\"


raw = cv2.imread(inpath + src + ".jpg")
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# raw_Filter = raw
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)
# raw2_Filter = raw2
cv2.imwrite(outpath + src + ".jpg", raw2_Filter)
# np.savetxt("D:\\raw2" + src + ".csv", raw2_Filter, fmt="%d", delimiter=',')

noise_num = 1
th =5
a, b, guodu, d, e = modify_rgb.noise_array(raw2_Filter, raw_Filter,noise_num,th)
# a, b, guodu, d, e = modify_rgb.noise_array(raw2_Filter,noise_num,th)
# np.savetxt("D:\\guodu" + src + ".csv", guodu, fmt="%d", delimiter=',')
for i in range(guodu.shape[0]):
    for j in range(guodu.shape[1]):
        if guodu[i, j] == 1:
            guodu[i, j] = 100



re = modify_rgb.gradient_average_abs_rgb(raw2_Filter,raw_Filter,1)
np.savetxt(outpath + src + ".csv", raw2_Filter, fmt="%d", delimiter=',')
start_point = np.zeros((re.shape[0],re.shape[1]))
# 从右上逆时针
xx_tag = [-1, -1, -1, 0, +1, +1, +1, 0]
yy_tag = [+1, 0, -1, -1, -1, 0, +1, +1]
for i in range(1,re.shape[0]-1):
    for j in range(1,re.shape[1]-1):
        if guodu[i,j]==100:
            count = 0
            for k in range(8):
                if re[i,j]>re[i+xx_tag[k],j+yy_tag[k]]:
                    count+=1
            if count==8 and re[i,j] > 10:
                start_point[i,j] = 255
            else:
                start_point[i,j] =100
cv2.imwrite(outpath+src+"start_point.jpg",start_point)


# xx_tag = [-1, -1, -1, 0, +1, +1, +1, 0]
# yy_tag = [+1, 0, -1, -1, -1, 0, +1, +1]
# def short_distance(matrix,x1,y1,x2,y2):
#     re = matrix.copy()
#     list = []
#     for k in range(8):
#         if re[x1+xx_tag[k],y1+yy_tag[k]]:
