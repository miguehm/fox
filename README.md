# HOW TO RUN

## Install dependences

```bash
sudo pip install mpi4py \
sudo pip install numpy
```

## Run code

```bash
mpiexec -n 4 python fox_algorithm.py
```

> `n` flag is according your cpu cores.

## Verify results

```bash
python3 checker.py
```
