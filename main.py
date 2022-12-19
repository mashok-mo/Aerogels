import bezier
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()



class Field:
    def __init__(self, size):
        self.__matrix = []
        self.__size = size
    @property
    def matrix(self):
        return self.__matrix
    @property
    def size(self):
        return self.__size
    def init_render(self):
        self.__matrix = [0] * self.__size
        for i in range(self.__size):
            self.__matrix[i] = [0] * self.__size
    def print(self):
        for i in range(len(self.__matrix)):
            for j in range(0, len(self.__matrix[i])):
                print(self.__matrix[i][j], end=' ')
            print()
    def count_elements(self):
        count = 0
        for element in self.__matrix:
            count += len(element)
        return(count)
    def count_ones(self):
        count = 0
        for i in range(0, len(self.__matrix)):
            for j in range(0, len(self.__matrix[i])):
                if self.__matrix[i][j] == 1:
                    count += 1
        return(count)

class Controller:
    def __init__(self, required_porosity, thick):
        self.__required_porosity = required_porosity
        self.__thick = thick
    @property
    def required_porosity(self):
        return self.__required_porosity
    @property
    def thick(self):
        return self.__thick
    def count_porosity(self, matrix):
        return(1-matrix.count_ones()/matrix.count_elements())
    def create_fiber(self, size):
        seed = random.randint(1, 2)
        if seed == 1:
            point = np.asfortranarray([[0, random.randint(0, size-1)], [random.randint(0, size-1), random.randint(0, size-1)],
                                       [random.randint(0, size-1), random.randint(0, size-1)], [size-1, random.randint(0, size-1)]])
        else:
            point = np.asfortranarray([[random.randint(0, size-1), 0], [random.randint(0, size-1), random.randint(0, size-1)],
                                       [random.randint(0, size-1), random.randint(0, size-1)], [random.randint(0, size-1), size-1]])
        curve = bezier.curve.Curve(point, degree=3)
        s_vals = np.linspace(0, 1.0, size*3)
        array = curve.evaluate_multi(s_vals)
        curve_point = []
        for i in range(0, len(array)):
            for j in range(0, len(array[i])):
                curve_point.append(round(array[i][j]))
        return (curve_point)
    def update(self, matrix, curve_point):
        for i in range(0, len(curve_point), 2):
            matrix.matrix[curve_point[i]][curve_point[i + 1]] = 1
            self.create_thickness(matrix, curve_point[i], curve_point[i+1], self.__thick)
    def create_thickness(self, matrix, cx, cy, thick):
        for x in range(cx - thick, cx + thick):
            for y in range(cy - thick, cy + thick):
                if x < matrix.size and y < matrix.size and x >= 0 and y >= 0:
                    if math.sqrt((cx - x) ** 2 + (cy - y) ** 2) <= thick:
                        matrix.matrix[x][y] = 1
    def check_porosity(self, matrix):
        if self.count_porosity(matrix) <= self.__required_porosity:
            return(True)

def main():
    size = int(input('Введите размер поля: '))
    field = Field(size)
    field.init_render()
    required_porosity = int(input('Введите значение пористости, %: '))/100
    thick = round(float(input('Введите диаметр волокна, нм: '))/4)
    controller = Controller(required_porosity, thick)
    while True:
        controller.update(field, controller.create_fiber(field.size))
        if controller.check_porosity(field) == True:
            break
    #field.print()
    plt.pcolormesh(field.matrix, cmap = "copper")
    plt.show()
main()