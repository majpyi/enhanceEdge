import numpy as np
import cv2
src = "blur1041004ththth3noisenum1"
# image = np.loadtxt("D:\\out\\tranrgb\\"+src+".csv", dtype=np.int, delimiter=",", encoding='utf-8')
image = np.loadtxt("D:\\out\\dilat\\"+src+".csv", dtype=np.int, delimiter=",", encoding='utf-8')
xx = [-1, -1, -1, 0, +1, +1, +1, 0, -1]
yy = [+1, 0, -1, -1, -1, 0, +1, +1, +1]
re = np.zeros((image.shape[0],image.shape[1]))

for i in range(1,image.shape[0]-1):
    for j in range(1,image.shape[1]-1):
        if image[i,j]>=200:
            count_0 = 0
            for k in range(len(xx)):
                if image[i+xx[k],j+yy[k]]<=10:
                    count_0+=1
            if count_0 ==7 or count_0==6:
                re[i,j] = 255
            else:
                re[i,j] = 60
cv2.imwrite("D:\\re.jpg",re)

re1 = re.copy()
src = "blur1041004ththth1noisenum1"
image = np.loadtxt("D:\\out\\dilat\\"+src+".csv", dtype=np.int, delimiter=",", encoding='utf-8')
for i in range(1,image.shape[0]-1):
    for j in range(1,image.shape[1]-1):
        if image[i,j]>=200 and re[i,j]!=255 and re[i,j]!=60:
            # count_0 = 0
            # for k in range(len(xx)):
            #     if image[i+xx[k],j+yy[k]]<=10:
            #         count_0+=1
            # if count_0 ==7 or count_0==6:
            #     re[i,j] = 255
            # else:
            #     re[i,j] = 60
            re1[i,j] = 120
cv2.imwrite("D:\\re1.jpg",re1)

re2 = re.copy()
src = "blur1041004ththth1noisenum1"
image = np.loadtxt("D:\\out\\tranrgb\\"+src+".csv", dtype=np.int, delimiter=",", encoding='utf-8')
for i in range(1,image.shape[0]-1):
    for j in range(1,image.shape[1]-1):
        if image[i,j]>=200 and re[i,j]!=255 and re[i,j]!=60:
            # count_0 = 0
            # for k in range(len(xx)):
            #     if image[i+xx[k],j+yy[k]]<=10:
            #         count_0+=1
            # if count_0 ==7 or count_0==6:
            #     re[i,j] = 255
            # else:
            #     re[i,j] = 60
            re2[i,j] = 120
cv2.imwrite("D:\\re2.jpg",re2)


re3 = re.copy()
src = "blur1041004ththth2noisenum1"
image = np.loadtxt("D:\\out\\tranrgb\\"+src+".csv", dtype=np.int, delimiter=",", encoding='utf-8')
for i in range(1,image.shape[0]-1):
    for j in range(1,image.shape[1]-1):
        if image[i,j]>=200 and re[i,j]!=255 and re[i,j]!=60:
            # count_0 = 0
            # for k in range(len(xx)):
            #     if image[i+xx[k],j+yy[k]]<=10:
            #         count_0+=1
            # if count_0 ==7 or count_0==6:
            #     re[i,j] = 255
            # else:
            #     re[i,j] = 60
            re3[i,j] = 120
cv2.imwrite("D:\\re3.jpg",re3)