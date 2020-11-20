# This is a sample Python script.
import pandas as pd
import matplotlib.pyplot as plt

"""
Edyta Mróz https://github.com/malinowakrew/FEM/
"""
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from stiffnessMatrix.globalStiffnesMatrix import *

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')
    klasa = SOE()
    klasa.calculateHg()
    #print(klasa.Hg)
    klasa.initHg()

    H = pd.DataFrame(klasa.Hg)
    plt.pcolor(H.reindex(index=H.index[::-1]))
    #plt.yticks(np.arange(0.5, len(H.index), 1), H.index)
    #plt.xticks(np.arange(0.5, len(H.columns), 1), H.columns)
    plt.show()

    print(H)
    print(klasa.k)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
