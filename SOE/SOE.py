from stiffnessMatrix.net import *
from Cmatrix.CMatrix import *
import pandas as pd
import matplotlib.pyplot as plt

from stiffnessMatrix.HMatrix import *

class SOE():
    def __init__(self) -> None:
        self.nodes = self.initHg()
        self.Hg = np.zeros((self.nodes, self.nodes))
        self.Cg = np.zeros((self.nodes, self.nodes)) # do zmienienia :D
        self.Pg = np.zeros(self.nodes)
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
        self.t = float(table[6])
        return s

    def initHg(self):
        net = self.read()
        return(len(net["wezly"]))

    def initNet(self):
        net = self.read()

        if self.pointsNumber == 4:
            net_lok = net_4_elements(-1.0 / math.sqrt(3))
        elif self.pointsNumber == 9:
            net_lok = net_9_elements(math.sqrt(3.0 / 5.0))
        elif self.pointsNumber == 16:
            net_lok = net_16_elements(2)
        else:
            raise ValueError

        return net_lok

    def calculateHg(self, c):
        net = self.read()
        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            mask_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])
                mask_glob.append(net["krawedzie"][nodeNumber])

            #H = form(net_lok.net, net_glob, self.k)
            #H
            stiffnessMatrix = StiffnessMatrix(self.net.net, net_glob, self.k)

            matrix_ksi_eta = stiffnessMatrix.form()
            jacobian = stiffnessMatrix.Jacobian(matrix_ksi_eta["matrix_eta"], matrix_ksi_eta["matrix_ksi"])
            self.Jacobian_list.append(jacobian)
            Ni = stiffnessMatrix.derivativeCalculate(jacobian, matrix_ksi_eta["matrix_eta"], matrix_ksi_eta["matrix_ksi"])
            #print(Ni)
            H = stiffnessMatrix.localHcalculate(jacobian, Ni)

            #H_bc
            if mask_glob != [0.0, 0.0, 0.0, 0.0]:
                #print(f"Maska {mask_glob} dla {net_glob} dla elementu {nr}")
                localNet = net_4_elements(1.0 / math.sqrt(3))
                hbc = HBC()
                jacobiany = hbc.jacobian(net_glob)
                H_bc = hbc.calculateHBC(localNet.edges_ksi_eta(0), mask_glob, jacobiany, c) # to nie zależy dla delty

                H += H_bc

            for rowNumber, row in enumerate(H):
                for itemNumber, value in enumerate(row):
                    self.Hg[elem[rowNumber]][elem[itemNumber]] += value

    def calculateCg(self, c, ro):
        net = self.read()
        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])
            #print(f"Jakobiany dla punkty {nr} {self.Jacobian_list[nr]}")
            C = CMatrixCalculate(self.net.net, c, ro, self.Jacobian_list[nr])
            #print("Macierz P")
            #print(P)

            for rowNumber, row in enumerate(C):
                for itemNumber, value in enumerate(row):
                    self.Cg[elem[rowNumber]][elem[itemNumber]] += value

        #Jakobiany zostaną zmienione

        
        """
        for rowNumber, row in enumerate(H):
            for itemNumber, value in enumerate(row):
                self.Hg[elem[rowNumber]][elem[itemNumber]] += value

        """
    def calculateHBC(self, c):
        net = self.read()
        print(net["wezly"])
        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            mask_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])
                mask_glob.append(net["krawedzie"][nodeNumber])

            if mask_glob != [0.0, 0.0, 0.0, 0.0]:
                print(f"Maska {mask_glob} dla {net_glob} dla elementu {nr}")
                localNet = net_4_elements(1.0 / math.sqrt(3))
                hbc = HBC()
                jacobiany = hbc.jacobian(net_glob)
                print(hbc.calculateHBC(localNet.edges_ksi_eta(0), mask_glob, jacobiany, c)) # to nie zależy dla delty

    def calculateP(self, c, t8):
        net = self.read()
        print(net["wezly"])
        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            mask_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])
                mask_glob.append(net["krawedzie"][nodeNumber])

            if mask_glob != [0.0, 0.0, 0.0, 0.0]:
                localNet = net_4_elements(1.0 / math.sqrt(3))
                hbc = Pmatrix()
                jacobiany = hbc.jacobian(net_glob)
                P_local = hbc.calculateP(localNet.edges_ksi_eta(0), mask_glob, jacobiany, c, t8)# to nie zależy dla delty

                for number, _ in enumerate(P_local):
                    self.Pg[elem[number]] = P_local[number]

    def drawStiffnessMatrix(self):
        H = pd.DataFrame(self.Hg)
        plt.pcolor(H.reindex(index=H.index[::-1]))
        plt.yticks(np.arange(0.5, len(H.index), 1), H.index)
        plt.xticks(np.arange(0.5, len(H.columns), 1), H.columns)
        plt.title("Stiffness Matrix")
        plt.show()

    def drawCMatrix(self):
        P = pd.DataFrame(self.Cg)
        plt.pcolor(P.reindex(index=P.index[::-1]))
        plt.yticks(np.arange(0.5, len(P.index), 1), P.index)
        plt.xticks(np.arange(0.5, len(P.columns), 1), P.columns)
        plt.title("C Matrix")
        plt.show()

    def drawNet(self):
        for krotka in self.net.net:
            plt.plot(krotka, 'bo')
        plt.show()

