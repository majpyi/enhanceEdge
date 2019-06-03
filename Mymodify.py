xxx = [0, -1, -1, -1, 0, +1, +1, +1]
yyy = [+1, +1, 0, -1, -1, -1, 0, +1]


def point_classification(raw2, i, j):
	list = {}
	for k in range(8):
		list[k] = (int(int(raw2[i + xxx[k], j + yyy[k]]) - int(raw2[i + xxx[k - 1], j + yyy[k - 1]]))) * int((
				int(raw2[i + xxx[k], j + yyy[k]]) - int(raw2[i + xxx[k - 1], j + yyy[k - 1]])))
	# list[k] = abs(int(raw2[i + xxx[k], j + yyy[k]] - raw2[i + xxx[k - 1], j + yyy[k - 1]]))
	sortedlist = sorted(list.items(), key=lambda d: d[1], reverse=True)
	# print(list)
	# print(sortedlist)
	# print(sortedlist[0][0])
	a = sortedlist[0][0]
	# print(sortedlist[1][0])
	b = sortedlist[1][0]
	reign1 = []
	reign2 = []
	for k in range(min(a, b), max(a, b)):
		reign1.append((i + xxx[k], j + yyy[k]))
	for k in range(8):
		if k in range(min(a, b), max(a, b)):
			continue
		reign2.append((i + xxx[k], j + yyy[k]))
	return reign1, reign2


def Denoising(raw2, i, j):
	dic_energy = {}
	for k in range(8):
		dic_energy[k] = (int(int(raw2[i + xxx[k], j + yyy[k]]) - int(raw2[i + xxx[k - 1], j + yyy[k - 1]]))) * int((
				int(raw2[i + xxx[k], j + yyy[k]]) - int(raw2[i + xxx[k - 1], j + yyy[k - 1]])))
	# list[k] = abs(int(raw2[i + xxx[k], j + yyy[k]] - raw2[i + xxx[k - 1], j + yyy[k - 1]]))
	sortedlist = sorted(dic_energy.items(), key=lambda d: d[1], reverse=True)

	newlist = {}
	for k in range(8):
		newlist[k] = (int(int(raw2[i + xxx[k], j + yyy[k]]) - int(raw2[i + xxx[k - 2], j + yyy[k - 2]]))) * int((
				int(raw2[i + xxx[k], j + yyy[k]]) - int(raw2[i + xxx[k - 2], j + yyy[k - 2]])))

	# print(dic_energy)
	# print(newlist)
	# print(newlist.keys())
	# print(list(dic_energy.keys()))
	sumall = 0
	for n in range(8):
		sumall += dic_energy.get(n)
	energy = []
	for m in range(8):
		l = list(dic_energy.values())
		# print(l)
		sum = sumall
		# print(sum)
		k = m
		sum -= dic_energy.get(k)
		l.remove(dic_energy.get(k))
		if k + 1 >= 8:
			sum -= int(dic_energy.get(k + 1 - 8))
			l.remove(dic_energy.get(k + 1 - 8))
		else:
			sum -= int(dic_energy.get(k + 1))
			l.remove(dic_energy.get(k + 1))
		if k + 1 >= 8:
			sum += int(newlist.get(k + 1 - 8))
			l.append(newlist.get(k + 1 - 8))
		else:
			sum += int(newlist.get(k + 1))
			l.append(newlist.get(k + 1))
		sortedl = sorted(l)
		sum -= sortedl[-1]
		sum -= sortedl[-2]
		energy.append(sum)

	# print(energy)

	index = []
	# index.append(energy.index(min(energy)))
	index.append(energy.index(min(energy)))
	# print(index)

	dic_energy = {}
	for k in range(8):
		if k in index:
			dic_energy[k] = (int(int(raw2[i + xxx[(k+1)%8], j + yyy[(k+1)%8]]) - int(raw2[i + xxx[k - 1], j + yyy[k - 1]]))) * int((
					int(raw2[i + xxx[(k+1)%8], j + yyy[(k+1)%8]]) - int(raw2[i + xxx[k - 1], j + yyy[k - 1]])))
		elif k == index[0] + 1 % 8:
			continue
		else:
			dic_energy[k] = (int(int(raw2[i + xxx[k], j + yyy[k]]) - int(raw2[i + xxx[k - 1], j + yyy[k - 1]]))) * int((
					int(raw2[i + xxx[k], j + yyy[k]]) - int(raw2[i + xxx[k - 1], j + yyy[k - 1]])))
	# list[k] = abs(int(raw2[i + xxx[k], j + yyy[k]] - raw2[i + xxx[k - 1], j + yyy[k - 1]]))
	# print(dic_energy)
	sortedlist = sorted(dic_energy.items(), key=lambda d: d[1], reverse=True)

	a = sortedlist[0][0]
	b = sortedlist[1][0]
	reign1 = []
	reign2 = []
	noise = []
	for k in index:
		noise.append((i + xxx[k], j + yyy[k]))
	for k in range(min(a, b), max(a, b)):
		if k in index:
			continue
		reign1.append((i + xxx[k], j + yyy[k]))
	for k in range(8):
		if k in range(min(a, b), max(a, b)):
			continue
		if k in index:
			continue
		reign2.append((i + xxx[k], j + yyy[k]))

	tag = 0
	for k in range(8):
		if dic_energy.get(k) == 0:
			tag += 1

	while len(reign1) == 0 or len(reign2) == 0:
		energy[index[0]] = 255 * 255
		index = []
		reign1 = []
		reign2 = []
		noise = []
		index.append(energy.index(min(energy)))
		for k in index:
			noise.append((i + xxx[k], j + yyy[k]))
		for k in range(min(a, b), max(a, b)):
			if k in index:
				continue
			reign1.append((i + xxx[k], j + yyy[k]))
		for k in range(8):
			if k in range(min(a, b), max(a, b)):
				continue
			if k in index:
				continue
			reign2.append((i + xxx[k], j + yyy[k]))

	# if tag == 8:
	# 	for k in index:
	# 		reign1.append((i + xxx[k], j + yyy[k]))
	# 	noise.pop(0)
	# 	return reign1, reign2, noise
	return reign1, reign2, noise
