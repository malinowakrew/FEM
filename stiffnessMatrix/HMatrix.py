from stiffnessMatrix.integral import *

class StiffnessMatrix:
    def __init__(self, ksi_eta_table, x_y_table, k):
        self.ksi_eta_table = ksi_eta_table
        self.x_y_table = x_y_table
        self.size_of_local_data = len(ksi_eta_table)
        self.k = k

    def form(self):
        ksi_eta_table = self.ksi_eta_table
        """"
        N1 = (1.0-ksi)(1.0-eta)/4.0
        N2 = (1.0+ksi)(1.0-eta)/4.0
        N3 = (1.0+ksi)(1.0+eta)/4.0
        N4 = (1.0-ksi)(1.0+eta)/4.0
        """
        size_of_local_data = len(ksi_eta_table)
        #print(size_of_local_data)

        Y_N1_dev_ksi = lambda ksi: (1.0 - ksi) / -4.0
        Y_N2_dev_ksi = lambda ksi: (1.0 + ksi) / -4.0
        Y_N3_dev_ksi = lambda ksi: (1.0 + ksi) / 4.0
        Y_N4_dev_ksi = lambda ksi: (1.0 - ksi) / 4.0
        Y_N = [Y_N1_dev_ksi, Y_N2_dev_ksi, Y_N3_dev_ksi, Y_N4_dev_ksi]

        X_N1_dev_eta = lambda eta: (1.0 - eta) / -4.0
        X_N2_dev_eta = lambda eta: (1.0 - eta) / 4.0
        X_N3_dev_eta = lambda eta: (1.0 + eta) / 4.0
        X_N4_dev_eta = lambda eta: (1.0 + eta) / -4.0
        X_N = [X_N1_dev_eta, X_N2_dev_eta, X_N3_dev_eta, X_N4_dev_eta]

        matrix_ksi = np.zeros((size_of_local_data, 4))
        matrix_eta = np.zeros((size_of_local_data, 4))

        for nr_2, point in enumerate(ksi_eta_table):
            for nr_1, n in enumerate(X_N):
                matrix_ksi[nr_2][nr_1] = n(point[0])

        for nr_2, point in enumerate(ksi_eta_table):
            for nr_1, n in enumerate(Y_N):
                matrix_eta[nr_2][nr_1] = n(point[1])

        # print("KSI ETA")
        # print(matrix_ksi)
        # print(matrix_eta)

        return {"matrix_ksi": matrix_ksi, "matrix_eta": matrix_eta}


    def Jacobian(self, matrix_eta, matrix_ksi):
        matrix_Jakobian_list = []
        lista_wyznacznikow_Jakkobianow = []
        for i in range(0, self.size_of_local_data):
            matrix_Jakobian = np.zeros((2, 2))
            Ni_eta = matrix_eta[i]
            Ni_ksi = matrix_ksi[i]

            for nr, point in enumerate(self.x_y_table):
                matrix_Jakobian[0, 0] += point[1] * Ni_eta[nr]

            for nr, point in enumerate(self.x_y_table):
                matrix_Jakobian[1, 0] += point[1] * Ni_ksi[nr]

            for nr, point in enumerate(self.x_y_table):
                matrix_Jakobian[0, 1] += point[0] * Ni_eta[nr]

            for nr, point in enumerate(self.x_y_table):
                matrix_Jakobian[1, 1] += point[0] * Ni_ksi[nr]

            # print(f"Jakobian \n{matrix_Jakobian}")

            det = matrix_Jakobian[1, 1] * matrix_Jakobian[0, 0] - matrix_Jakobian[1, 0] * matrix_Jakobian[0, 1]

            matrix_Jakobian1 = np.linalg.inv(matrix_Jakobian)
            # print(f"Wyznacznik {det}")
            lista_wyznacznikow_Jakkobianow.append(det)

            matrix_Jakobian_list.append(matrix_Jakobian)

        return matrix_Jakobian_list

    def derivativeCalculate(self, matrix_Jakobian_list, matrix_eta, matrix_ksi):
        Ni_x = np.zeros((self.size_of_local_data, 4))
        Ni_y = np.zeros((self.size_of_local_data, 4))

        for i, jakobian in enumerate(matrix_Jakobian_list):
            matrix_Jakobian1 = np.linalg.inv(jakobian)
            Ni_eta = matrix_eta[i]
            Ni_ksi = matrix_ksi[i]


            for j in range(0, 4):
                Ni_x_in_row = (matrix_Jakobian1[0][0] * Ni_eta[j] + matrix_Jakobian1[1][0] * Ni_ksi[j])
                Ni_y_in_row = (matrix_Jakobian1[0][1] * Ni_eta[j] + matrix_Jakobian1[1][1] * Ni_ksi[j])
                Ni_x[i][j] = Ni_x_in_row
                Ni_y[i][j] = Ni_y_in_row
        Ni = np.concatenate((Ni_x, Ni_y))
        return Ni


    def localHcalculate(self, matrix_Jakobian_list, Ni):
        Ni_x = Ni[:self.size_of_local_data]
        Ni_y = Ni[self.size_of_local_data:]
        H_map = []

        lista_wyznacznikow_Jakkobianow = []
        for matrix_Jakobian in matrix_Jakobian_list:
            det = matrix_Jakobian[1, 1] * matrix_Jakobian[0, 0] - matrix_Jakobian[1, 0] * matrix_Jakobian[0, 1]
            lista_wyznacznikow_Jakkobianow.append(det)

        for pkt in range(0, self.size_of_local_data):
            H_pkt_x = np.zeros((4, 4))
            H_pkt_y = np.zeros((4, 4))
            Ni_x_pkt = Ni_x[pkt]
            Ni_y_pkt = Ni_y[pkt]
            for i in range(0, 4):
                for j in range(0, 4):
                    H_pkt_x[i][j] = Ni_x_pkt[i] * Ni_x_pkt[j] * self.k * lista_wyznacznikow_Jakkobianow[pkt]
                    H_pkt_y[i][j] = Ni_y_pkt[i] * Ni_y_pkt[j] * self.k * lista_wyznacznikow_Jakkobianow[pkt]

            H_map.append(H_pkt_y + H_pkt_x)

        H = np.zeros((4, self.size_of_local_data))
        if self.size_of_local_data == 4:
            H = integral_4_elements(H_map, 1.0)
        if self.size_of_local_data == 9:
            H = integral_9_elements(H_map, 5.0 / 9.0, 8.0 / 9.0)
        if self.size_of_local_data == 16:
            H = integral_16_elements(H_map, 0.347855, 0.652145)
        return H


