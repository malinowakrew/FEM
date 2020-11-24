import numpy as np
from stiffnessMatrix.integral import *


def form (ksi_eta_table, x_y_table, k):
    """"
    N1 = (1.0-ksi)(1.0-eta)/4.0
    N2 = (1.0+ksi)(1.0-eta)/4.0
    N3 = (1.0+ksi)(1.0+eta)/4.0
    N4 = (1.0-ksi)(1.0+eta)/4.0
    """
    size_of_local_data = len(ksi_eta_table)

    Y_N1_dev_ksi = lambda ksi: (1.0-ksi)/-4.0
    Y_N2_dev_ksi = lambda ksi: (1.0+ksi)/-4.0
    Y_N3_dev_ksi = lambda ksi: (1.0+ksi)/4.0
    Y_N4_dev_ksi = lambda ksi: (1.0-ksi)/4.0
    Y_N = [Y_N1_dev_ksi, Y_N2_dev_ksi, Y_N3_dev_ksi, Y_N4_dev_ksi]

    X_N1_dev_eta = lambda eta: (1.0 - eta)/-4.0
    X_N2_dev_eta = lambda eta: (1.0 - eta)/4.0
    X_N3_dev_eta = lambda eta: (1.0 + eta)/4.0
    X_N4_dev_eta = lambda eta: (1.0 + eta)/-4.0
    X_N = [X_N1_dev_eta, X_N2_dev_eta, X_N3_dev_eta, X_N4_dev_eta]

    matrix_ksi = np.zeros((size_of_local_data, 4))
    matrix_eta = np.zeros((size_of_local_data, 4))

    for nr_2, point in enumerate(ksi_eta_table):
        for nr_1, n in enumerate(X_N):
            matrix_ksi[nr_2][nr_1] = n(point[0])

    for nr_2, point in enumerate(ksi_eta_table):
        for nr_1, n in enumerate(Y_N):
            matrix_eta[nr_2][nr_1] = n(point[1])

    #print("KSI ETA")
    #print(matrix_ksi)
    #print(matrix_eta)

    Ni_x = np.zeros((size_of_local_data, 4))
    Ni_y = np.zeros((size_of_local_data, 4))

    lista_wyznacznikow_Jakkobianow = []
    for i in range(0, size_of_local_data):
        matrix_Jakobian = np.zeros((2, 2))
        Ni_eta = matrix_eta[i]
        Ni_ksi = matrix_ksi[i]


        for nr, point in enumerate(x_y_table):
            matrix_Jakobian[0, 0] += point[1] * Ni_eta[nr]

        for nr, point in enumerate(x_y_table):
            matrix_Jakobian[1, 0] += point[1] * Ni_ksi[nr]

        for nr, point in enumerate(x_y_table):
            matrix_Jakobian[0, 1] += point[0] * Ni_eta[nr]

        for nr, point in enumerate(x_y_table):
            matrix_Jakobian[1, 1] += point[0] * Ni_ksi[nr]

        #print(f"Jakobian \n{matrix_Jakobian}")

        det = matrix_Jakobian[1, 1] * matrix_Jakobian[0, 0] - matrix_Jakobian[1, 0] * matrix_Jakobian[0, 1]

        matrix_Jakobian1 = np.linalg.inv(matrix_Jakobian)
        #print(f"Wyznacznik {det}")
        lista_wyznacznikow_Jakkobianow.append(det)

        #print(f"Jakobian odwrócony \n {matrix_Jakobian1}")

        #print(matrix)
        for j in range(0, 4):
            Ni_x_in_row = (matrix_Jakobian1[0][0] * Ni_eta[j] + matrix_Jakobian1[1][0] * Ni_ksi[j])
            Ni_y_in_row = (matrix_Jakobian1[0][1] * Ni_eta[j] + matrix_Jakobian1[1][1] * Ni_ksi[j])
            Ni_x[i][j] = Ni_x_in_row
            Ni_y[i][j] = Ni_y_in_row

    #print("d{{N}}/dx")
    #print(Ni_y)
    #print("d{{N}}/dy")
    #print(Ni_x)


    H_map = []
    for pkt in range(0, size_of_local_data):
        H_pkt_x = np.zeros((4, 4))
        H_pkt_y = np.zeros((4, 4))
        Ni_x_pkt = Ni_x[pkt]
        Ni_y_pkt = Ni_y[pkt]
        for i in range(0, 4):
            for j in range(0, 4):
                H_pkt_x[i][j] = Ni_x_pkt[i] * Ni_x_pkt[j] * k * lista_wyznacznikow_Jakkobianow[pkt]
                H_pkt_y[i][j] = Ni_y_pkt[i] * Ni_y_pkt[j] * k * lista_wyznacznikow_Jakkobianow[pkt]

        H_map.append(H_pkt_y+H_pkt_x)
        #print(f"H lokalne dla punktu {pkt}")
        #print(H_pkt_y+H_pkt_x)

    H = np.zeros((4, size_of_local_data))
    if(size_of_local_data == 4):
        #H += (H_pkt_x + H_pkt_y)
        H = integral_4_elements(H_map, 1.0)
    if(size_of_local_data == 9):
        H = integral_9_elements(H_map, 5.0/9.0, 8.0/9.0)

        #print(f"\n\n\n H dla {pkt} \n{(H_pkt_x + H_pkt_y) * 30.0 * det}")
        #print(f"Macierz H  dla punktu nr {pkt} \n{H_pkt_x}")
        #print(f"Macierz H x dla punktu nr {pkt} \n{H_pkt_y}")

    #print(f"\n\n\nMatrix H \n{H}")
    return H
