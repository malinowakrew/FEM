# This is a sample Python script.
import pandas as pd
import matplotlib.pyplot as plt

"""
Edyta Mróz https://github.com/malinowakrew/FEM/
"""
from stiffnessMatrix.SOE import *

def stiffnessmatrixcalculateH():
    soe = SOE()
    soe.calculateHg()
    #print(soe.Hg)
    #soe.drawStiffnessMatrix()
    soe.calculatePg()


if __name__ == '__main__':
    stiffnessmatrixcalculateH()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
