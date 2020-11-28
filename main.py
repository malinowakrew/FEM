# This is a sample Python script.

"""
Edyta Mróz https://github.com/malinowakrew/FEM/
"""
from SOE.SOE import *

def stiffnessmatrixcalculateH():
    soe = SOE()
    soe.calculateHg()
    soe.calculatePg()

    np.set_printoptions(linewidth=np.inf)
    print("\nMatrix H")
    with np.printoptions(precision=3, suppress=True):
        print(soe.Hg)

    print("\n\nMatrix P")
    with np.printoptions(precision=3, suppress=True):
        print(soe.Pg)

    #drawing matrix
    #soe.drawPMatrix()
    #soe.drawStiffnessMatrix()

    soe.drawNet()


if __name__ == '__main__':
    stiffnessmatrixcalculateH()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
