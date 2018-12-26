import matplotlib.pyplot as plt
# plt.scatter(1.5, 2.5, c='r')
# plt.scatter(1.5, 2.5, c='b')
# plt.scatter([1, 2, 3], [2, 3, 4])
plt.plot([1,2,2,4],[2,3,4,6])
plt.axis("equal")
plt.gca().invert_yaxis()
plt.show()