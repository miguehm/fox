import numpy as np

matrix_A = np.loadtxt('arrayA.txt')
matrix_B = np.loadtxt('arrayB.txt')
matrix_C = np.loadtxt('result.txt')

# Check if the result matrix given by the fox algorithm is correct
# by comparing it with the matrix multiplication using numpy
print((matrix_A @ matrix_B == matrix_C).all())

print(matrix_C)
print(matrix_A @ matrix_B)