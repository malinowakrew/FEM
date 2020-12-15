import numpy as np
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

    def edges_ksi_eta(self, delta):
        net = []
        return [[(-1.0/math.sqrt(3), -1.0), (1.0/math.sqrt(3), -1.0)],
                [(-1.0, 1.0 / math.sqrt(3)), (-1.0, -1.0 / math.sqrt(3))],
                [(1.0/math.sqrt(3), 1.0), (-1.0/math.sqrt(3), 1.0)],
                [(1.0, -1.0 / math.sqrt(3)), (1.0, 1.0 / math.sqrt(3))]]

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

class net_16_elements:
    def __init__(self, delta):
        self.net = self.net_ksi_eta(delta)

    def net_ksi_eta(self, delta):
        net = []
        row = [-0.861136, -0.339981, 0.339981, 0.861136]
        for numeri, i in enumerate(row):
            for numerj, j in enumerate(row):
                net.append([i, j])
        return net

    def integral_16_elements(self, function, weight_1, weight_2):
        """
        net = self.net
        result = 0.0
        for number in [0, 2, 6, 8]:
            result += function(net[number][0], net[number][1]) * weight_1 ** 2
        for number in [1, 3, 5, 7]:
            result += function(net[number][0], net[number][1]) * weight_1 * weight_2
        result += function((net[4])[0], (net[4])[1]) * weight_2 ** 2
        """

        result = 0.0
        for number in [0, 3, 12, 15]:
            result += function(self.net[number][0], self.net[number][1]) * weight_1 ** 2
        for number in [1, 2, 4, 7, 8, 11, 13, 14]:
            result += function(self.net[number][0], self.net[number][1]) * weight_1 * weight_2
        for number in [5, 6, 9, 10]:
            result += function(self.net[number][0], self.net[number][1]) * weight_2 ** 2
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

def integral_16_elements(values, weight_1, weight_2):
    result = 0.0
    for number in [0, 3, 12, 15]:
        result += values[number] * weight_1 ** 2
    for number in [1, 2, 4, 7, 8, 11, 13, 14]:
        result += values[number] * weight_1 * weight_2
    for number in [5, 6, 9, 10]:
        result += values[number] * weight_2 ** 2
    return result


def main():
    fun = lambda x, y: -2*x**2*y+2*x*y+4 #-5*x**2*y+2*x*y**2+10
    integral = net_4_elements(1.0/ math.sqrt(3.0))
    print(integral.integral_4_elements(fun, 1.0))

    integral9 = net_9_elements(math.sqrt(3.0/5.0))
    print(integral9.integral_9_elements(fun, 5.0/9.0, 8.0/9.0))

    integral16 = net_16_elements(4)
    print(integral16.integral_16_elements(fun, 0.347855, 0.652145))

if __name__ == "__main__":
    main()