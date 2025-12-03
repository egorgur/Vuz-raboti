import numpy as np
import matplotlib.pyplot as plt

# Коэффициенты целевой функции: Z = 50000*x1 + 40000*x2
c = [50000, 40000]

# Ограничения:
# x1 + x2 <= 20
# x1 >= 5, x1 <= 15
# x2 >= 8

# Построение области
x1 = np.linspace(0, 20, 400)
x2_line = 20 - x1  # x1 + x2 = 20

# Вершины
A = (5, 8)
B = (5, 15)
C = (12, 8)
D = (15, 5)
E = (15, 8)

# Вычисление Z
vertices = [A, B, C, D, E]
Z_values = [c[0]*v[0] + c[1]*v[1] for v in vertices]
max_Z = max(Z_values)
opt_vertex = vertices[Z_values.index(max_Z)]

print(f"Максимальный доход: {max_Z} руб.")
print(f"Оптимальное распределение: x1={opt_vertex[0]}, x2={opt_vertex[1]}")