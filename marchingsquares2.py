# coding: utf-8

# In[250]:


from numpy import *
import numpy as np
import cv2
import matplotlib.pyplot as plt
from pylab import *
import config




# 给原矩阵的值做标记值
# 方法：像素绝对值大于阈值的标记为原像素，小于阈值的根据正负分别标记为1，-1
# 参数：原矩阵，阈值
def labels_matrix(ori_matrix, value):
    x, y = ori_matrix.shape
    new_matrix = np.zeros((x, y))
    for i in range(x):
        for j in range(y):
            if abs(ori_matrix[i][j]) <= value:
                if ori_matrix[i][j] > 0:  # 0继续保持
                    new_matrix[i][j] = 1
                elif ori_matrix[i][j] < 0:
                    new_matrix[i][j] = -1
            elif abs(ori_matrix[i][j]) > value:
                new_matrix[i][j] = ori_matrix[i][j]
    return new_matrix

def labels_matrix1(ori_matrix, value ,min):
    x, y = ori_matrix.shape
    new_matrix = np.zeros((x, y))
    for i in range(x):
        for j in range(y):
            if min <= abs(ori_matrix[i][j]) <= value:
                if ori_matrix[i][j] > 0:  # 0继续保持
                    new_matrix[i][j] = 1
                elif ori_matrix[i][j] < 0:
                    new_matrix[i][j] = -1
            elif abs(ori_matrix[i][j]) > value:
                new_matrix[i][j] = ori_matrix[i][j]
    return new_matrix

# In[255]:


# 根据点(边)的序号0,1,2,3得到位与右侧中点坐标,画图原因，x,y与矩阵的x,y相反
def mid_point(num, ax, ay, bx, by, cx, cy, dx, dy):
    if num == 0:
        return ay, (ax + dx) / 2
    if num == 1:
        return (ay + by) / 2, ax
    if num == 2:
        return by, (bx + cx) / 2
    if num == 3:
        return (ay + by) / 2, dx


# In[256]:


# 找到以该点为左上角点的四边形,参数：矩阵，坐标
def get_squares(matrix, x, y):
    return matrix[x][y], matrix[x][y + 1], matrix[x + 1][y + 1], matrix[x + 1][
        y], x, y, x, y + 1, x + 1, y + 1, x + 1, y


# In[257]:


# 根据两个点找到下一个square（跟踪）
# 参数：矩阵,两个点在四个点中的序号，两个点的坐标
# return 四边形的四个点的值,以及四个点的坐标,以及这个线段在下一个四边形的边的序号
def find_next_sq(matrix, aindex, bindex, ax, ay, bx, by):
    i, j = matrix.shape
    aindex = int(aindex)
    bindex = int(bindex)
    indexs = []
    if aindex > bindex:
        big_index = aindex
        indexs = [ax, ay]
    else:
        big_index = bindex
        indexs = [bx, by]
    if (big_index == 1) & (aindex + bindex == 1):
        if bx == 0:
            return
        else:
            return get_squares(matrix, indexs[0] - 1, indexs[1] - 1), 3
    elif big_index == 2:
        if by == j - 1:
            return
        else:
            return get_squares(matrix, indexs[0] - 1, indexs[1]), 0
    elif (big_index == 3) & (aindex + bindex == 5):
        if bx == i - 1:
            return
        else:
            return get_squares(matrix, indexs[0], indexs[1]), 1
    elif ((big_index == 3) & (aindex + bindex == 3)):
        if by == 0:
            return
        else:
            return get_squares(matrix, indexs[0] - 1, indexs[1] - 1), 2
    elif ((big_index == 0) & (aindex + bindex == -1)):
        if by == 0:
            return
        else:
            return get_squares(matrix, indexs[0], indexs[1] - 1), 2


# In[286]:


