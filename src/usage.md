# Usage

In order to run the program you need to execute the following command:

Linux:
```bash
$ python3 src/main.py {n_processes} {n} {m}
```


Windows:
```bash
py src/main.py {n_processes} {n} {m} 
```

Where:
- **`n_processes`** is the number of processes that will be used to execute the algorithm.
- **`n`** is the exponent of the matrix size. The matrix size will be $2^n$.
- **`m`** is an optional parameter that indicates another exponent of the matrix size. The matrix size will be $2^m$.
- The program will execute the algorithm for all the matrix sizes $2^x\ \forall\ x \in [n, m]$.

> :warning: **WARNING:** The program will execute the algorithm for all the matrix sizes $2^x\ \forall\ x \in [n, m]$. For values of $n$ and $m$ greater than 11, the execution time will be very long. For example, for $n=11$ and $m=12$, the execution time will be approximately 1 hour. 

## Example:
```bash
$ python3 src/main.py 4 6 8
```
Generates the following graph:
![Output](graphs/felamar/LAPTOP/64-256_Linux/fox_enteros_64-256.png "Output")
