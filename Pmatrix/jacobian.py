import numpy as np

def Jacobian(matrix_eta, matrix_ksi, x_y_table, size_of_local_data):
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

        # print(f"Jakobian \n{matrix_Jakobian}")

        det = matrix_Jakobian[1, 1] * matrix_Jakobian[0, 0] - matrix_Jakobian[1, 0] * matrix_Jakobian[0, 1]

        matrix_Jakobian1 = np.linalg.inv(matrix_Jakobian)
        # print(f"Wyznacznik {det}")
        lista_wyznacznikow_Jakkobianow.append(det)

    return lista_wyznacznikow_Jakkobianow