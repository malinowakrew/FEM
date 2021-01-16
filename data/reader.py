from stiffnessMatrix.net import *


class Reader:
    def __init__(self, path=r"data/data.txt"):
        self.path = path

    def read(self):
        """
        method use to read data form txt format
        :return:
        """
        path = self.path
        with open(path, "r") as file:
            data = file.read()
            file.close()

        table_row = data.split("\n")
        table = {(number.split(":"))[0]: float((number.split(":"))[1].strip()) for number in table_row}
        return table
