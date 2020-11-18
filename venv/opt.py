import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

x1 = np.linspace(-1, 1, 200)
x2 = np.linspace(-1, 1, 200)

dzialanie = lambda x1, x2: x1*x1+x2*x2-math.cos(2.5*(3.14159*x1))-math.cos(2.5*3.14159*x2)+2.0
macierz = np.zeros((200, 200))

for nri, i in enumerate(x1):
    for nrj, j in enumerate(x2):
        macierz[nri][nrj] = dzialanie(i, j)

plt.pcolor(macierz)
#plt.yticks(np.arange(0.5, len(macierz.index), 1), macierz.index)
#plt.xticks(np.arange(0.5, len(macierz.columns), 1), macierz.columns)
plt.show()