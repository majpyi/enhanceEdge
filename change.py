import cv2
src=cv2.imread("noise.jpg")
des = cv2.GaussianBlur(src,(5,5),0,0)
cv2.imwrite("des.jpg",des)