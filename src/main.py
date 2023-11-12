import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from sys import argv

def run_mpi_file(mpi_file_path, exponent, isInt=True):
    result = subprocess.run(['mpiexec', '-n', f'{argv[1]}', 'python', mpi_file_path, f'{exponent}', f'{isInt}'], stdout=subprocess.PIPE, text=True)
    #return result.stdout.decode('utf-8')
    return result.stdout.splitlines()

def run_sec_file(sec_file_path, exponent, isInt=True):
    result = subprocess.run(['python', sec_file_path, f'{exponent}', f'{isInt}'], stdout=subprocess.PIPE, text=True)  
    #return result.stdout.decode('utf-8')  
    return result.stdout.splitlines()

def data(min_e, max_e, isInt=True):
    times_MPI  = {}
    times_SEC  = {}
    memory_MPI = {}
    memory_SEC = {}
    iterations = 1
    np.random.seed(69)  # set the seed for the random numbers generator
                        # so that the same numbers are generated in each process
    for exponent in range(min_e, max_e):
        times_MPI [exponent] = np.zeros(iterations)
        times_SEC [exponent] = np.zeros(iterations)
        memory_MPI[exponent] = np.zeros(iterations)
        memory_SEC[exponent] = np.zeros(iterations)
        print(f'Calculating for {2**exponent}...')
        for i in range(iterations):
            times_SEC[exponent][i], memory_MPI[exponent][i] = run_sec_file('src/fox_SEC.py', exponent, isInt=isInt)
            times_MPI[exponent][i], memory_SEC[exponent][i] = run_mpi_file('src/fox_MPI.py', exponent, isInt=isInt)
    
    return times_MPI, times_SEC, memory_MPI, memory_SEC

def create_dir(path, e_range, numtype):
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(f'{path}/{e_range}'):
        os.makedirs(f'{path}/{e_range}')
    return f'{path}/{e_range}/fox_{numtype}_{e_range}.png'

def graphs(min_e, max_e, isInt=True):

    times_MPI, times_SEC, memory_MPI, memory_SEC = data(min_e, max_e, isInt=isInt)

    y_Time_MPI   = [np.mean(times_MPI [exponent]) for exponent in times_MPI ]
    y_Time_SEC   = [np.mean(times_SEC [exponent]) for exponent in times_SEC ]
    y_Memory_MPI = [np.mean(memory_MPI[exponent]) for exponent in memory_MPI]
    y_Memory_SEC = [np.mean(memory_SEC[exponent]) for exponent in memory_SEC]
    
    bar_w = 0.35
    x_Time_MPI   = np.array([exponent - bar_w/2 for exponent in times_MPI ])
    x_Time_SEC   = np.array([exponent + bar_w/2 for exponent in times_SEC ])
    x_Memory_MPI = np.array([exponent - bar_w/2 for exponent in memory_MPI])
    x_Memory_SEC = np.array([exponent + bar_w/2 for exponent in memory_SEC])

    x_Labels = [str(2**exponent) for exponent in times_MPI]
    num_type = 'enteros' if isInt else 'reales'

    fig, (Time_ax, Memory_ax) = plt.subplots(1, 2, figsize=(20, 5))
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.5, hspace=0.5)
    fig.suptitle(f'Comparación de las ejecuciones del algoritmo Fox con matrices de números {num_type}.')
    
    Time_ax.set_title ('Gráfica comparativa de los tiempos de ejecución entre ejecuciones\nsecuenciales y paralelas.')
    Time_ax.set_xlabel('Orden de la Matriz')
    Time_ax.set_ylabel('Tiempo de ejecución (s)')
    Time_ax.set_xticks(x_Time_MPI + bar_w/2, x_Labels)
    Time_ax.set_yticks([]) 

    bars_Time_MPI = Time_ax.bar(x_Time_MPI, 
                                y_Time_MPI, 
                                bar_w, 
                                label='MPI',        
                                color='#EA75FA'
                                )
    bars_Time_SEC = Time_ax.bar(x_Time_SEC, 
                                y_Time_SEC, 
                                bar_w, 
                                label='Secuencial', 
                                color='#4590FA'
                                )
    
    for bar in bars_Time_SEC + bars_Time_MPI :
        x_pos   = bar.get_x() + bar.get_width()/2.0
        y_value = bar.get_height()
        Time_ax.text(
            x_pos, 
            y_value, 
            f'{y_value:5.5}s', 
            va='bottom', 
            ha='center'
        )
    Time_ax.legend()

    Memory_ax.set_title(f'Grafica comparativa de la memoria (RAM) utilizada entre ejecuciones\nsecuenciales y paralelas.')
    Memory_ax.set_xlabel('Orden de la Matriz')
    Memory_ax.set_ylabel('Memoria utilizada (MB)')
    Memory_ax.set_xticks(x_Memory_MPI + bar_w/2, x_Labels)
    Memory_ax.set_yticks([])

    bars_Memory_MPI = Memory_ax.bar(x_Memory_MPI,
                                    y_Memory_MPI,
                                    bar_w,
                                    label='MPI',
                                    color='#EA75FA'
                                    )
    bars_Memory_SEC = Memory_ax.bar(x_Memory_SEC,
                                    y_Memory_SEC,
                                    bar_w,
                                    label='Secuencial',
                                    color='#4590FA'
                                    )
    
    for bar in bars_Memory_SEC + bars_Memory_MPI :
        x_pos   = bar.get_x() + bar.get_width()/2.0
        y_value = bar.get_height()
        Memory_ax.text(
            x_pos, 
            y_value, 
            f'{(y_value/1024):5.5}MB', 
            va='bottom', 
            ha='center'
        )
    Memory_ax.legend()
    
    fig.savefig(create_dir('graphs', f'{2**(min_e)}-{2**(max_e-1)}', num_type))

def main():

    #! WARNING: This will take a long time to run. 
    #!          Uncomment the graphs you want to generate.
    #* There are already some graphs generated in the graphs folder.
    print(argv[1])
    graphs( 12,  13, isInt=True)
    # graphs( 6,  9, isInt=False)
    # graphs( 9, 12, isInt=True)
    # graphs( 9, 12, isInt=False)
    # graphs(12, 14, isInt=True)
    # graphs(12, 14, isInt=False)
    
if __name__ == '__main__':
    main()
