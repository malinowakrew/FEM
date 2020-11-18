from ksztalt import *
from siatka import *
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

    def read(self):
        sciezka = r"dane.txt"
        with open(sciezka, "r") as plik:
            dane = plik.read()
            plik.close()

        tablica = dane.split("\n")

        tablica_danych = [float(element) for element in tablica[:4]]

        s = siatka(tablica_danych[0], tablica_danych[1], int(tablica_danych[2]), int(tablica_danych[3]))

        self.k = float(tablica[6])
        return s

    def initHg(self):
        net = self.read()
        return(len(net["wezly"]))

    def calculateHg(self):
        net = self.read()
        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])

            net_lok = [[-1.0 / math.sqrt(3), -1.0 / math.sqrt(3)], [1.0 / math.sqrt(3), -1.0 / math.sqrt(3)],
                   [1.0 / math.sqrt(3), 1.0 / math.sqrt(3)], [-1.0 / math.sqrt(3), 1.0 / math.sqrt(3)]]

            net_lok_9 = net_9_elements(math.sqrt(3.0/5.0))
            #print(net_lok_9.net)

            H = form(net_lok_9.net, net_glob, self.k)

            for rowNumber, row in enumerate(H):
                for itemNumber, value in enumerate(row):
                    self.Hg[elem[rowNumber]][elem[itemNumber]] += value


def main():
    klasa = SOE()
    klasa.calculateHg()
    print(klasa.Hg)

if __name__ == "__main__":
    main()