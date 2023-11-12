import os 
import subprocess
import numpy as np
import matplotlib.pyplot as plt

def run_mpi_file(mpi_file_path, exponent, isInt=True):
    result = subprocess.run(['mpiexec', '-n', '4', 'python', mpi_file_path, f'{exponent}', f'{isInt}'], stdout=subprocess.PIPE, text=True)
    #return result.stdout.decode('utf-8')
    return result.stdout.splitlines()

def run_sec_file(sec_file_path, exponent, isInt=True):
    result = subprocess.run(['python', sec_file_path, f'{exponent}', f'{isInt}'], stdout=subprocess.PIPE, text=True)  
    #return result.stdout.decode('utf-8')  
    return result.stdout.splitlines()

def graphs(min_e, max_e, isInt=True):
    times_MPI = {}
    times_SEC = {}
    memory_MPI = {}
    memory_SEC = {}
    np.random.seed(69)  # set the seed for the random numbers generator
                        # so that the same numbers are generated in each process

    if not os.path.exists('graphs'):
        os.makedirs('graphs')
        
    if not os.path.exists(f'graphs/{2**(min_e)}-{2**(max_e-1)}'):
        os.makedirs(f'graphs/{2**(min_e)}-{2**(max_e-1)}')

    if not os.path.exists(f'graphs/{2**(min_e)}-{2**(max_e-1)}'):
        os.makedirs(f'graphs/{2**(min_e)}-{2**(max_e-1)}')

    for exponent in range(min_e, max_e):
        times_MPI[exponent] = np.zeros(5)
        times_SEC[exponent] = np.zeros(5)
        memory_MPI[exponent] = np.zeros(5)
        memory_SEC[exponent] = np.zeros(5)
        print(f'Calculating for 2^{exponent}...')
        for i in range(5):
            times_SEC[exponent][i], memory_SEC[exponent][i]= run_sec_file('fox_SEC.py', exponent, isInt=isInt)
            times_MPI[exponent][i], memory_MPI[exponent][i]= run_mpi_file('fox_MPI.py', exponent, isInt=isInt)

    bar_width = 0.35

    y_MPI = [np.mean(times_MPI[exponent]) for exponent in times_MPI]
    y_SEC = [np.mean(times_SEC[exponent]) for exponent in times_SEC]
    
    x_MPI = np.array([exponent - bar_width/2 for exponent in times_MPI])
    x_SEC = [exponent + bar_width/2 for exponent in times_SEC]

    y_memory_MPI = [np.mean(memory_MPI[exponent]) for exponent in memory_MPI]
    y_memory_SEC = [np.mean(memory_SEC[exponent]) for exponent in memory_SEC]

    x_memory_MPI = np.array([exponent - bar_width/2 for exponent in memory_MPI])
    x_memory_SEC = [exponent + bar_width/2 for exponent in memory_SEC]

    # ========================== Time ==========================
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

    plt.savefig(f'graphs/{2**(min_e)}-{2**(max_e-1)}/fox_{numtype}_{2**(min_e)}-{2**(max_e-1)}.png')

    # ========================== Memory ==========================
    x_labels = [str(2**exponent) for exponent in memory_MPI]
    numtype = 'enteros' if isInt else 'reales'

    plt.figure(figsize=(10, 5))
    plt.title(f'Memoria del algoritmo fox con\nmatrices de números {numtype}.')
    plt.xlabel('Orden de la Matriz')
    plt.ylabel('Memoria (MB)')
    plt.xticks(x_memory_MPI + bar_width/2, x_labels)
    plt.yticks([]) 
    bars_MPI = plt.bar(x_memory_MPI, y_memory_MPI, bar_width, label='MPI',        color='#EA75FA')
    bars_SEC = plt.bar(x_memory_SEC, y_memory_SEC, bar_width, label='Secuencial', color='#4590FA')
    plt.legend()

    for bar in bars_SEC + bars_MPI:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval/1024} MB', va='bottom', ha='center')

    plt.savefig(f'graphs/{2**(min_e)}-{2**(max_e-1)}/memory_fox_{numtype}_{2**(min_e)}-{2**(max_e-1)}.png')

def main():
    # graphs(6, 9, isInt=True)
    # graphs(6, 9, isInt=False)
    # graphs(9, 12, isInt=True)
    # graphs(9, 12, isInt=False)
    graphs(12, 13, isInt=True)
    graphs(12, 13, isInt=False)
    
if __name__ == '__main__':
    main()