class MatricesForElement:

    def jacobian(self, local_data: []):
        jacobian_table = []
        for nodeNumber, node in enumerate(local_data):
            if nodeNumber != len(local_data) - 1:
                L = math.sqrt((local_data[nodeNumber][0] - local_data[nodeNumber + 1][0]) ** 2 +
                              (local_data[nodeNumber][1] - local_data[nodeNumber + 1][1]) ** 2)
                jacobian_table.append(L / 2.0)
            else:
                L = math.sqrt((local_data[nodeNumber][0] - local_data[0][0]) ** 2
                              + (local_data[nodeNumber][1] - local_data[0][1]) ** 2)
                jacobian_table.append(L / 2.0)
        return jacobian_table

class HBC(MatricesForElement):

    def calculateHBC(self, ksi_eta_edges, mask, detList, alfa):
        HBCforElement = np.zeros((4, 4))
        for maskNumber, i in enumerate(mask):
            edge = False
            number2: int = 0
            number1: int = 0
            if maskNumber != len(mask) - 1:
                if i == 1.0 and mask[maskNumber + 1] == 1.0:
                    edge = True
                    number1 = maskNumber
                    number2 = maskNumber + 1

            else:
                if mask[maskNumber] == 1.0 and mask[0] == 1.0:
                    edge = True
                    number1 = maskNumber
                    number2 = 0

            if edge:
                N_matrix = np.zeros((4, 4))
                node = ksi_eta_edges[number1]

                N_matrix_list = []
                for iter in range(0, len(node)):

                    N = [0, 0, 0, 0]
                    if number1 in [0, 2]:
                        N[number1] = (1.0 - (node[iter])[0]) / 2.0
                        N[number2] = (1.0 + (node[iter])[0]) / 2.0
                    if number1 in [1, 3]:
                        N[number1] = (1.0 - (node[iter])[1]) / 2.0
                        N[number2] = (1.0 + (node[iter])[1]) / 2.0

                    N_matrix_for_edge = np.zeros((4, 4))
                    for i in range(0, 4):
                        for j in range(0, 4):
                            N_matrix_for_edge[i][j] += N[i] * N[j] * alfa * detList[number1]  # bo na razie wagi to 1 właśnie :)
                    N_matrix_list.append(N_matrix_for_edge)

                if len(node) == 2:
                    N_matrix = N_matrix_list[0] + N_matrix_list[1]
                if len(node) == 3:
                    N_matrix = integral_3_edges(N_matrix_list)

                HBCforElement += N_matrix

        return HBCforElement


class Pmatrix(MatricesForElement):

    def calculateP(self, ksi_eta_edges, mask, det_list, alfa, t8):
        PforElement = np.zeros(4)
        for maskNumber, i in enumerate(mask):
            edge = False
            number2: int = 0
            number1: int = 0
            if maskNumber != len(mask) - 1:
                if mask[maskNumber] == 1.0 and mask[maskNumber + 1] == 1.0:
                    edge = True
                    number1 = maskNumber
                    number2 = maskNumber + 1

            else:
                if mask[maskNumber] == 1.0 and mask[0] == 1.0:
                    edge = True
                    number1 = maskNumber
                    number2 = 0

            if edge:
                node = ksi_eta_edges[number1]
                N1 = lambda ksi: (1.0-ksi) / 2.0
                N2 = lambda ksi: (1.0+ksi) / 2.0

                N_lambda = [N1, N2]
                P_local = np.zeros(4)
                P_N_list = []
                for iter in range(0, len(node)):
                    N = np.zeros(4)

                    if number1 in [0, 2]:
                        N[number1] = N_lambda[0]((node[iter])[0])
                        N[number2] = N_lambda[1]((node[iter])[0])
                    if number1 in [1, 3]:
                        N[number1] = N_lambda[0]((node[iter])[1])
                        N[number2] = N_lambda[1]((node[iter])[1])

                    P_N_list.append(N)
                if len(node) == 3:
                    N_sum = integral_3_edges(P_N_list)
                if len(node) == 2:
                    N_sum = P_N_list[0] + P_N_list[1]

                P_local += N_sum * det_list[maskNumber] * -1.0 * alfa * t8

                PforElement += P_local

        #print(f"P dla elementu {mask}: \n{PforElement}")
        #print("\n")
        return PforElement
