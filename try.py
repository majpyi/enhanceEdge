class node:
	type = 0
	gray = 0
	is_bd = 0


n = 321
m = 481
li = []
mp = []
for i in range(m):
	li.append(node())
# mp = li*n
for i in range(n):
	mp.append(li)
# print(mp)
print(mp[0][0])
print(li[0].type)
