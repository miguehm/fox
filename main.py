import os 
import subprocess
import numpy as np
import matplotlib.pyplot as plt

def run_mpi_file(mpi_file_path, exponent, isInt=True):
    result = subprocess.run(['mpiexec', '-n', '8', 'python', mpi_file_path, f'{exponent}', f'{isInt}'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def run_sec_file(sec_file_path, exponent, isInt=True):
    result = subprocess.run(['python', sec_file_path, f'{exponent}', f'{isInt}'], stdout=subprocess.PIPE)  
    return result.stdout.decode('utf-8')  

def graphs(min_e, max_e, isInt=True):
    times_MPI = {}
    times_SEC = {}
    np.random.seed(69)  # set the seed for the random numbers generator
                        # so that the same numbers are generated in each process
    for exponent in range(min_e, max_e):
        times_MPI[exponent] = np.zeros(5)
        times_SEC[exponent] = np.zeros(5)
        print(f'Calculating for {2**exponent}...')
        for i in range(5):
            times_SEC[exponent][i] = run_sec_file('fox_SEC.py', exponent, isInt=isInt)
            times_MPI[exponent][i] = run_mpi_file('fox_MPI.py', exponent, isInt=isInt)

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
    bars_MPI = plt.bar(x_MPI, y_MPI, bar_width, label='MPI',        color='#EA75FA')
    bars_SEC = plt.bar(x_SEC, y_SEC, bar_width, label='Secuencial', color='#4590FA')
    plt.legend()
    
    for bar in bars_SEC + bars_MPI:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:5.5}s', va='bottom', ha='center')

    OM_min, OM_max = 2**(min_e), 2**(max_e-1)
    if not os.path.exists('graphs'):
        os.makedirs('graphs')

    if not os.path.exists(f'graphs/{OM_min}-{OM_max}'):
        os.makedirs(f'graphs/{OM_min}-{OM_max}')

    plt.savefig(f'graphs/{OM_min}-{OM_max}/fox_{numtype}_{OM_min}-{OM_max}.png')

def main():

    #! WARNING: This will take a long time to run. If you want to run it, uncomment the lines below.
    #* We recommend you to run one call to graphs() at a time.
    graphs(6, 9, isInt=True)
    # graphs(6, 9, isInt=False)
    # graphs(9, 12, isInt=True)
    # graphs(9, 12, isInt=False)
    # graphs(12, 14, isInt=True)
    # graphs(12, 14, isInt=False)
    
if __name__ == '__main__':
    main()