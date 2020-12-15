# This is a sample Python script.

"""
Edyta Mróz https://github.com/malinowakrew/FEM/
"""
from SOE.SOE import *

def stiffnessmatrixcalculateH():

    np.set_printoptions(linewidth=np.inf)
    soe = SOE()
    #soe.calculateHBC(25.0)
    t = 0
    tab = []
    fig, axes = plt.subplots(nrows=9, ncols=1)
    fig.set_size_inches(10, 30)
    soe.calculateP(300.0, 1200.0)

    soe.calculateHg(300.0)

    soe.calculateCg(7800.0, 700.0)
    while t < 9:
        tab.append(soe.calculations())
        temp = soe.calculations()

        im = axes.flat[t].scatter(temp["x"], temp["y"], c=temp["t"], cmap='RdBu')
        print(im)
        plt.scatter(temp["x"], temp["y"], c=temp["t"])
        plt.colorbar()
        plt.show()
        t += 1

    tab = pd.concat(tab)
    print(tab)
    fig.subplots_adjust()
    cbar_ax = fig.add_axes([0.9, 0.9, 0.9, 0.9])
    fig.colorbar(im, ax=axes.flat, cax=cbar_ax)
    plt.show()
    plt.savefig('temp_plot.png', dpi=fig.dpi)
    #plt.scatter(tab["x"], tab["y"], c=tab["t"])
    #plt.show()

    #drawing matrix
    #soe.drawCMatrix()
    #soe.drawStiffnessMatrix()
    soe.calculations()




if __name__ == '__main__':
    stiffnessmatrixcalculateH()

