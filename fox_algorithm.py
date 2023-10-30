import numpy as np
from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
np.random.seed(69)
if rank == 0:
    exponent = input("El tamaño de la matriz esta dado por la forma 2^n.\nIngrese el valor de n: ")
    exponent = int(exponent)
    if exponent > 13:
        print("El orden máximo es de 2^13 = 8192")
        comm.Abort()

    MATRIX_SIZE = 2**exponent
    matrix_A    = np.random.randint(1000, 2000, (MATRIX_SIZE, MATRIX_SIZE)) 
    matrix_B    = np.random.randint(1000, 2000, (MATRIX_SIZE, MATRIX_SIZE))
    matrix_C    = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
    data        = (MATRIX_SIZE, matrix_A, matrix_B, matrix_C)
else:
    data = None
data = comm.bcast(data, root=0)
MATRIX_SIZE, matrix_A, matrix_B, matrix_C = data

for row in range(MATRIX_SIZE): 
    if rank == row % size and rank < MATRIX_SIZE:
        for i in range(MATRIX_SIZE):
            col = (row + i) % MATRIX_SIZE
            matrix_C[row] += matrix_A[row, col] * matrix_B[col]
    comm.Allreduce(MPI.IN_PLACE, matrix_C[row], op=MPI.SUM)

if rank == 0:
    
    print(f'{repr(matrix_A)}\n')
    print(f'{repr(matrix_B)}\n')
    print(f'{repr(matrix_C)}')
    np.savetxt('arrays0.txt', matrix_A, fmt='%d')
    np.savetxt('arrays1.txt', matrix_B, fmt='%d')
    np.savetxt('arrays2.txt', matrix_C, fmt='%d')
    print('#############################')
