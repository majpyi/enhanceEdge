import M
import numpy as np
from change import *

path = ""

src = cv2.imread(path + "2.jpg")
GaussianBlur = cv2.GaussianBlur(src, (11, 11), 0, 0)
medianBlur = cv2.medianBlur(src, 5)
cv2.imwrite("GaussianBlur.jpg", GaussianBlur)
cv2.imwrite("medianBlur.jpg", medianBlur)

raw = cv2.imread(path + "jaoyan.jpg")
raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
a, b, tagp = noise_array(raw2)
# tagp = np.zeros((3,3))
rows = raw2.shape

cv2.imwrite(path + "gray.jpg", raw2)
cv2.imwrite(path + "tagp.jpg", tagp)

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

totag = 0


# raws 原始图像  tagp 标记矛盾点 , n 方形结束位置 , end 剩余部分结束位置 , tag 标记行多还是列多
# while solve(raw2, tagp, n, end, tag, totag) == 1:
#     totag = 0
#     solve(raw2, tagp, n, end, tag, totag)

# while solve1(rows[0], rows[1], raw2, tagp, totag) == 1:
#     totag = 0
#     solve1(rows[0], rows[1], raw2, tagp, totag)

# solve(raw2, tagp, n, end, tag, totag)






# a = np.array( [[10, 10, 10], [10, 10, 10], [10, 10, 5]] )
# print(type(a))
# print(type(raw2))
# print(a)
noise = findSingleNoise(raw2,rows[0],rows[1])
# noise1 = findSingleNoise(a,3,3)

np.savetxt('a.csv', noise, fmt="%d", delimiter=',')
cv2.imwrite("singleNoise.jpg", noise)


gauss = map(raw2,rows[0],rows[1],noise)
cv2.imwrite("gauss.jpg", gauss)


cv2.imwrite("C.jpg", raw2)
np.savetxt('re.csv', raw2, fmt="%d", delimiter=',')
np.savetxt('raw.csv', raw, fmt="%d", delimiter=',')
np.savetxt('tagp.csv', tagp, fmt="%d", delimiter=',')
