import sys
import numpy as np

from tqdm import tqdm
from time import perf_counter
from resource import getrusage, RUSAGE_SELF

def fox_SEC(exponent: int, isInt: bool) -> float:

    MATRIX_SIZE = 2**exponent

    if isInt:
        matrix_A    = np.random.randint(1_000, 2_000, (MATRIX_SIZE, MATRIX_SIZE)) 
        matrix_B    = np.random.randint(1_000, 2_000, (MATRIX_SIZE, MATRIX_SIZE)) 
        matrix_C    = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
    else:
        matrix_A    = np.random.uniform(1_000, 2_000, (MATRIX_SIZE, MATRIX_SIZE))
        matrix_B    = np.random.uniform(1_000, 2_000, (MATRIX_SIZE, MATRIX_SIZE))
        matrix_C    = np.zeros((MATRIX_SIZE, MATRIX_SIZE))

    start_time = perf_counter()

    for row_i in tqdm(range(MATRIX_SIZE)): 
        for i in range(MATRIX_SIZE):
            col = (row_i + i) % MATRIX_SIZE
            matrix_C[row_i] += matrix_A[row_i, col] * matrix_B[col] 
        

    print(perf_counter() - start_time)
    print(getrusage(RUSAGE_SELF).ru_maxrss)

if __name__ == '__main__':
    fox_SEC(int(sys.argv[1]), bool(sys.argv[2]))
