import change
import cv2
import matplotlib.pyplot as plt

# plt.rcParams['savefig.dpi'] = 300 #图片像素
# plt.rcParams['figure.dpi'] = 300 #分辨率
plt.rcParams['figure.figsize'] = (40, 20)

plt.plot([1, 2], [3, 4], color='r', lw=0.1)

# ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# change.pltshow()
# plt.savefig('D:\\plot123_2.png', dpi=300) #指定分辨率保存
plt.savefig('D:\\plot123_2.png', dpi=100) #指定分辨率保存

# plt.show()