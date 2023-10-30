import numpy as np

a = np.loadtxt('arrays0.txt', dtype=int)
b = np.loadtxt('arrays1.txt', dtype=int)
c = np.loadtxt('arrays2.txt', dtype=int)

print(repr(a), '\n')
print(repr(b), '\n')
print(repr(c), '\n')

print((a @ b).all() == c.all())