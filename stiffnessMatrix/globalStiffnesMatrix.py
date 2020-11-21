from stiffnessMatrix.net import *
from stiffnessMatrix.integral import *
from stiffnessMatrix.stiffnessMatrix import *
import numpy as np
import math

class SOE():
    def __init__ (self):
        self.macierzrobocza = []
        self.nodes =self.initHg()
        self.Hg = np.zeros((self.nodes, self.nodes)) # to zmienić
        self.Pg = 0
        self.t = 0
        self.k = 0
        self.pointsNumber = 0

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

    def calculateHg(self):
        net = self.read()
        if (self.pointsNumber == 4):
            net_lok = net_4_elements(-1.0 / math.sqrt(3))
        elif (self.pointsNumber == 9):
            net_lok = net_9_elements(math.sqrt(3.0 / 5.0))
        else:
            raise ValueError

        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])

            H = form(net_lok.net, net_glob, self.k)

            for rowNumber, row in enumerate(H):
                for itemNumber, value in enumerate(row):
                    self.Hg[elem[rowNumber]][elem[itemNumber]] += value

