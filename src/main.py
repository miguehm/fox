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

def data(min_e, max_e, isInt=True):
    times_MPI = {}
    times_SEC = {}
    np.random.seed(69)  # set the seed for the random numbers generator
                        # so that the same numbers are generated in each process
    for exponent in range(min_e, max_e):
        times_MPI[exponent] = np.zeros(5)
        times_SEC[exponent] = np.zeros(5)
        print(f'Calculating for {2**exponent}...')
        for i in range(5):
            times_SEC[exponent][i] = run_sec_file('src/fox_SEC.py', exponent, isInt=isInt)
            times_MPI[exponent][i] = run_mpi_file('src/fox_MPI.py', exponent, isInt=isInt)
    
    return times_MPI, times_SEC

def create_dir(path, e_range, numtype):
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(f'{path}/{e_range}'):
        os.makedirs(f'{path}/{e_range}')
    return f'{path}/{e_range}/fox_{numtype}_{e_range}.png'

def graphs(min_e, max_e, isInt=True):

    times_MPI, times_SEC = data(min_e, max_e, isInt=isInt)

    y_MPI = [np.mean(times_MPI[exponent]) for exponent in times_MPI]
    y_SEC = [np.mean(times_SEC[exponent]) for exponent in times_SEC]
    
    bar_w = 0.35
    x_MPI = np.array([exponent - bar_w/2 for exponent in times_MPI])
    x_SEC = np.array([exponent + bar_w/2 for exponent in times_SEC])

    x_labels = [str(2**exponent) for exponent in times_MPI]
    num_type = 'enteros' if isInt else 'reales'

    fig, (T_ax, M_ax) = plt.subplots(1, 2, figsize=(20, 5))
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.5, hspace=0.5)
    
    T_ax.set_title(f'Tiempo de ejecución del algoritmo fox con\nmatrices de números {num_type}.')
    T_ax.set_xlabel('Orden de la Matriz')
    T_ax.set_ylabel('Tiempo de ejecución (s)')
    T_ax.set_xticks(x_MPI + bar_w/2, x_labels)
    T_ax.set_yticks([]) 

    bars_MPI = T_ax.bar(x_MPI, y_MPI, bar_w, label='MPI',        color='#EA75FA')
    bars_SEC = T_ax.bar(x_SEC, y_SEC, bar_w, label='Secuencial', color='#4590FA')
    
    for bar in bars_SEC + bars_MPI:
        x_pos   = bar.get_x() + bar.get_width()/2.0
        y_value = bar.get_height()
        T_ax.text(
            x_pos, 
            y_value, 
            f'{y_value:5.5}s', 
            va='bottom', 
            ha='center'
        )
    
    T_ax.legend()
    
    fig.savefig(create_dir('graphs', f'{2**(min_e)}-{2**(max_e-1)}', num_type))

def main():

    #! WARNING: This will take a long time to run. 
    #!          Uncomment the graphs you want to generate.
    #* There are already some graphs generated in the graphs folder.
    graphs( 6,  7, isInt=True)
    # graphs( 6,  9, isInt=False)
    # graphs( 9, 12, isInt=True)
    # graphs( 9, 12, isInt=False)
    # graphs(12, 14, isInt=True)
    # graphs(12, 14, isInt=False)
    
if __name__ == '__main__':
    main()