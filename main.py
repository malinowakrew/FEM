# This is a sample Python script.
import pandas as pd
import matplotlib.pyplot as plt

"""
Edyta Mróz https://github.com/malinowakrew/FEM/
"""
from stiffnessMatrix.globalStiffnesMatrix import *

def stiffnessmatrixcalculateH():
    soe = SOE()
    soe.calculateHg()
    soe.drawStiffnessMatrix()



if __name__ == '__main__':
    stiffnessmatrixcalculateH()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
