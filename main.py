import bezier
import numpy as np
import random
import math
import matplotlib.pyplot as plt

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
            for j in range(self.__size):
                self.__matrix[i][j] = [0] * self.__size
    def count_ones(self):
        count = 0
        for x in range(0, self.__size):
            for y in range(0, self.__size):
                for z in range(0, self.__size):
                    if self.__matrix[x][y][z] == 1:
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
        return(matrix.count_ones()/matrix.size**3)
    def create_thickness(self, matrix, cx, cy, thick):
        point_x = []
        for x in range(cx - thick, cx + thick):
            for y in range(cy - thick, cy + thick):
                if x < matrix.size and y < matrix.size and x >= 0 and y >= 0:
                    if math.sqrt((cx - x) ** 2 + (cy - y) ** 2) <= thick:
                        point_x.append(x)
                        point_x.append(y)
        return (point_x)
    def create_bezier_curve(self, point, size):
        curve = bezier.curve.Curve(point, degree=3)
        s_vals = np.linspace(0, 1.0, size * 5)
        array = curve.evaluate_multi(s_vals)
        curve_point = []
        for x in range(0, len(array)):
            for y in range(0, len(array[x])):
                curve_point.append(math.ceil(array[x][y]))
        return (curve_point)
    def create_fiber(self, matrix):
        seed = random.randint(1, 3)
        if seed == 1:
            point = np.asfortranarray([[0, random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1)],
                                       [random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1)],
                                       [random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1)],
                                       [matrix.size - 1, random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1)]])
            curve_point = self.create_bezier_curve(point, matrix.size)
            for i in range(0, len(curve_point), 3):
                matrix.matrix[curve_point[i]][curve_point[i + 1]][curve_point[i + 2]] = 1
                point_x = self.create_thickness(matrix, curve_point[i+2], curve_point[i + 1], self.__thick)
                for x in range (0,len(point_x),2):
                    matrix.matrix[curve_point[i]][point_x[x+1]][point_x[x]] = 1
        elif seed == 2:
            point = np.asfortranarray([[random.randint(0, matrix.size - 1), 0, random.randint(0, matrix.size - 1)],
                                       [random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1)],
                                       [random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1)],
                                       [random.randint(0, matrix.size - 1), matrix.size-1, random.randint(0, matrix.size - 1)]])
            curve_point = self.create_bezier_curve(point, matrix.size)
            for i in range(0, len(curve_point), 3):
                matrix.matrix[curve_point[i]][curve_point[i + 1]][curve_point[i + 2]] = 1
                point_x = self.create_thickness(matrix, curve_point[i+2], curve_point[i], self.__thick)
                for x in range (0,len(point_x),2):
                    matrix.matrix[point_x[x+1]][curve_point[i+1]][point_x[x]] = 1
        elif seed == 3:
            point = np.asfortranarray([[random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1), 0],
                                       [random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1)],
                                       [random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1)],
                                       [random.randint(0, matrix.size - 1), random.randint(0, matrix.size - 1), matrix.size - 1]])
            curve_point = self.create_bezier_curve(point, matrix.size)
            for i in range(0, len(curve_point), 3):
                matrix.matrix[curve_point[i]][curve_point[i + 1]][curve_point[i + 2]] = 1
                point_x = self.create_thickness(matrix, curve_point[i], curve_point[i+1], self.__thick)
                for x in range (0,len(point_x),2):
                    matrix.matrix[point_x[x+1]][point_x[x]][curve_point[i + 2]] = 1
    def create_xyz(self, matrix):
        global x,y,z
        x = []
        y = []
        z = []
        for i in range(0, matrix.size):
            for j in range(0, matrix.size):
                for k in range(0, matrix.size):
                    if matrix.matrix[i][j][k] == 1:
                        x.append(i)
                        y.append(j)
                        z.append(k)

    def check_porosity(self, matrix):
        if self.count_porosity(matrix) > self.__required_porosity:
            return(False)

def main():
    size = int(input('Введите размер поля: '))
    field = Field(size)
    field.init_render()
    required_porosity = 1 - int(input('Введите значение пористости, %: '))/100
    thick = round(float(input('Введите диаметр волокна, нм: '))/4)
    controller = Controller(required_porosity, thick)
    controller.create_fiber(field)
    while controller.check_porosity(field) != False:
        controller.create_fiber(field)
    controller.create_xyz(field)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(x, y, z, edgecolors='black')
    plt.show()
main()