import cv2


for i in range(5,16,5):
    # 主函数
    src = "41004"
    inpath = "D:\\experiment\\pic\\q\\"
    # outpath = "D:\\out\\"
    raw = cv2.imread(inpath + src + ".jpg")
    th = i
    # raw2 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    # raw_Filter = cv2.GaussianBlur(raw, 7, 50, 50)
    # raw_Filter = cv2.medianBlur(raw,5)
    raw_Filter = cv2.blur(raw,(th,th))
    # raw_Filter = raw
    raw2 = cv2.cvtColor(raw_Filter, cv2.COLOR_BGR2GRAY)
    # raw2_Filter = cv2.GaussianBlur(raw2, 7, 50, 50)
    # raw2_Filter = cv2.medianBlur(raw2,5)
    raw2_Filter = cv2.blur(raw2,(th,th))


    cv2.imwrite("D:\\experiment\\pic\\q\\blur" +str(th)+ src + ".jpg", raw2_Filter)
