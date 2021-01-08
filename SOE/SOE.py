from stiffnessMatrix.net import *
from Cmatrix.CMatrix import *
import pandas as pd
import matplotlib.pyplot as plt

from stiffnessMatrix.HMatrix import *


class SOE():
    def __init__(self, time_max, tau, k, t0, density, specific_heat, alfa, ambient_temperature, net_table, point_number)->None:
        """
        :param time_max: 
        :param tau: 
        :param k: 
        :param t0: 
        :param density: 
        :param specific_heat: 
        :param alfa: 
        :param ambient_temperature: 
        :param net_table: 
        :param point_number: 
        """
        """
        Creating a global net
        """
        self.global_net = net(net_table[0], net_table[1], int(net_table[2]), int(net_table[3]))
        """
        Values which must be read from data.txt file
        """
        self.nodes = self.init_nodes()
        self.time_max = time_max
        self.k = self.global_net["wspolczynnik_przewodzenia"]
        self.tau = tau
        self.t0 = np.full(self.nodes, t0)
        self.density = density
        self.specific_heat = specific_heat
        self.alfa = alfa
        self.ambient_temperature = ambient_temperature
        """
        Initialization values H, C and P - global matrix for equation
        """
        self.Hg = np.zeros((self.nodes, self.nodes))
        self.Cg = np.zeros((self.nodes, self.nodes))
        self.Pg = np.zeros(self.nodes)

        """
        Jacobian list for all elements to provide calculate it multiple times
        """
        self.Jacobian_list = []
        """
        Data required to make a local net 
        """
        self.pointsNumber = point_number
        self.local_net = self.initNet()

    def init_nodes(self):
        return len(self.global_net["wezly"])

    def initNet(self):
        if self.pointsNumber == 4:
            net_lok = net_4_elements(-1.0 / math.sqrt(3))
        elif self.pointsNumber == 9:
            net_lok = net_9_elements(math.sqrt(3.0 / 5.0))
        elif self.pointsNumber == 16:
            net_lok = net_16_elements(2)
        else:
            raise ValueError

        return net_lok

    def calculate_hg(self):
        net = self.global_net
        c = self.alfa
        """
        Reading coordinates for every element and transform it to local net
        """
        for nr, elem in enumerate(net["elementy"]):
            coordinates_of_element = []
            mask_for_element = []
            for nodeNumber in elem:
                coordinates_of_element.append(net["wezly"][nodeNumber])
                mask_for_element.append(net["krawedzie"][nodeNumber])
                k = self.k[nodeNumber]
                #k=self.k

            """
            Creating local H matrix 
            """
            stiffnessMatrix = StiffnessMatrix(self.local_net.net, coordinates_of_element, k)

            matrix_ksi_eta = stiffnessMatrix.form()
            jacobian = stiffnessMatrix.Jacobian(matrix_ksi_eta["matrix_eta"], matrix_ksi_eta["matrix_ksi"])
            self.Jacobian_list.append(jacobian)
            Ni = stiffnessMatrix.derivativeCalculate(jacobian, matrix_ksi_eta["matrix_eta"], matrix_ksi_eta["matrix_ksi"])
            H = stiffnessMatrix.localHcalculate(jacobian, Ni)

            """
            Calculate H bc for edges of the element and add it to local H matrix
            """
            if mask_for_element != [0.0, 0.0, 0.0, 0.0]:
                #print(f"Maska {mask_glob} dla {net_glob} dla elementu {nr}")
                if len(self.local_net.net) in [4, 9]:
                    localNet = self.local_net
                else:
                    localNet = net_4_elements(1.0 / math.sqrt(3))
                hbc = HBC()
                jacobians = hbc.jacobian(coordinates_of_element)
                H_bc = hbc.calculateHBC(localNet.edges_ksi_eta(0), mask_for_element, jacobians, c) # to nie zależy dla delty

                H += H_bc
                # print(H)
        
            """
            Adding values to global H matrix for local ones
            """
            for rowNumber, row in enumerate(H):
                for itemNumber, value in enumerate(row):
                    self.Hg[elem[rowNumber]][elem[itemNumber]] += value

        # print("H global")
        # print(self.Hg)

    def calculateCg(self):
        """
        Calculate C global matrix
        :return: 
        """
        net = self.global_net
        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])
            #print(f"Jakobiany dla punkty {nr} {self.Jacobian_list[nr]}")
            C = CMatrixCalculate(self.local_net.net, self.density, self.specific_heat, self.Jacobian_list[nr])
            #print("Macierz P")
            #print(P)

            for rowNumber, row in enumerate(C):
                for itemNumber, value in enumerate(row):
                    self.Cg[elem[rowNumber]][elem[itemNumber]] += value


    def calculateHBC(self, c):
        """
        Using only for test
        :param c: 
        :return: 
        """
        net = self.global_net
        print(net["wezly"])
        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            mask_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])
                mask_glob.append(net["krawedzie"][nodeNumber])

            if mask_glob != [0.0, 0.0, 0.0, 0.0]:
                #print(f"Maska {mask_glob} dla {net_glob} dla elementu {nr}")
                localNet = net_4_elements(1.0 / math.sqrt(3))
                hbc = HBC()
                jacobiany = hbc.jacobian(net_glob)
                print(hbc.calculateHBC(localNet.edges_ksi_eta(0), mask_glob, jacobiany, c)) # to nie zależy dla delty

    def calculateP(self):
        net = self.global_net
        c = self.alfa
        t8 = self.ambient_temperature
        for nr, elem in enumerate(net["elementy"]):
            net_glob = []
            mask_glob = []
            for nodeNumber in elem:
                net_glob.append(net["wezly"][nodeNumber])
                mask_glob.append(net["krawedzie"][nodeNumber])

            if mask_glob != [0.0, 0.0, 0.0, 0.0]:
                if len(self.local_net.net) in [4]:
                    localNet = self.local_net
                else:
                    localNet = net_4_elements(1.0 / math.sqrt(3))
                hbc = Pmatrix()
                jacobiany = hbc.jacobian(net_glob)
                P_local = hbc.calculateP(localNet.edges_ksi_eta(0), mask_glob, jacobiany, c, t8)  # to nie zależy dla delty

                for number, _ in enumerate(P_local):
                    self.Pg[elem[number]] += P_local[number]

        # print(self.Pg)
    ## takie do gaussa
    @staticmethod
    def elimination(matrix_in):
        matrix_out = matrix_in
        shape_matrix = matrix_out.shape
        row = shape_matrix[0]
        column = shape_matrix[1]

        for a in range(1, row):
            for i in range(a, row):
                k = matrix_out[i][a - 1] / matrix_out[a - 1][a - 1]
                for j in range(a - 1, column):
                    element = matrix_out[i][j]
                    matrix_out[i][j] = (element - (k * matrix_out[a - 1][j]))

        return matrix_out
    @staticmethod
    def gauss_calculations(matrix_in):
        matrix_out = matrix_in
        shape_matrix = matrix_out.shape
        row = shape_matrix[0]
        column = shape_matrix[1]

        solution_vector = []
        for i in reversed(range(0, row)):
            temporary_solution = matrix_out[i, column - 1]
            for j in range(0, row - i - 1):
                temporary_solution = temporary_solution - (solution_vector[j] * matrix_out[i][column - 2 - j])

            temporary_solution = (temporary_solution / matrix_out[i, i])
            solution_vector.append(temporary_solution)

        return solution_vector

    #DODAWANKO I PO CZASIE CHODZONKO
    def calculations(self, nr):
        C = self.Cg / self.tau
        H = self.Hg + C

        P = self.Pg - np.matmul(C, self.t0)
        P = -1.0 * P
        print(P)

        P_in_proper_shape = [[i] for i in P]

        H_matrix_with_free_vector = np.append(H, P_in_proper_shape, axis=1)
        result = self.gauss_calculations(self.elimination(H_matrix_with_free_vector))

        # show results
        print(f"Results {nr}")
        print(max(result))
        print(min(result))

        self.t0 = result
        x = []
        y = []
        con = []
        egdes = []

        color = []
        for nr, i in enumerate(self.global_net["wezly"]):
            x.append(i[0])
            y.append(i[1])
            color.append(result[nr])
            con.append(self.global_net["wspolczynnik_przewodzenia"][nr])
            egdes.append(self.global_net["krawedzie"][nr])

        return(pd.DataFrame({"x": x,
                             "y": y,
                             "t": color,
                             "con": con,
                             "egdes": egdes}))


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


