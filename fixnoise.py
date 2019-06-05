xxx = [0, -1, -1, -1, 0, +1, +1, +1]
yyy = [+1, +1, 0, -1, -1, -1, 0, +1]


def Denoising(raw2, i, j, tag):
	dic_ = {}

	for k in range(8):
		if tag[i + xxx[k], j + yyy[k]] != 1:
			dic_[k] = raw2[i + xxx[k], j + yyy[k]]

	dic_energy = {}
	for k in range(len(dic_)):
		if dic_.get(k):
			for p in range(k + 1, len(dic_) * 2):
				if dic_.get(p):
					next = dic_.get(p)
					break
			dic_energy[k] = (int(dic_[k]) - int(next)) * (int(dic_[k]) - int(next))
	sortedlist = sorted(dic_energy.items(), key=lambda d: d[1], reverse=True)

	a = sortedlist[0][0]
	b = sortedlist[1][0]

	reign1 = []
	reign2 = []
	for k in range(min(a, b), max(a, b)):
		reign1.append(raw2[i + xxx[k], j + yyy[k]])
	for k in range(8):
		if k in range(min(a, b), max(a, b)):
			continue
		reign2.append(raw2[i + xxx[k], j + yyy[k]])

	# print(reign1)
	# print(reign2)

	reign1.sort()
	reign2.sort()

	# print(re1)
	# print(re2)
	for k in range(8):
		if tag[i + xxx[k], j + yyy[k]] == 1:
			min1 = 300
			min2 = 300
			for m in range(len(reign1)):
				if (raw2[i + xxx[k], j + yyy[k]] - reign1[m]) < min1:
					min1 = raw2[i + xxx[k], j + yyy[k]] - reign1[m]
			for m in range(len(reign2)):
				if (raw2[i + xxx[k], j + yyy[k]] - reign2[m]) < min2:
					min2 = raw2[i + xxx[k], j + yyy[k]] - reign2[m]
			if min1 > min2:
				raw2[i + xxx[k], j + yyy[k]] = reign2[int(len(reign2) / 2)]
			if min1 < min2:
				raw2[i + xxx[k], j + yyy[k]] = reign1[int(len(reign1) / 2)]
# return reign1, reign2
