import bezier
import numpy as np
import random

matrix = [' '] * 100
for i in range(100):
    matrix[i] = [' '] * 100

while True:
    seed = random.randint(1,2)
    if seed == 1:
        point = np.asfortranarray([[0,random.randint(0,99)],[random.randint(0,99),random.randint(0,99)],[random.randint(0,99),random.randint(0,99)],[99,random.randint(0,99)]])
    if seed == 2:
        point = np.asfortranarray([[random.randint(0,99),0],[random.randint(0,99),random.randint(0,99)],[random.randint(0,99),random.randint(0,99)],[random.randint(0,99),99]])
    curve = bezier.curve.Curve(point, degree = 3)
    s_vals = np.linspace(0, 1.0, 500)
    array = curve.evaluate_multi(s_vals)
    new_array = []
    for i in range(0, len(array)):
        for j in range(0, len(array[i])):
            new_array.append(round(array[i][j]))
    for i in range(0, len(new_array),2):
        matrix[new_array[i]][new_array[i+1]] = 1
    count = 0
    one = 0
    for element in matrix:
        count += len(element)
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if matrix[i][j] == 1:
                one +=1
    new_array.clear()
    if one/count >= 0.05:
        break

for i in range(100):
    for j in range(0, len(matrix[i])):
        print(matrix[i][j], end=' ')
    print()

#print(new_array)