import numpy as np
import math
from stiffnessMatrix.integral import *

def PMatrixCalculate(ksi_eta_table, ro, c, matrix_Jakobian_list):
    size_of_local_data = len(ksi_eta_table)

    #Poszczególne N
    N1 = lambda ksi, eta: (1.0-ksi)*(1.0-eta)/4.0
    N2 = lambda ksi, eta: (1.0+ksi)*(1.0-eta)/4.0
    N3 = lambda ksi, eta: (1.0+ksi)*(1.0+eta)/4.0
    N4 = lambda ksi, eta: (1.0-ksi)*(1.0+eta)/4.0
    N = [N1, N2, N3, N4]

    matrixN = np.zeros((size_of_local_data, 4))
    for numberPoint, point in enumerate(ksi_eta_table):
        for numberNp, Np in enumerate(N):
            matrixN[numberPoint, numberNp] = Np(point[0], point[1]) #* jakobiany_tymczasowe[numberPoint]

    #print(matrixN)


    #Jakobiany - potrzebna refaktoryzacja kodu umożliwiająca liczenie jakobianów
    lista_wyznacznikow_Jakkobianow =[]
    for matrix_Jakobian in matrix_Jakobian_list:
        det = matrix_Jakobian[1, 1] * matrix_Jakobian[0, 0] - matrix_Jakobian[1, 0] * matrix_Jakobian[0, 1]
        lista_wyznacznikow_Jakkobianow.append(det)

    #P

    P_map = []
    for pkt in range(0, size_of_local_data):
        P_pkt = np.zeros((4, 4))
        Ni_pkt = matrixN[pkt]
        for i in range(0, 4):
            for j in range(0, 4):
                P_pkt[i][j] = Ni_pkt[i] * Ni_pkt[j] * ro * c * lista_wyznacznikow_Jakkobianow[pkt]

        P_map.append(P_pkt)

    P = np.zeros((4, 4))
    if size_of_local_data == 4:
        P = integral_4_elements(P_map, 1.0)
    if size_of_local_data == 9:
        P = integral_9_elements(P_map, 5.0/9.0, 8.0/9.0)

    return P
