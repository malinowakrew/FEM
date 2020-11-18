import numpy as np

def form (xy_eta_table, x_y_table):
    """"
    N1 = (1.0-xy)(1.0-eta)/4.0
    N2 = (1.0+xy)(1.0-eta)/4.0
    N3 = (1.0+xy)(1.0+eta)/4.0
    N4 = (1.0-xy)(1.0+eta)/4.0
    """
    Y_N1_dev_xy = lambda xy: (1.0-xy)/-4.0
    Y_N2_dev_xy = lambda xy: (1.0+xy)/-4.0
    Y_N3_dev_xy = lambda xy: (1.0+xy)/4.0
    Y_N4_dev_xy = lambda xy: (1.0-xy)/4.0
    Y_N = [Y_N1_dev_xy, Y_N2_dev_xy, Y_N3_dev_xy, Y_N4_dev_xy]

    X_N1_dev_eta = lambda eta: (1.0 - eta) /-4.0
    X_N2_dev_eta = lambda eta: (1.0 - eta) /4.0
    X_N3_dev_eta = lambda eta: (1.0 + eta) / 4.0
    X_N4_dev_eta = lambda eta: (1.0 + eta) / -4.0
    X_N = [X_N1_dev_eta, X_N2_dev_eta, X_N3_dev_eta, X_N4_dev_eta]

    matrix_xy = np.zeros((4,4))
    matrix_eta = np.zeros((4, 4))

    for nr_1, n in enumerate(X_N):
        for nr_2, point in enumerate(xy_eta_table):
            matrix_xy[nr_2][nr_1] = n(point[0])

    for nr_1, n in enumerate(Y_N):
        for nr_2, point in enumerate(xy_eta_table):
            matrix_eta[nr_2][nr_1] = n(point[1])

    #print(matrix_xy)
    #print(matrix_eta)

    Ni_x = np.zeros((4,4))
    Ni_y = np.zeros((4,4))


    for i in range(0,4):
        matrix = np.zeros((2, 2))
        Ni_eta = matrix_eta[i]
        equal = Ni_eta
        Ni_ksi = matrix_xy[i]
        equal2 = Ni_ksi

        for nr, point in enumerate(x_y_table):
            matrix[1, 1] += point[0] * equal[nr]

        for nr, point in enumerate(x_y_table):
            matrix[1, 0] += -point[0] * equal2[nr]

        for nr, point in enumerate(x_y_table):
            matrix[0, 1] += -point[1] * equal[nr]

        for nr, point in enumerate(x_y_table):
            matrix[0, 0] += point[1] * equal2[nr]

        det = matrix[1,1] * matrix[0,0] - matrix[1,0] * matrix[0, 1]
        #print(det)

        #print(matrix)
        for j in range(0,4):
            Ni_x_in_row = (matrix[0][0] * equal[j] + matrix[0][1] * equal2[j])* 1.0/det
            Ni_y_in_row = (matrix[1][0] * equal[j] + matrix[1][1] * equal2[j])* 1.0/det
            Ni_x[i][j] = Ni_x_in_row
            Ni_y[i][j] = Ni_y_in_row

    print("wyniki dla N po y")
    print(Ni_y)
    print("wyniki dla N po x")
    print(Ni_x)
    

def adas():
    tab = (4, 5, 6, 7)
    tab2 = [[4, 5], [6,7]]
    martix = np.matrix(tab2)

    print(matrix)

    #print(tab[1][1])


if __name__ == "__main__":
    adas()