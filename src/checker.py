import numpy as np

matrix_A = np.loadtxt('/results/matrix_A.data')
matrix_B = np.loadtxt('/results/matrix_B.data')
matrix_C = np.loadtxt('/results/matrix_C.data')

# Check if the result matrix given by the fox algorithm is correct
# by comparing it with the matrix multiplication using numpy
print((matrix_A @ matrix_B == matrix_C).all())