from mpi4py import MPI
import numpy as np

def big_job(a, b):
    # Aquí va el código para realizar el trabajo pesado
    print("hola")

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Crear un espacio de parámetros para explorar
arr_a = np.linspace(0.03, 0.5, 36)
arr_b = np.linspace(0.05, 0.95, 36)

# Distribuir los trabajos entre los procesos
jobs = [(a, b) for a in arr_a for b in arr_b]
np.random.shuffle(jobs)

for i in range(size):
    if rank == i:
        a, b = jobs[i]
        big_job(a, b)
