import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
# src = "blur1041004"
src = "41004"
out = "D:\\out\\grab_cut\\"
img = cv.imread("D:\\experiment\\pic\\q\\"+src+".jpg")
mask = np.zeros(img.shape[:2],np.uint8)
# mask = cv.GC_FGD
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

# rect = (40,70,330,260)
# rect = (40,70,260,330)

rect = (70,40,330,260)
# rect = (200,40,100,200)
# 左上角像素点的坐标  第一个是列,第二个是行
# 选取长度 第一个是列的长,第二个是行的高
# rect = (70,40,260,330)
cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
# cv.grabCut(img,mask,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
# plt.imshow(img),plt.colorbar(),plt.show()
cv.imwrite(out+src+".jpg", img)
