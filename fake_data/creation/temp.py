import numpy as np
from scipy.stats import gamma
import matplotlib.pyplot as plt

sample = np.random.gamma(.1, 10, 1000)
sample = np.random.gamma(.05, 500, 1000)

np.percentile(sample, [50, 80, 95])

plt.plot(np.percentile(sample, np.arange(0, 101, 10)))
plt.show()

plt.hist(sample, bins=100)
plt.show()


