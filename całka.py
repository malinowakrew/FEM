from siatka import *
import math

class net_4_elements():
    def __init__ (self, delta):
        self.net = self.net_ksi_eta(delta)

    def net_ksi_eta(self, delta):
        net = []
        for y in range(0, 2):
            for x in range(0, 2):
                net.append([-delta + (2 * x * delta), -delta + (2 * y * delta)])
        return net

    def integral_4_elements(self, function, weight):
        result = 0.0
        for node in self.net:
            result += function(node[0], node[1]) * weight
        return result


class net_9_elements():
    def __init__(self, delta):
        self.net = self.net_ksi_eta(delta)

    def net_ksi_eta(self, delta):
        net = []
        for y in range(0, 3):
            for x in range(0, 3):
                net.append([-delta + (x * delta), -delta + (y * delta)])
        return net

    def integral_9_elements(self, function, weight_1, weight_2):
        net = self.net
        result = 0.0
        for number in [0, 2, 6, 8]:
            result += function(net[number][0], net[number][1]) * weight_1 ** 2
        for number in [1, 3, 5, 7]:
            result += function(net[number][0], net[number][1]) * weight_1 * weight_2
        result += function((net[4])[0], (net[4])[1]) * weight_2 ** 2
        return result

#### PRÓBA ####
def integral_4_elements(values, weight):
    result = 0.0
    for numberNode, node in enumerate(values):
        result += node * weight
    return result

def integral_9_elements(values, weight_1, weight_2):
    result = 0.0
    for number in [0, 2, 6, 8]:
        result += values[number] * weight_1 ** 2
    for number in [1, 3, 5, 7]:
        result += values[number] * weight_1 * weight_2
    result += values[4] * weight_2 ** 2
    return result


def test():
    path = r"dane.txt"
    with open(path, "r") as file:
        data = file.read()
        file.close()

    data_table = data.split("\n")

    equation = lambda x, y : eval(data_table[4])

    net = net_9_elements(0.77)
    res = net.integral_9_elements(equation, 5.0/9.0, 8.0/9.0)
    print("for 9 elements {}".format(res))

    net_4 = net_4_elements(-1.0/math.sqrt(3))
    res_4 = net_4.integral_4_elements(equation, 1.0)
    print("for 4 elements {}".format(res_4))



