from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Crear dos matrices A y B
A = np.random.rand(100, 100)
B = np.random.rand(100, 100)

# Dividir las matrices en submatrices
sub_As = np.array_split(A, size)
sub_Bs = np.array_split(B, size)

# Cada proceso realiza la multiplicación de matrices en su submatriz correspondiente
if rank == 0:
    sub_Cs = [None] * size
else:
    sub_Cs = None

sub_C = np.dot(sub_As[rank], sub_Bs[rank])

# Cada proceso envía su submatriz resultante al proceso principal
comm.send(sub_C, dest=0, tag=rank)

if rank == 0:
    for i in range(1, size):
        sub_Cs[i] = comm.recv(source=i, tag=i)
    # Combinar las submatrices resultantes en la matriz resultante
    C = np.concatenate(sub_Cs, axis=0)
    print(C)
