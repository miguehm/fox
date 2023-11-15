# MPI Fox Algorithm
<div align="center">
<img src="media/fox.mp4">
</div>

This is a simple implementation of the Fox algorithm for matrix multiplication using MPI. The algorithm is described in the following paper:
> Dean, N. (2017). Matrix Multiplication. Retrieved from https://www.cs.csi.cuny.edu/~gu/teaching/courses/csc76010/slides/Matrix%20Multiplication%20by%20Nur.pdf

The objective of this project is to show the execution time and RAM usage of the algorithm for different matrix sizes and number of processes. 

The program will run the algorithm for all the matrix sizes $2^x\ \forall\ x \in [n, m]$ five times and will calculate the average execution time and RAM usage. The results will be used to generate a graph that will be saved in the `graphs` folder. The graph will be saved in the following format:

![Graph](graph/../graphs/felamar/LAPTOP/512-2048_Linux/fox_enteros_512-2048.png "Graph")
> **Note:** This format is reserved for Linux users. Windows users will see only the execution time graph.

This project was developed as part of the course "Operating Systems" at the Benemérita Universidad Autónoma de Puebla.

## TO DO
- [ ] Add RAM measurement for Windows.
- [ ] Create CSV files with the results.
- [ ] Add a script to generate the graphs from the CSV files.