# 对每个square标记中点然后画线
# 参数：四个点（顺时针）像素值，坐标
def squares_2(a, b, c, d, ax, ay, bx, by, cx, cy, dx, dy):
    labels = [a, b, c, d]  # 存放4个点的像素值
    indexs = [[ax, ay], [bx, by], [cx, cy], [dx, dy]]
    mid_points = []  # 存放用过的线中点的坐标
    spe_indexs = []  # 存放一端点为1/-1的两个点的序号，坐标
    #     print(labels)
    mul_list = [0] * 4  # 存放每条边两端点乘积
    mid_x = [0] * 4
    mid_y = [0] * 4
    for i in range(4):
        mul_list[i] = labels[i - 1] * labels[i]  # 乘前一个
    tag = 0  # 正负的边数
    flag = 0  # 是对否有要标记的点
    for i in mul_list:
        if i < 0:
            tag += 1
    #     print(mul_list,tag)
    if tag < 2:
        return
    else:
        for ii in range(4):  # 遍历边
            if mul_list[ii] < 0:  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<第一个条件：正负点之间才标中点
                if (abs(labels[ii]) > 1) & (abs(labels[ii - 1]) > 1):  # <<<<<<<<<<<<<<<第二个条件：当两个点的值的绝对值都大于阈值（>1）标记中点
                    mid_x[ii], mid_y[ii] = mid_point(ii, ax, ay, bx, by, cx, cy, dx, dy)  # 取中点
                    mid_points.append([mid_x[ii], mid_y[ii]])  # 存中点
                    flag = 1
                elif abs(labels[ii]) == 1:  # <<<<<<第三个条件：其中有一个点为-1/1
                    if ((mul_list[(ii + 2) % 4] < 0) & (abs(labels[(ii + 1) % 4]) > 1) & (
                            abs(labels[(ii + 2) % 4]) > 1)) | (
                            (mul_list[(ii + 3) % 4] < 0) & (abs(labels[(ii + 2) % 4]) > 1) & (
                            abs(labels[(ii + 3) % 4]) > 1)):  # 剩余三点有两相邻点一正一负，且都大于阈值
                        #                         print("坐标！！",indexs[ii],indexs[ii-1],labels[ii],labels[ii-1])
                        spe_indexs.append([ii, ii - 1, indexs[ii], indexs[ii - 1]])
                        mid_x[ii], mid_y[ii] = mid_point(ii, ax, ay, bx, by, cx, cy, dx, dy)
                        mid_points.append([mid_x[ii], mid_y[ii]])
                        flag = 1
                elif abs(labels[(ii + 3) % 4]) == 1:
                    if ((mul_list[(ii + 1) % 4] < 0) & (abs(labels[(ii) % 4]) > 1) & (
                            abs(labels[(ii + 1) % 4]) > 1)) | (
                            (mul_list[(ii + 2) % 4] < 0) & (abs(labels[(ii + 1) % 4]) > 1) & (
                            abs(labels[(ii + 2) % 4]) > 1)):
                        #                        print("坐标！！",indexs[ii],indexs[ii-1],labels[ii],labels[ii-1])
                        spe_indexs.append([ii, ii - 1, indexs[ii], indexs[ii - 1]])
                        mid_x[ii], mid_y[ii] = mid_point(ii, ax, ay, bx, by, cx, cy, dx, dy)
                        mid_points.append([mid_x[ii], mid_y[ii]])
                        flag = 1
        # print(mid_x[ii],mid_y[ii])
        #                 elif (abs(labels[ii])==1)&(abs(labels[ii-1]) > 1):#<<<<<<第三个条件：其中有一个点为-1/1,另一个点的绝对值大于阈值
        #                     if (abs(labels[ii-2]) > 1)&(mul_list[ii-1] < 0):#绝对值大于阈值且相邻,两个点一正一负
        # #                         print("坐标！！",indexs[ii],indexs[ii-1],labels[ii],labels[ii-1])
        #                         final_indexs.append([ii,ii-1,indexs[ii],indexs[ii-1]])
        #                         flag = 1
        #                         mid_x[ii],mid_y[ii] = mid_point(ii,ax,ay,bx,by,cx,cy,dx,dy)
        #                 elif (abs(labels[ii]) > 1)&(abs(labels[ii-1]) == 1):
        #                     if (abs(labels[(ii+1)%4]) > 1)&(mul_list[(ii+1)%4] < 0):#绝对值大于阈值且相邻,两个点一正一负
        # #                         print("坐标！！",indexs[ii],indexs[ii-1],labels[ii],labels[ii-1])
        #                         final_indexs.append([ii,ii-1,indexs[ii],indexs[ii-1]])
        #                         flag = 1
        #                         mid_x[ii],mid_y[ii] = mid_point(ii,ax,ay,bx,by,cx,cy,dx,dy)
        #         print(mid_x,mid_y)
        mid_xx = []  # 去掉原来没用过的
        mid_yy = []
        for ii in range(4):
            if ((mid_x[ii] != 0) & (mid_y[ii] != 0)) | ((mid_x[ii] == 0) & (mid_y[ii] != 0)) | (
                    (mid_x[ii] != 0) & (mid_y[ii] == 0)):
                mid_xx.append(mid_x[ii])
                mid_yy.append(mid_y[ii])
        x = [[mid_xx[ii - 1], mid_xx[ii]] for ii in range(len(mid_xx))]
        y = [[mid_yy[ii - 1], mid_yy[ii]] for ii in range(len(mid_yy))]
        #         print(x,y)
        if len(mid_points) < 2:
            return
        elif len(mid_points) == 4:
            return
        else:
            return mid_points, spe_indexs, x, y


