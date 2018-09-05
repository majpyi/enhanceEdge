import M
import numpy as np
from change import *


path = ""


src=cv2.imread(path+"2.jpg")
GaussianBlur = cv2.GaussianBlur(src,(5,5),0,0)
medianBlur = cv2.medianBlur(src,5)
cv2.imwrite("GaussianBlur.jpg",GaussianBlur)
cv2.imwrite("medianBlur.jpg",medianBlur)


raw = cv2.imread(path+"a.jpg")
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
a, b, tagp = noise_array(raw2)
rows = raw2.shape

cv2.imwrite(path+"gray.jpg", raw2)
cv2.imwrite(path+"tagp.jpg", tagp)

tag = 0
n = 0
end = 0
if rows[0] > rows[1]:
    tag = 0
    n = rows[1]
    end = rows[0]
else:
    tag = 1
    n = rows[0]
    end = rows[1]

# raws 原始图像  tagp 标记矛盾点 , n 方形结束位置 , end 剩余部分结束位置 , tag 标记行多还是列多
while solve(raw2,tagp,n,end,tag) == 0:
    solve(raw2, tagp, n, end, tag)

# solve(raw2)


cv2.imwrite("C.jpg", raw2)
np.savetxt('re.csv', raw2, fmt="%d", delimiter=',')
np.savetxt('raw.csv', raw, fmt="%d", delimiter=',')
np.savetxt('tagp.csv', tagp, fmt="%d", delimiter=',')
