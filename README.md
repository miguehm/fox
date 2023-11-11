# Parallel Programming Algorithm FOX in Python

We highly recommend you read the [theory](https://www.cs.csi.cuny.edu/~gu/teaching/courses/csc76010/slides/Matrix%20Multiplication%20by%20Nur.pdf) about this Algorithm.

## Install dependences

```bash
sudo pip install mpi4py \
sudo pip install numpy
```

> Windows users may need to configure your path, check [Python MPI Setup](https://nyu-cds.github.io/python-mpi/setup/) for more info

## Run code

Linux

```bash
mpiexec -n 4 python fox_algorithm.py
```

> `n` flag is according your cpu cores.

## Measure Time

Windows PowerShell

```bash
Measure-Command {mpiexec -n 4 python fox_algorithm.py}
```

Linux

```bash
time mpiexec -n 4 python fox_algorithm.py
```

## Verify results

```bash
python3 checker.py
```

## Measure memory
```bash
pip install memory-profiler # install library
mpiexec -np 2 python -m mprof run test.py
```