#         print(x,y)
#             for jj in range(len(x)):
#                 plt.plot(x[jj], y[jj], color='r')
#                 plt.scatter(x[jj], y[jj], color='b')
#             if flag == 1:
#                 return final_indexs,x,y
#             else:
#                 return


# In[287]:


# 对每个square标记中点然后画线(特殊情况)
# 参数：四个点（顺时针）像素值，坐标
def squares_2_2(a, b, c, d, ax, ay, bx, by, cx, cy, dx, dy):
    labels = [a, b, c, d]  # 存放4个点的像素值
    indexs = [[ax, ay], [bx, by], [cx, cy], [dx, dy]]
    mid_points = []  # 存放 有效边 的中点
    spe_indexs = []
    #     final_indexs = []
    #     print(labels)
    mul_list = [0] * 4  # 存放每条边两端点乘积
    mid_x = [0] * 4
    mid_y = [0] * 4
    for i in range(4):
        mul_list[i] = labels[i - 1] * labels[i]  # 乘前一个
    tag = 0  # 正负的边数
    flag = 0  # 是对否有要标记的点
    for i in mul_list:
        if i < 0:
            tag += 1
    #     print(mul_list)
    if tag < 2:
        return
    else:
        for ii in range(4):  # 遍历边
            if mul_list[ii] < 0:  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<第一个条件：正负点之间才标中点
                mid_x[ii], mid_y[ii] = mid_point(ii, ax, ay, bx, by, cx, cy, dx, dy)
                mid_points.append([mid_x[ii], mid_y[ii]])
                spe_indexs.append([ii, ii - 1, indexs[ii], indexs[ii - 1]])
                flag = 1
        #                 final_indexs.append([ii,ii-1,indexs[ii],indexs[ii-1]])
        mid_xx = []  # 去掉原来没用过的
        mid_yy = []
        for ii in range(4):
            if ((mid_x[ii] != 0) & (mid_y[ii] != 0)) | ((mid_x[ii] == 0) & (mid_y[ii] != 0)) | (
                    (mid_x[ii] != 0) & (mid_y[ii] == 0)):
                mid_xx.append(mid_x[ii])
                mid_yy.append(mid_y[ii])
        x = [[mid_xx[ii - 1], mid_xx[ii]] for ii in range(len(mid_xx))]
        y = [[mid_yy[ii - 1], mid_yy[ii]] for ii in range(len(mid_yy))]
        print("len(mid_points)", len(mid_points))
        if len(x) < 2:
            return
        elif len(mid_points) == 4:
            return
        else:
            #         print(x,y)
            #             for jj in range(len(x)):
            #                 plt.plot(x[jj], y[jj], color='r')
            #                 plt.scatter(x[jj], y[jj], color='b')
            if flag == 1:
                return mid_points, spe_indexs, x, y
            else:
                return


# In[288]:


