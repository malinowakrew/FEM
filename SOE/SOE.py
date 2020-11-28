from stiffnessMatrix.net import *
from Pmatrix.PMatrix import *
import pandas as pd
import matplotlib.pyplot as plt
import math

from stiffnessMatrix.HMatrix import *

class SOE():
    def __init__(self) -> None:
        self.nodes = self.initHg()
        self.Hg = np.zeros((self.nodes, self.nodes))
        self.Pg = np.zeros((self.nodes, self.nodes)) # do zmienienia :D
        self.net = self.initNet()
        self.t = 0
        self.k = 0
        self.Jacobian_list = []

    def read(self):
        path = r"data/data.txt"
        with open(path, "r") as file:
            data = file.read()
            file.close()

        table = data.split("\n")

        net_table = [float(element) for element in table[:4]]

        s = net(net_table[0], net_table[1], int(net_table[2]), int(net_table[3]))

        self.k = float(table[4])
        self.pointsNumber = int(table[5])
        return s

    def initHg(self):
        net = self.read()
        return(len(net["wezly"]))

    def initNet(self):
        net = self.read()

        if (self.pointsNumber == 4):
            net_lok = net_4_elements(-1.0 / math.sqrt(3))
        elif (self.pointsNumber == 9):
            net_lok = net_9_elements(math.sqrt(3.0 / 5.0))
        elif (self.pointsNumber == 16):
            net_lok = net_16_elements(2)
        else:
            raise ValueError

        return net_lok

    def calculateHg(self):
        net = self.read()
        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])

            #H = form(net_lok.net, net_glob, self.k)

            stiffnessMatrix = StiffnessMatrix(self.net.net, net_glob, self.k)

            matrix_ksi_eta = stiffnessMatrix.form()
            jacobian = stiffnessMatrix.Jacobian(matrix_ksi_eta["matrix_eta"], matrix_ksi_eta["matrix_ksi"])
            self.Jacobian_list.append(jacobian)
            Ni = stiffnessMatrix.derivativeCalculate(jacobian, matrix_ksi_eta["matrix_eta"], matrix_ksi_eta["matrix_ksi"])
            #for i in jacobian:
            #    print(i)
            #print(len(Ni))
            H = stiffnessMatrix.localHcalculate(jacobian, Ni)


            for rowNumber, row in enumerate(H):
                for itemNumber, value in enumerate(row):
                    self.Hg[elem[rowNumber]][elem[itemNumber]] += value

    def calculatePg(self):
        net = self.read()
        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])
            #print(f"Jakobiany dla punkty {nr} {self.Jacobian_list[nr]}")
            P = PMatrixCalculate(self.net.net, 7800, 700, self.Jacobian_list[nr])
            #print("Macierz P")
            #print(P)

            for rowNumber, row in enumerate(P):
                for itemNumber, value in enumerate(row):
                    self.Pg[elem[rowNumber]][elem[itemNumber]] += value

        #Jakobiany zostaną zmienione

        
        """
        for rowNumber, row in enumerate(H):
            for itemNumber, value in enumerate(row):
                self.Hg[elem[rowNumber]][elem[itemNumber]] += value

        """

    def drawStiffnessMatrix(self):
        H = pd.DataFrame(self.Hg)
        plt.pcolor(H.reindex(index=H.index[::-1]))
        plt.yticks(np.arange(0.5, len(H.index), 1), H.index)
        plt.xticks(np.arange(0.5, len(H.columns), 1), H.columns)
        plt.title("Stiffness Matrix")
        plt.show()

    def drawPMatrix(self):
        P = pd.DataFrame(self.Pg)
        plt.pcolor(P.reindex(index=P.index[::-1]))
        plt.yticks(np.arange(0.5, len(P.index), 1), P.index)
        plt.xticks(np.arange(0.5, len(P.columns), 1), P.columns)
        plt.title("P Matrix")
        plt.show()

    def drawNet(self):
        for krotka in self.net.net:
            plt.plot(krotka, 'bo')
        plt.show()