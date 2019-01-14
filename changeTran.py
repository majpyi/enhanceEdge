import numpy as np
import transition_fixrgb
import cv2

src1 = "blur1041004ththth5noisenum1"
src = "blur1041004"
inpath = "D:\\experiment\\pic\\q\\"
# inpath = "D:\\"
outpath = "D:\\out\\fixtran\\"
raw = cv2.imread(inpath + src + ".jpg")
# raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
raw_Filter = cv2.bilateralFilter(raw, 7, 50, 50)
# raw_Filter = raw
raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
raw2_Filter = cv2.bilateralFilter(raw2, 7, 50, 50)

guodu = np.loadtxt("D:\\out\\dilat\\"+src1+".csv", dtype=np.int, delimiter=",", encoding='utf-8')

re = raw2_Filter.copy()
stop =  transition_fixrgb.change_tran(raw2_Filter, guodu,re)
while (stop == 1):
    stop = transition_fixrgb.change_tran(raw2_Filter, guodu,re)

# np.savetxt("D:\\raw2" + src + ".csv", raw2, fmt="%d", delimiter=',')
np.savetxt(outpath + src + ".csv", re, fmt="%d", delimiter=',')
# np.savetxt("D:\\guodu" + src + ".csv", guodu, fmt="%d", delimiter=',')
cv2.imwrite(outpath + src + ".jpg", re)