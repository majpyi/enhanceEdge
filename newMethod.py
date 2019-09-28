import queue
import heapq
import numpy as np
import cv2

mod = 1e9 + 7
d = 8
D = 5


class node:
	type = 0
	gray = 0
	is_bd = 0


# mp[2222][2222]

n = 321
m = 481
# nodec = node()
# mp = [m*nodec]*n
# li = []
# for i in range(m):
# 	li.append(node())
# mp = li*

# mp = li*n
# li = [][]
mp = [[] for i in range(n + 1)]

for i in range(n + 1):
	for j in range(m + 1):
		mp[i].append(node())
#
# mp = np.shape((n+1,m+1))
# mp = None
# for i in range((n+1)*(m+1)):
# 	mp.append(node())
# for i in range(n + 1):
# # # 	mp[i] = []
# 	for j in range(m + 1):
# mp = np.concatenate(mp, node())

# 		mp[i].append(node())
# mp.append(li)
# 	mp[i][j] = node()
# mp = [[node()]*(m+1) for i in range(n+1)]
# mp.reshape(n+1,m+1)


print(mp)

tp = np.zeros((10000000))
mx = [0, 0, 1, -1]
my = [1, -1, 0, 0]
# vis = []
vis = np.zeros((n + 1, m + 1))


class X:
	x = 0
	y = 0
	co = 0

	def __init__(self, name, y, co):
		self.x = name
		self.y = y
		self.co = co


def bfs(x, y, co):
	vis[x][y] = 1
	# queue<X> q;
	list = []
	list.append(X(x, y, co))
	while len(list) != 0:
		u = list[0]
		list.remove(u)
		#     q.pop();
		mp[u.x][u.y].type = u.co
		tp[co] = tp[co] + 1
		for i in range(4):
			nx = u.x + mx[i]
			ny = u.y + my[i]
			if 1 <= nx <= n and m >= ny >= 1 and abs(int(mp[u.x][u.y].gray) - int(mp[nx][ny].gray)) <= d and vis[nx][
				ny] == 0:
				vis[nx][ny] = 1
				list.append(X(nx, ny, co))


class Node:
	x = 0
	y = 0
	dx = 0
	type = 0
	gray = 0

	def __init__(self, x, y, dx, type, gray):
		self.x = x
		self.y = y
		self.dx = dx
		self.type = type
		self.gray = gray

	def __lt__(self, a):
		# print(type(a.dx))
		# print(type(self.dx))
		return self.dx < a.dx

	# def __cmp__(self, a):
	# 	return dx > a.dx


# bool operator<(const Node &a) const {


# priority_queue<Node> q;//优先队列
q = queue.PriorityQueue()


def dfs(x, y):
	vis[x][y] = 2

	for i in range(4):
		nx = x + mx[i]
		ny = y + my[i]
		if (1 <= nx <= n and 1 <= ny <= m and mp[nx][ny].type != mp[x][y].type and
				tp[mp[nx][ny].type] > D):
			q.put(Node(x, y, abs(int(mp[x][y].gray) - int(mp[nx][ny].gray)), mp[nx][ny].type, mp[nx][ny].gray))

	for i in range(4):
		nx = x + mx[i]
		ny = y + my[i]
		if (1 <= nx <= n and 1 <= ny <= m and mp[nx][ny].type == mp[x][y].type and
				vis[nx][ny] == 1):
			dfs(nx, ny)


def merge(t):
	global dx
	while not q.empty() and tp[t] > 0:
		# u = q.top()
		u = q.get()
		# print(type(u))
		if vis[u.x][u.y] == 2:
			vis[u.x][u.y] = 3
			tp[t] = tp[t] - 1
			mp[u.x][u.y].type = u.type
			mp[u.x][u.y].gray = u.gray
		else:
			continue
		for j in range(4):
			# print(type(u.x))
			# print(u.x)

			nx = u.x + mx[j]
			ny = u.y + my[j]
			if 1 <= nx <= n and 1 <= ny <= m and mp[nx][ny].type == t and vis[nx][ny] == 2:
				dx = abs(int(mp[u.x][u.y].gray) - int(mp[nx][ny].gray))
				q.put(Node(nx, ny, dx, u.type, u.gray))


