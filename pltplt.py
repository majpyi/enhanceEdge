import matplotlib.pyplot as plt

# plt.scatter(1.5, 2.5, c='r')
# plt.scatter(1.5, 2.5, c='b')
# plt.scatter([1, 2, 3], [2, 3, 4])
# plt.plot([1,2,2,4],[2,3,4,6])
# plt.plot([1,2,2,4],[2,3,4,6])
plt.plot([429.5, 430.0, 1], [318.0, 318.5, 1])
plt.axis("equal")
plt.gca().invert_yaxis()
plt.show()
