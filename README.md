# Parallel Programming Algorithm FOX in Python

## Install dependences

```bash
sudo pip install mpi4py \
sudo pip install numpy
```

> Windows users may need to configure your path, check [Python MPI Setup](https://nyu-cds.github.io/python-mpi/setup/) for more info

## Run code

```bash
mpiexec -n 4 python fox_algorithm.py
```

> `n` flag is according your cpu cores.

## Verify results

```bash
python3 checker.py
```
