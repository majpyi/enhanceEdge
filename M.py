import cv2
import numpy as np


# 边的能量
def line_energy(p1, p2):
    return (p1 - p2) * (p1 - p2)


# 根据中心点像素和与之的相对位置求八邻域点内的坐标
# 参数：中心像素点坐标，相对位置（从左上为0顺指针标记）,邻域个数
# 得到：邻域点像素
def find_index(i, j, x, num=8):
    ii = 0
    jj = 0
    if num == 8:
        if ((x == 0) | (x == 1) | (x == 2)):
            ii = i - 1
        if ((x == 4) | (x == 5) | (x == 6)):
            ii = i + 1
        if ((x == 3) | (x == 7)):
            ii = i

        if ((x == 0) | (x == 6) | (x == 7)):
            jj = j - 1
        if ((x == 2) | (x == 3) | (x == 4)):
            jj = j + 1
        if ((x == 1) | (x == 5)):
            jj = j
    if num == 16:
        if ((x == 0) | (x == 1) | (x == 2) | (x == 3) | (x == 4)):
            ii = i - 2
        if ((x == 5) | (x == 15)):
            ii = i - 1
        if ((x == 6) | (x == 14)):
            ii = i
        if ((x == 7) | (x == 13)):
            ii = i + 1
        if ((x == 8) | (x == 9) | (x == 10) | (x == 11) | (x == 12)):
            ii = i + 2

        if ((x == 0) | (x == 15) | (x == 14) | (x == 13) | (x == 12)):
            jj = j - 2
        if ((x == 1) | (x == 11)):
            jj = j - 1
        if ((x == 2) | (x == 10)):
            jj = j
        if ((x == 3) | (x == 9)):
            jj = j + 1
        if ((x == 4) | (x == 5) | (x == 6) | (x == 7) | (x == 8)):
            jj = j + 2
    return ii, jj


# 找八邻域点，组成列表
# 参数：灰度矩阵，像素点坐标,邻域个数
# 得到：邻域点(值)列表
def point_list(gray, i, j, num=8):
    if num == 8:
        lists = []  # 八邻域灰度值从左上开始沿顺时针方向排列
        addr = []  # 在gray中的坐标
        lists.extend(
            [gray[i - 1, j - 1], gray[i - 1, j], gray[i - 1, j + 1], gray[i, j + 1], gray[i + 1, j + 1], gray[i + 1, j],
             gray[i + 1, j - 1], gray[i, j - 1]])
        addr.extend(((i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1), (i + 1, j + 1), (i + 1, j), (i + 1, j - 1),
                     (i, j - 1)))
    if num == 16:
        lists = []  # 八邻域灰度值从左上开始沿顺时针方向排列
        addr = []
        lists.extend([gray[i - 2, j - 2], gray[i - 2, j - 1], gray[i - 2, j], gray[i - 2, j + 1], gray[i - 2, j + 2],
                      gray[i - 1, j + 2], gray[i, j + 2], gray[i + 1, j + 2], gray[i + 2, j + 2], gray[i + 2, j + 1],
                      gray[i + 2, j], gray[i + 2, j - 1], gray[i + 2, j - 2], gray[i + 1, j - 2], gray[i, j - 2],
                      gray[i - 1, j - 2]])
        addr.extend(((i - 2, j - 2), (i - 2, j - 1), (i - 2, j), (i - 2, j + 1), (i - 2, j + 2), (i - 1, j + 2),
                     (i, j + 2), (i + 1, j + 2), (i + 2, j + 2), (i + 2, j + 1), (i + 2, j), (i + 2, j - 1),
                     (i + 2, j - 2), (i + 1, j - 2), (i, j - 2), (i - 1, j - 2)))

    return lists, addr


