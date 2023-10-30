#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>

#define FIFO_BC "mi_fifo2"

int main() {
    int i;
    pid_t pidA, pidB, pidC;
    int pares[100], impares[100], sumas[100];
    int fd;

    // Crear el cauce FIFO
    mkfifo(FIFO_BC, 0666);

    pidA = fork();
    if (pidA == 0) {
        fd = open(FIFO_BC, 0777);
        for (int i = 0; i < 100; i++) {
            pares[i] = i * 2; // Almacena el número par en el arreglo de pares
            write(fd, &pares[i], sizeof(pares[i]));
        }
        close(fd);
        exit(0);
    }

    pidB = fork();
    if (pidB == 0) {
        sleep(2);
        fd = open(FIFO_BC, 0777);
        for (int i = 0; i < 100; i++) {
            impares[i] = i * 2 + 1; // Almacena el número impar en el arreglo de impares
            write(fd, &impares[i], sizeof(impares[i]));
        }
        close(fd);
        exit(0);
    }

    // Esperar a que los procesos hijos terminen
    waitpid(pidA, NULL, 0);
    waitpid(pidB, NULL, 0);

    pidC = fork();
    if (pidC == 0) {
        fd = open(FIFO_BC, 0777);
        for(i=0;i<100;i++){
            read(fd, &pares[i], sizeof(pares[i]));
        }
        for(i=0;i<100;i++){
            read(fd, &impares[i], sizeof(impares[i]));
            sumas[i]=pares[i]+impares[i];
        }
        close(fd);

        // Imprimir las sumas
        for (i = 0; i < 100; i++) {
            printf("La suma de %d + %d es: %d\n", pares[i], impares[i], sumas[i]);
        }

        exit(0);
    }

    return 0;
}