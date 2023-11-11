import fox_MPI as fmpi
import fox_SEC as fsec
import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI
import os 

def graphs(min_e: int, max_e: int, isInt=True):
    times_MPI = {}
    times_SEC = {}
    np.random.seed(69)  # set the seed for the random numbers generator
                        # so that the same numbers are generated in each process 
    for exponent in range(min_e, max_e):
        times_MPI[exponent] = np.zeros(5)
        times_SEC[exponent] = np.zeros(5)
        for i in range(5):
            times_MPI[exponent][i] = fmpi.fox_MPI(exponent, True)
            times_SEC[exponent][i] = fsec.fox_SEC(exponent, True)
    
    if MPI.COMM_WORLD.Get_rank() == 0:

        bar_width = 0.35

        y_MPI = [np.mean(times_MPI[exponent]) for exponent in times_MPI]
        y_SEC = [np.mean(times_SEC[exponent]) for exponent in times_SEC]
        
        x_MPI = np.array([exponent - bar_width/2 for exponent in times_MPI])
        x_SEC = [exponent + bar_width/2 for exponent in times_SEC]

        x_labels = [str(2**exponent) for exponent in times_MPI]

        numtype = 'enteros' if isInt else 'reales'
        plt.figure(figsize=(10, 5))
        plt.title(f'Tiempo de ejecución del algoritmo fox con\nmatrices de números {numtype}.')
        plt.xlabel('Orden de la Matriz')
        plt.ylabel('Tiempo de ejecución (s)')
        plt.xticks(x_MPI + bar_width/2, x_labels)
        plt.yticks([]) 
        bars_MPI = plt.bar(x_MPI, y_MPI, bar_width,label='MPI', color='#EA75FA')
        bars_SEC = plt.bar(x_SEC, y_SEC, bar_width,label='Secuencial', color='#4590FA')
        plt.legend()
        
        for bar in bars_SEC:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:5.5}s', va='bottom', ha='center')

        for bar in bars_MPI:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:5.5}s', va='bottom', ha='center')  # va: vertical alignment

        if not os.path.exists('graphs'):
            os.makedirs('graphs')
        if not os.path.exists(f'graphs/{2**(min_e)}-{2**(max_e-1)}'):
            os.makedirs(f'graphs/{2**(min_e)}-{2**(max_e-1)}')
        plt.savefig(f'graphs/{2**(min_e)}-{2**(max_e-1)}/fox_{numtype}_{2**(min_e)}-{2**(max_e-1)}.png')

def main():
    # graphs( 6,  9, isInt=True)
    # graphs( 6,  9, isInt=False)
    graphs( 9, 12, isInt=True)
    graphs( 9, 12, isInt=False)
    # graphs(12, 14, isInt=True)
    # graphs(12, 14, isInt=False)

if __name__ == '__main__':
    main()