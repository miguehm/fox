import numpy as np

matrix_A = np.loadtxt('arrayA.txt', dtype=int)
matrix_B = np.loadtxt('arrayB.txt', dtype=int)
matrix_C = np.loadtxt('result.txt', dtype=int)


print(f'{matrix_A =}')
print(f'{matrix_B =}')
print(f'{matrix_C =}')

# Check if the result matrix given by the fox algorithm is correct
# by comparing it with the matrix multiplication using numpy
print(f'Is the result matrix correct: {(matrix_A @ matrix_B).all() == matrix_C.all()}')