def work():
	# for (int i = 1; i <= n; i++) {
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			# for (int j = 1; j <= m; j++) {
			num = 0
			goal = 4
			df = 0
			dt = 0
			flag = 0
			for k in range(4):
				nx = i + mx[k]
				ny = j + my[k]
				if 1 <= nx <= n and 1 <= ny <= m and mp[nx][ny].type == mp[i][j].type:
					num = num + 1
				else:
					if nx == 0 or nx == n + 1 or ny == 0 or ny == m + 1:
						goal -= 1
					else:
						if df == 0:
							df = mp[nx][ny].gray
							dt = mp[nx][ny].type
						elif dt != mp[nx][ny].type:
							flag = 1

			if num == goal:
				mp[i][j].is_bd = 0
			else:
				if flag == 1:
					mp[i][j].is_bd = 3
				else:
					if mp[i][j].gray < df:
						mp[i][j].is_bd = 1
					else:
						mp[i][j].is_bd = 2


# mp[i][j].is_bd = mp[i][j].gray < df ? 1 : 2


#
# /*-----------------------------------------------------------------------------------------------------------*/
#
# void print() {
#     for (int i = 1; i <= n; i++) {
#         for (int j = 1; j < m; j++) {
#             printf("%3d,", mp[i][j].type);
#         }
#         printf("%3d\n", mp[i][m].type);
#     }
# //    printf("\n");
# }
#
# void printgray() {
#     for (int i = 1; i <= n; i++) {
#         for (int j = 1; j < m; j++) {
#             printf("%3d,", mp[i][j].gray);
#         }
#         printf("%3d\n", mp[i][m].gray);
#     }
# //    printf("\n");
# }
#
# void printis() {
#     for (int i = 1; i <= n; i++) {
#         for (int j = 1; j < m; j++) {
#             printf("%d,", mp[i][j].is_bd);
#         }
#         printf("%d\n", mp[i][m].is_bd);
#     }
# //    printf("\n");
# }
#


#     freopen("D:\\out\\296059.csv", "r", stdin);  //第一个 输入文件   名字自己命名，并且需要和cpp文件在同一个文件夹
#     if (tag == 1) {
#         freopen("D:\\out\\type.csv", "w", stdout);//第二个 输出文件
#     }
#     if (tag == 2) {
#         freopen("D:\\out\\bd.csv", "w", stdout);//第二个 输出文件
#     }
#     if (tag == 3) {
#         freopen("D:\\out\\gray.csv", "w", stdout);//第二个 输出文件
#     }
#     //
# //    printf("输入n*m大小灰度矩阵 依次输入n,m\n");
# //	printf("请输入灰度矩阵：\n");

inpath = "D:\\experiment\\pic\\q\\"
outpath = "D:\\out\\"
src = "296059"

raw = cv2.imread(inpath + src + ".jpg")
raw1 = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)

print(raw1)

for i in range(1, n + 1):
	for j in range(1, m + 1):
		mp[i][j].gray = raw1[i - 1][j - 1]

#             if (j != m)scanf("%d,", &mp[i][j].gray);//输入灰度矩阵
#             else scanf("%d", &mp[i][j].gray);
# //       cin>>mp[i][j].gray;
#         }
#     }
#     //////////////
tot = 1
for i in range(1, n + 1):
	for j in range(1, m + 1):
		if vis[i][j] == 0:
			bfs(i, j, tot)
			tot += 1
#             }
#
#         }
#     /*----------------------------------*/
# //	printf("初步分类:类型矩阵\n");
# //
# //	print();
#     /*----------------------------------*/


for i in range(1, n + 1):
	for j in range(1, m + 1):
		t = mp[i][j].type
		if tp[t] <= D and vis[i][j] == 1:
			while not q.empty():
				q.get()
			dfs(i, j)
			merge(t)

work()

re = np.zeros((n + 1, m + 1))
pic = np.zeros((n + 1, m + 1))

tag = int(input())

# print(tag)

if tag == 1:
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			re[i][j] = mp[i][j].type

if tag == 2:
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			re[i][j] = mp[i][j].is_bd
			if mp[i][j].is_bd == 3:
				pic[i][j] = 175
			elif mp[i][j].is_bd == 2:
				pic[i][j] = 255
			else:
				pic[i][j] = 0
	np.savetxt(outpath + "outpic.csv", re, fmt="%d", delimiter=',')
	cv2.imwrite(outpath + "outpic" + ".jpg", pic)

if tag == 3:
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			re[i][j] = mp[i][j].gray
	np.savetxt(outpath + "outpic.csv", re, fmt="%d", delimiter=',')
	cv2.imwrite(outpath + "outpic" + ".jpg", re)
