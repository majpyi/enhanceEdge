import cv2

path = ""
raw = cv2.imread(path + "cs2.jpg")
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
re=cv2.Canny(raw2,200,250)
cv2.imwrite("Canny.jpg",re)