# 邻域的最小能量
# 参数：邻域点列表值
# 得到：最小能量,a,b区点值的list 和 a，b区邻域的点的index（eg：0-7）
def least_energy(point_list):
    line = []  # 存放边的能量
    for p in range(-1, len(point_list) - 1):
        line.append(line_energy(int(point_list[p]), int(point_list[p + 1])))
    line_1 = line[:]  # 副本
    line_1.reverse()  # 倒序
    a = []
    b = []
    # 删掉两条能量最大的边
    #     print(line)
    large1_index = line.index(max(line))
    del line[large1_index]
    #     print(line)
    large2_index = line_1.index(max(line))  # 避免重复值位置重复！
    large2_index = len(point_list) - 1 - large2_index
    index2 = line.index(max(line))
    del line[index2]
    # 得到最小能量
    energy = sum(line)
    # A,B分区
    large_index = [large1_index, large2_index]
    large_index.sort()
    #     print(line)
    #     print(large_index[0])
    #     print(large_index[1])
    A = point_list[large_index[0]:large_index[1]]
    #     B =  [i for i in point_list if i not in A]
    #     B = []
    for i in range(len(point_list)):
        if (i >= large_index[0]) & (i < large_index[1]):
            a.append(i)
        else:
            b.append(i)
    for i in A:
        point_list.remove(i)
    return energy, A, point_list, a, b


# 邻域内定位最有可能的噪声
# 参数：灰度矩阵图，像素点坐标,邻域个数
# 得到：噪声像素在八邻域中的位置
def find_noise(gray, i, j, num=8):
    energy_list = []
    point_lists = point_list(gray, i, j, num)[0]
    #     print("point_list",point_list)
    for x in range(len(point_lists)):
        li = point_lists[:]
        del li[x]
        #         print(li)
        #         print(least_energy(li)[0])
        energy_list.append(least_energy(li)[0])
    #     print(energy_list)
    minn = energy_list.index(min(energy_list))
    return minn


# 每个八邻域内定位3个最有可能噪声点
# 参数：灰度矩阵图，中心像素坐标
# 得到：三个噪声点，A,B区与中心像素的坐标
def point_classification(gray, i, j, count, num=8):
    list_point = point_list(gray, i, j, num)[0]  # 初始的八邻域
    e_point_1 = list_point[:]  # 副本
    e_point = list_point[:]  # 副本
    e_point.reverse()
    point_lists = list_point[:]  # point_list作为副本，负责三次减去噪声
    minn = []  # 获取定位到的噪声在gray中的坐标
    rest_a = []  # 获取出3个噪声点外的a区点灰度值
    rest_b = []  # 获取出3个噪声点外的b区点灰度值
    a = []  # a区的index
    b = []  # b区的index
    noise = []  # 噪声的index
    while (count > 0):  # 计数3次
        energy_list = []  # 存储边的能量
        # 获取一个噪声
        for x in range(len(point_lists)):
            li = point_lists[:]
            lli = point_lists[:]
            del li[x]
            energy_list.append(least_energy(li)[0])
        noise_index = energy_list.index(min(energy_list))  # 得到噪声的领域index
        for ii in noise:
            # print('i=',i)
            if noise_index >= ii:
                noise_index = noise_index + 1
            else:
                break
        noise.append(noise_index)
        noise.sort()
        minn.append(find_index(i, j, noise_index, num))
        del point_lists[energy_list.index(min(energy_list))]  # 删去定位噪声，剩下的邻域为下一次定位噪声做准备
        count = count - 1
        if count == 0:
            least = least_energy(point_lists)
            rest_a.extend(least[3])
            rest_b.extend(least[4])
            for ii in rest_a:
                for iii in noise:
                    if ii >= iii:
                        ii = ii + 1
                a.append(find_index(i, j, ii, num))
            for ii in rest_b:
                for iii in noise:
                    if ii >= iii:
                        ii = ii + 1
                b.append(find_index(i, j, ii, num))
    return minn, a, b


