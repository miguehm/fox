import numpy as np

matrix_A = np.loadtxt('arrayA.txt', dtype=int)
matrix_B = np.loadtxt('arrayB.txt', dtype=int)
matrix_C = np.loadtxt('result.txt', dtype=int)

# Check if the result matrix given by the fox algorithm is correct
# by comparing it with the matrix multiplication using numpy
print((matrix_A @ matrix_B == matrix_C).all())