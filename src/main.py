import typer   
import os
import platform
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

isLinux = os.name == 'posix'

global nthreads

if isLinux:
    python_path = 'python3'
else:
    python_path = 'python'

def run_mpi_file(mpi_file_path, exponent, isInt=True):
    global nthreads
    result = subprocess.run(['mpiexec', '-n', f'{nthreads}', python_path, mpi_file_path, f'{exponent}', f'{isInt}'], stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()

def run_sec_file(sec_file_path, exponent, isInt=True):
    result = subprocess.run([python_path, sec_file_path, f'{exponent}', f'{isInt}'], stdout=subprocess.PIPE, text=True)  
    return result.stdout.splitlines()

def get_processor_info():
    if platform.system() == "Windows":
        # TODO: check how this works on Windows
        return platform.processor()
    elif platform.system() == "Darwin":
        # TODO: check how this works on Mac
        return os.popen("/usr/sbin/sysctl -n machdep.cpu.brand_string").read().strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo | grep 'model name' | uniq | awk -F: '{print $2}'"
        return os.popen(command).read().strip()
    return ""

def data(min_e, max_e=0, isInt=True):
    times_MPI  = {}
    times_SEC  = {}
    memory_MPI = {}
    memory_SEC = {}
    iterations = 5
    
    np.random.seed(69)  # set the seed for the random numbers generator
                        # so that the same numbers are generated in each process
    for exponent in range(min_e, max_e):
        times_MPI [exponent] = np.zeros(iterations)
        times_SEC [exponent] = np.zeros(iterations)
        memory_MPI[exponent] = np.zeros(iterations)
        memory_SEC[exponent] = np.zeros(iterations)
        print(f'Calculating for {2**exponent}...')
        for i in range(iterations):
            times_MPI[exponent][i], memory_MPI[exponent][i] = run_mpi_file('src/fox_MPI.py', exponent, isInt=isInt)
            times_SEC[exponent][i], memory_SEC[exponent][i] = run_sec_file('src/fox_SEC.py', exponent, isInt=isInt)
    
    return times_MPI, times_SEC, memory_MPI, memory_SEC

def create_dir(path, e_range, numtype):
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(f'{path}/{e_range}'):
        os.makedirs(f'{path}/{e_range}')
    return f'{path}/{e_range}/fox_{numtype}_{e_range}.png'

def graphs(min_e, max_ex=0, isInt=True):

    if int(min_e) > 11 or int(max_ex) > 11: 
        response = input('This will take a long time to run. Are you sure you want to continue? (y/n)\n')
        if response.lower() != 'y': return

    max_e = max_ex + 1 if max_ex != 0 else min_e + 1

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

    if isLinux:
       fig1, Time_ax = plt.subplots(1, 1, figsize=(10, 5))
       fig2, Memory_ax = plt.subplots(1, 1, figsize=(10, 5))
    else:
       fig1, Time_ax = plt.subplots(1, 1, figsize=(10, 5))
        
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.5, hspace=0.5)
    fig1.suptitle(f'Comparación de tiempo\nAlgoritmo Fox VS Secuencial de tipo {num_type}.')

    global nthreads
    
    Time_ax.set_title (f'{get_processor_info()}\nThreads: {nthreads}')
    Time_ax.set_xlabel('Orden de la Matriz')
    Time_ax.set_ylabel('Tiempo de ejecución (s)')
    Time_ax.set_xticks(x_Time_MPI + bar_w/2, x_Labels)
    Time_ax.set_yticks([]) 
    bars_Time_MPI = Time_ax.bar(x_Time_MPI, 
                                y_Time_MPI, 
                                bar_w, 
                                label='MPI',        
                                color='#FA821E')
    bars_Time_SEC = Time_ax.bar(x_Time_SEC, 
                                y_Time_SEC, 
                                bar_w, 
                                label='Secuencial', 
                                color='#FAC01E')
    
    for bar in bars_Time_SEC + bars_Time_MPI :
        x_pos   = bar.get_x() + bar.get_width()/2.0
        y_value = bar.get_height()
        Time_ax.text(
            x_pos, 
            y_value, 
            f'{y_value:5.5}s', 
            va='bottom', 
            ha='center')
    Time_ax.legend()

    plt.tight_layout()
    fig1.savefig(create_dir('graphs', f'{2**(min_e)}-{2**(max_e-1)}', f'{num_type} - time'))

    if isLinux:
        fig2.suptitle(f'Comparación de memoria RAM\nAlgoritmo fox VS Secuencial de tipo {num_type}.')
        Memory_ax.set_title (f'{get_processor_info()}\nThreads: {nthreads}')
        Memory_ax.set_xlabel('Orden de la Matriz')
        Memory_ax.set_ylabel('Memoria utilizada (MB)')
        Memory_ax.set_xticks(x_Memory_MPI + bar_w/2, x_Labels)
        Memory_ax.set_yticks([])
        bars_Memory_MPI = Memory_ax.bar(x_Memory_MPI, 
                                        y_Memory_MPI, 
                                        bar_w, 
                                        label='MPI',
                                        color='#FA821E')
        bars_Memory_SEC = Memory_ax.bar(x_Memory_SEC, 
                                        y_Memory_SEC, 
                                        bar_w, 
                                        label='Secuencial', 
                                        color='#FAC01E')
        
        for bar in bars_Memory_SEC + bars_Memory_MPI :
            x_pos   = bar.get_x() + bar.get_width()/2.0
            y_value = bar.get_height()
            Memory_ax.text(
                x_pos, 
                y_value, 
                f'{(y_value/1024):5.5}MB', 
                va='bottom', 
                ha='center')
        Memory_ax.legend()
        plt.tight_layout()
        fig2.savefig(create_dir('graphs', f'{2**(min_e)}-{2**(max_e-1)}', f'{num_type} - memory'))

    # fig.savefig(create_dir('graphs', f'{2**(min_e)}-{2**(max_e-1)}', num_type))

def main(
    from_order: int = typer.Option(6, help="Exponent of base 2 matrix order (2^)", rich_help_panel="Matrix order range"),
    to_order: int = typer.Option(13, help="Exponent of base 2 matrix order (2^)", rich_help_panel="Matrix order range"),
    threads: int = typer.Option(4, help="Number of cores to use", rich_help_panel="MPI options")
    ):
    
    global nthreads
    nthreads = threads

    if from_order > to_order:
        print('The maximum exponent must be greater than the minimum exponent.')
        return

    print("==== Iniciando multiplicaciones para numeros enteros...")
    graphs(from_order, to_order, isInt=True)
    print("==== Iniciando multiplicaciones para numeros reales...")
    graphs(from_order, to_order, isInt=False)

    #* There are already some graphs generated in the graphs folder.
    # graphs( 6,  9, isInt=True)
    # graphs( 6,  9, isInt=False)
    # graphs( 9, 12, isInt=True)
    # graphs( 9, 12, isInt=False)
    #! WARNING: This will take a long time to run. 
    #!          Uncomment them if you want to run them.
    # graphs(12, 14, isInt=True)
    # graphs(12, 14, isInt=False)
    
if __name__ == '__main__':
    typer.run(main)