# 遍历灰度矩阵并计数标记，噪声点+0，内部点+1，小边点+10，大边点+100,num为邻域个数
def score(gray, num=8):
    scores = np.zeros((gray.shape[0], gray.shape[1]))  # 初始化为0
    total_noise = []
    #     print(gray.shape[0])
    for k in range(0, gray.shape[0] - 1):
        for l in range(0, gray.shape[1] - 1):
            #             print(i)
            noise, a, b = point_classification(gray, k, l, 2, num)  # 根据中心像素点得到八邻域中的噪声，a,b区坐标
            total_noise.extend(noise)
            #             print(noise,a,b)
            num_a = []
            num_b = []
            for i in a:
                num_a.append(gray[i[0]][i[1]])
            for i in b:
                num_b.append(gray[i[0]][i[1]])

            #             if((len(num_b) == 0)|(len(num_a) == 0)):
            #                 print('AAAAAAAAA',k,l)
            # #                 gray[k][l] = 0
            # #                 continue
            #             print(num_a,num_b)
            #             print(type(a),type(max(num_a)),num_a ,num_b,type(int(max(num_a)-min(num_b))))
            if ((min(num_a) > max(num_b)) & (max(num_a) - min(num_b) > 15)):  # a区的点设为大边点, b区为小边点, 5为假设！！！！！！！！！！！！！！！！！
                for i in a:
                    scores[i[0]][i[1]] = scores[i[0]][i[1]] + 100
                for i in b:
                    scores[i[0]][i[1]] = scores[i[0]][i[1]] + 10
            elif ((min(num_b) > max(num_a)) & (max(num_b) - min(num_a) > 15)):  # b区的点设为大边点，a区为小边点
                for i in a:
                    scores[i[0]][i[1]] = scores[i[0]][i[1]] + 10
                for i in b:
                    scores[i[0]][i[1]] = scores[i[0]][i[1]] + 100
            elif (((min(num_a) > max(num_b)) & (max(num_a) - min(num_b) <= 15)) | (
                    (min(num_b) > max(num_a)) & (max(num_b) - min(num_a) <= 15)) | (
                          (max(num_a) > min(num_b)) & (min(num_b) > min(num_a))) | (
                          (max(num_b) > min(num_a)) & (min(num_a) > min(num_b)))):  # a,b算内部点，
                for i in a:
                    #                     print(scores[i[0]][i[1]])
                    scores[i[0]][i[1]] = scores[i[0]][i[1]] + 1.0
                for i in b:
                    scores[i[0]][i[1]] = scores[i[0]][i[1]] + 1.0
    return scores, total_noise


# 参数：灰度矩阵图
# 得到：噪声矩阵，积分矩阵, 矛盾点二值矩阵
def noise_array(gray, num=8):
    count = 0
    noise = np.zeros((gray.shape[0], gray.shape[1]))  # 初始化为0
    score_array_1 = score(gray, num)[0][0:gray.shape[0], 0:gray.shape[1]]  # 有值
    score_array_2 = np.zeros((score_array_1.shape[0], score_array_1.shape[1], 5))  # 全0
    contradiction_array = np.zeros((score_array_1.shape[0], score_array_1.shape[1]))
    for i in range(score_array_1.shape[0]):
        for j in range(score_array_1.shape[1]):
            #             print(i,j)
            score_array_2[i][j][0] = score_array_1[i][j] // 100  # [0, 0, 0]中第一个值 大边点
            score_array_2[i][j][1] = score_array_1[i][j] // 10 % 10  # 小边点
            score_array_2[i][j][2] = score_array_1[i][j] % 10  # 内部点
            score_array_2[i][j][3] = list(score_array_2[i][j]).index(max(score_array_2[i][j][0:3]))  # 存放前三值最大的所在的地址
            if score_array_2[i][j][0] * score_array_2[i][j][1] > 0:
                contradiction_array[i][j] = 255
                score_array_2[i][j][4] = 1  # 标记是否为矛盾点
            else:
                contradiction_array[i][j] = 0
            count_noise = num - score_array_2[i][j][0] - score_array_2[i][j][1] - score_array_2[i][j][2]
            noise[i][j] = count_noise
            if noise[i][j] < 0:
                count += 1
    #                 print( score_array_2[i][j])
    return noise, score_array_2, contradiction_array  # ,count


# 得到噪声矩阵的二值表示
def binary_noise(gray):
    noise = noise_array(gray)[0]
    noise2 = np.zeros((gray.shape[0] - 4, gray.shape[1] - 4))  # 初始化为0
    for i in range(noise.shape[0]):
        for j in range(noise.shape[1]):
            if noise[i][j] >= 7:
                noise2[i][j] = 1
    return noise2