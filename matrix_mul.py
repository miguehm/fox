import numpy as np
from mpi4py import MPI

# Read data

comm = MPI.COMM_WORLD # incluye todos los procesos en la ejecución
size = comm.Get_size() # Numero total de procesos en la ejecución de MPI
rank = comm.Get_rank() # El rango de procesos (desde 0 hasta size-1)

if rank == 0: # Se encuentra en el proceso 0
    A = np.random.randint(1000, 2000, (4,4))
    B = np.random.randint(1000, 2000, (4,4))
    
    comm.send((A, B, 1), dest=0, tag=11)
    
    A, B, dato = comm.recv(source=0, tag=11)

    if(dato):
        print("hola")
    
    print(f'{A = }')
    print(f'{B = }')
    
elif rank == 1:
    pass
    # A, B = comm.recv(source=0, tag=11)
    # print(f'{A = }')
    # print(f'{B = }')
    
elif rank == 2:
    pass
    # A, B = comm.recv(source=0, tag=11)
    # print("Proceso 2")
    # print(f'{A = }')
    # print(f'{B = }')
    
elif rank == 3:
    pass
    # A, B = comm.recv(source=0, tag=11)
    # print("Proceso 3")
    # print(f'{A = }')
    # print(f'{B = }')
    
else:
    pass
