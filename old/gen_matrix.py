import numpy as np

def generate_matrix():
    A = np.random.randint(1000, 2000, (4,4))
    B = np.random.randint(1000, 2000, (4,4))
    np.savez('matrix.npz', A = A, B = B)

def read_matrix():
    global data
    return data

if __name__ == "__main__":
    global data
    data = np.load('matrix.npz')
    generate_matrix()
