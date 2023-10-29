from mpi4py import MPI

comm = MPI.COMM_WORLD # incluye todos los procesos en la ejecución
size = comm.Get_size() # Numero total de procesos en la ejecución de MPI
rank = comm.Get_rank() # El rango de procesos (desde 0 hasta size-1)

# print(f'Size: {size}')
# print(f'Actual process: {rank}')

# Laptop tiene 2 nucleos, entonces:
# size: 2
# rank: 0, 1

if rank == 0: # Se encuentra en el proceso 0
    a = 4
    b = 2
    c = 3
    d = 5
    comm.send([a*b, c*d], dest=1) # Envia la info al proceso 1
elif rank == 1:
    s = comm.recv()
    print(f'{s[0] + s[1]}')
    # print("rank %d: %s" % (rank, s))
else:
    print("rank %d: idle" % (rank))
