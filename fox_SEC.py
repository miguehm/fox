import numpy as np
from time import time
from tqdm.auto import tqdm

def fox_SEC(exponent: int, isInt: bool) -> float:

    MATRIX_SIZE = 2**exponent

    if isInt:
        matrix_A    = np.random.randint(1000, 2000, (MATRIX_SIZE, MATRIX_SIZE)) 
        matrix_B    = np.random.randint(1000, 2000, (MATRIX_SIZE, MATRIX_SIZE)) 
        matrix_C    = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
    else:
        matrix_A    = np.random.uniform(1000, 2000, (MATRIX_SIZE, MATRIX_SIZE))
        matrix_B    = np.random.uniform(1000, 2000, (MATRIX_SIZE, MATRIX_SIZE))
        matrix_C    = np.zeros((MATRIX_SIZE, MATRIX_SIZE))

    start_time = time()

    for row_i in tqdm(range(MATRIX_SIZE)): 

        for i in range(MATRIX_SIZE):
            col = (row_i + i) % MATRIX_SIZE
            matrix_C[row_i] += matrix_A[row_i, col] * matrix_B[col] 

    np.savetxt('arrayA.txt', matrix_A, fmt='%d')
    np.savetxt('arrayB.txt', matrix_B, fmt='%d')
    np.savetxt('result.txt', matrix_C, fmt='%d')
    
    return time() - start_time