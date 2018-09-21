import cv2

path = ""
src = "cs3"
raw = cv2.imread(path + src + ".jpg")
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
threshold1 = 50
threshold2 = 100
re = cv2.Canny(raw2, threshold1, threshold2)
cv2.imwrite(src + str(threshold1) + str(threshold2) + "Canny.jpg", re)
