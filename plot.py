import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('output/area.txt')

plt.figure()
plt.hist(data, bins=500)

plt.xlim(0, 300)
print(data.max())


plt.xlabel('area')
plt.ylabel('count')

# plt.yscale('log')

plt.show()