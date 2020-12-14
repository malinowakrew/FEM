# This is a sample Python script.

"""
Edyta Mróz https://github.com/malinowakrew/FEM/
"""
from SOE.SOE import *

def stiffnessmatrixcalculateH():

    np.set_printoptions(linewidth=np.inf)
    soe = SOE()
    soe.calculateHBC(25.0)

    soe.calculateP(300.0, 1200.0)
    print(soe.Pg)

    soe.calculateHg(25.0)

    soe.calculateCg(7800, 700)

    print("\nMatrix H")
    with np.printoptions(precision=3, suppress=True):
        print(soe.Hg)

    print("\n\nMatrix C")
    with np.printoptions(precision=3, suppress=True):
        print(soe.Cg)

    #drawing matrix
    soe.drawCMatrix()
    soe.drawStiffnessMatrix()


if __name__ == '__main__':
    stiffnessmatrixcalculateH()