# 遍历所有像素点，画图
def traverse(matrix,src):
    w, h = matrix.shape
    mid_points = []  # 标记点
    spe_indexs = []  # 为跟踪做准备
    #     indexs = []
    x = []
    y = []
    count = 0
    # 遍历一遍
    for i in range(w - 1):
        for j in range(h - 1):
            a, b, c, d, ax, ay, bx, by, cx, cy, dx, dy = get_squares(matrix, i, j)
            #             print(a,b,c,d,ax,ay,bx,by,cx,cy,dx,dy)
            m = squares_2(a, b, c, d, ax, ay, bx, by, cx, cy, dx, dy)
            if m is not None:
                mid, spe, xx, yy = m
                mid_points.extend(mid)
                for ii in spe:
                    if ii is not None:
                        spe_indexs.append(ii)
                x.extend(xx)
                y.extend(yy)
    #                 indexs.extend(label_index)
    #                 xx.append(x)
    #                 yy.append(y)
    for jj in range(len(x)):
        plt.plot(x[jj], y[jj], color='black', lw=0.1)
        # plt.scatter(x[jj], y[jj], color='b')
    #     indexs_1 = [item for item in indexs if item is not None]
    #     print("indexs",indexs)
    #     print("xx",xx)
    #     print("yy",yy)
    xxx = []
    yyy = []
    last_mid = []
    print("spe_indexs", spe_indexs)
    print("mid_points", mid_points)
    # #     fi_spe_indexs
    for item in spe_indexs:
        print("item", item)
        #         while( not in mid_point):
        mm = find_next_sq(matrix, item[0], item[1], item[2][0], item[2][1], item[3][0], item[3][1])
        if mm is None:
            continue
        else:
            print("下一个方mm", mm)
            mix, line_index = mm
            a, b, c, d, ax, ay, bx, by, cx, cy, dx, dy = mix
            midx, midy = mid_point((line_index + 2) % 4, ax, ay, bx, by, cx, cy, dx, dy)  # 得到对面边的中点
            print("下一个的对面midx,midy", midx, midy)
            flag_end = 0  # 判断在结束之前last_mid是否被更改
            while ([midx, midy] not in mid_points):  # 如果对面边中点没被标记
                # 开始跟踪
                n = squares_2_2(a, b, c, d, ax, ay, bx, by, cx, cy, dx, dy)
                if n is None:
                    break
                else:
                    print("n，中点，特殊点，x,y", n)
                    mid, spe, x, y = n
                    xxx.extend(x)
                    yyy.extend(y)
                    print("mid", mid, len(mid))
                    if len(mid) > 2:  # 特殊情况
                        count += 1
                        break
                    else:
                        a = 0
                        for ii in range(len(mid)):
                            print("中点ii", mid[ii])
                            last_mid = mid[ii]
                            flag_end = 1
                            if mid[ii] not in mid_points:
                                a += 1
                                print("!!!!!!!!!!!!没加进去的", mid[ii])
                                mid_points.append(mid[ii])
                                mm = find_next_sq(matrix, spe[ii][0], spe[ii][1], spe[ii][2][0], spe[ii][2][1],
                                                  spe[ii][3][0], spe[ii][3][1])
                                if mm is None:
                                    break
                                else:
                                    mix, line_index = mm
                                    a, b, c, d, ax, ay, bx, by, cx, cy, dx, dy = mix
                                    midx, midy = mid_point((line_index + 2) % 4, ax, ay, bx, by, cx, cy, dx,
                                                           dy)  # 得到对面边的中点
                                    print("下一个的对面中点midx,midy", midx, midy)
                        if a == 0:
                            break
            if flag_end == 0:
                break
            else:
                print("last_mid", last_mid)
                if last_mid != []:
                    xxx.append([last_mid[0], midx])
                    yyy.append([last_mid[1], midy])
    #             print("!!!!!!!!!!!!1",x,y)
    #                 for k in range(len(x)):
    # #                 print("x[k],y[k]",x[k],y[k])
    #                     if (x[k] not in xx)|(y[k] not in yy):
    #                         xxx.append(x[k])
    #                         yyy.append(y[k])
    #                         xx.append(x[k])
    #                         yy.append(y[k])
    #                     elif xx.index[x[k]]!=yy.index[y[k]]:
    #                         xxx.append(x[k])
    #                         yyy.append(y[k])
    #                         xx.append(x[k])
    #                         yy.append(y[k])
    #     print("*xxx",xxx)
    #     print("*yyy",yyy)
    #     return xxx,yyy
    for jj in range(len(xxx)):
        plt.plot(xxx[jj], yyy[jj], color='black', lw=0.1)
        # plt.scatter(xxx[jj], yyy[jj], color='r')
    ax = plt.gca()
    ax.invert_yaxis()  # y轴反向
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    plt.savefig("D:\\"+str(src), dpi=500)  # 指定分辨率保存
    plt.show()
