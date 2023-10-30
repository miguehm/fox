#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#define ARRAY_SIZE 100
#define FIFO_BC "myfifo"

int main() {
    int pidA, pidB, pidC;
    int pares[ARRAY_SIZE], impares[ARRAY_SIZE], sumas[ARRAY_SIZE];
    int fd;
    int i;

    // Crear el pipe
    mkfifo(FIFO_BC, 0777);

    // Crear el proceso A
    pidA = fork();
    if (pidA == 0) {
        for (i = 0; i < ARRAY_SIZE; i++) {
            pares[i] = i * 2; // Almacena el número par en el arreglo de pares
        }
        fd = open(FIFO_BC, 1);
        write(fd, pares, sizeof(pares));
        close(fd);
        exit(0);
    }

    // Crear el proceso B
    pidB = fork();
    if (pidB == 0) {
        for (i = 0; i < ARRAY_SIZE; i++) {
            impares[i] = i * 2 + 1; // Almacena el número impar en el arreglo de impares
        }
        fd = open(FIFO_BC, 1);
        write(fd, impares, sizeof(impares));
        close(fd);
        exit(0);
    }

    // Esperar a que los procesos hijos terminen
    waitpid(pidA, NULL, 0);
    waitpid(pidB, NULL, 0);

    // Crear el proceso C
    pidC = fork();
    if (pidC == 0) {
        int pares_leidos[ARRAY_SIZE], impares_leidos[ARRAY_SIZE];
        fd = open(FIFO_BC, 0);
        read(fd, pares_leidos, sizeof(pares_leidos));
        read(fd, impares_leidos, sizeof(impares_leidos));
        close(fd);

        // Calcular la suma de los arreglos
        for (i = 0; i < ARRAY_SIZE; i++) {
            sumas[i] = pares_leidos[i] + impares_leidos[i];
        }

        // Imprimir las sumas
        for (i = 0; i < ARRAY_SIZE; i++) {
            printf("La suma de %d + %d es: %d\n", pares_leidos[i], impares_leidos[i], sumas[i]);
        }

        exit(0);
    }

    // Eliminar el pipe
    unlink(FIFO_BC);

    return 0;
} 