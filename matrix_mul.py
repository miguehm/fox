import numpy as np
from mpi4py import MPI

# Read data

comm = MPI.COMM_WORLD # incluye todos los procesos en la ejecución
size = comm.Get_size() # Numero total de procesos en la ejecución de MPI
rank = comm.Get_rank() # El rango de procesos (desde 0 hasta size-1)

if rank == 0: # Se encuentra en el proceso 0
    
    exponent = input("Ingrese el tamaño de la matriz: 2**")
    exponent = int(exponent)

    if exponent > 13:
        print("El orden máximo es de 2^13 = 8192")
        comm.Abort()

    n = 2**exponent

    # Generating matrices
    A = np.random.randint(1000, 2000, (n,n))
    B = np.random.randint(1000, 2000, (n,n))
    C = np.zeros((n,n), dtype=int)
    
    print(f'{A = }')
    print(f'{B = }')
    
    # Se envía a cada core
    comm.send((A, B, C), dest=0, tag=1)
    comm.send((A, B, C), dest=1, tag=1)
    comm.send((A, B, C), dest=2, tag=1)
    comm.send((A, B, C), dest=3, tag=1)
    
    # ----------
    
    # A, B, C = comm.recv(source=0, tag=1)
    
for i in range(size):
    if rank == i:
        A, B, C = comm.recv(source=0, tag=1)
        print(f"{C = }")
        # receive
