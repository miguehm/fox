# MPI Fox Algorithm
<div align="center">
<img src="media\Fox_Algorithm_ManimCE_v0.18.0_720.gif">
</div>

This is a simple implementation of the Fox algorithm for matrix multiplication using MPI. The algorithm is described in the following paper:
> Dean, N. (2017). Matrix Multiplication. Retrieved from https://www.cs.csi.cuny.edu/~gu/teaching/courses/csc76010/slides/Matrix%20Multiplication%20by%20Nur.pdf

The objective of this project is to show the execution time and RAM usage of the algorithm for different matrix sizes and number of processes. 

The program will run the algorithm for all the matrix sizes $2^x\ \forall\ x \in [n, m]$ five times and will calculate the average execution time and RAM usage. The results will be used to generate a graph that will be saved in the `graphs` folder. The graph will be saved in the following format:

![Graph](graph/../graphs/felamar/LAPTOP/512-2048_Linux/fox_enteros_512-2048.png "Graph")
> **Note:** This format is reserved for Linux users. Windows users will see only the execution time graph.

This project was developed as part of the course "Operatin Systems" at the Benemérita Universidad Autónoma de Puebla.

## Table of Contents

- [MPI Fox Algorithm](#mpi-fox-algorithm)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Example:](#example)
  - [TO DO](#to-do)


## Installation

First, clone the repository:

```bash
git clone https://github.com/miguehm/fox-algorithm.git && cd fox-algorithm
```
or alternatively, download the zip file and extract it:

![Download zip](media\zip_download.png "Download zip")
<!-- [![Download fox-algorithm](https://img.shields.io/github/v/release/miguehm/fox-algorithm?include_prereleases&label=Download&logo=github)] -->

Then, install the dependencies:

```bash
pip install -r requirements.txt
```

You need to have MPI installed. If you are using Windows, you can [download the installer](https://www.microsoft.com/en-us/download/details.aspx?id=57467) from the microsoft official page. If you are using Linux, you don't need to install anything.

## Usage

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

### Example:
```bash
$ python3 src/main.py 4 6 8
```
Generates the following graph:
![Output](graphs/felamar/LAPTOP/64-256_Linux/fox_enteros_64-256.png "Output")

## TO DO
- [ ] Add RAM measurement for Windows.
- [ ] Create CSV files with the results.
- [ ] Add a script to generate the graphs from the CSV files.
