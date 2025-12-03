import numpy as np
from scipy.optimize import linprog

# Затраты на перевозку (3 офиса × 3 проекта)
costs = [
    [6, 9, 7],
    [8, 5, 10],
    [7, 6, 8]
]

# Доступно в офисах
supply = [15, 20, 15]
# Требуется для проектов
demand = [18, 12, 20]

# Преобразование в стандартную форму для linprog
c = np.array(costs).flatten()

# Матрица ограничений
A_eq = []
# Ограничения по строкам (офисы)
for i in range(3):
    row = [0]*9
    row[i*3:(i+1)*3] = [1,1,1]
    A_eq.append(row)
# Ограничения по столбцам (проекты)
for j in range(3):
    row = [0]*9
    for i in range(3):
        row[i*3 + j] = 1
    A_eq.append(row)

b_eq = supply + demand

# Границы переменных
bounds = [(0, None)]*9

# Решение
res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
print("Статус:", res.message)
print("Минимальные затраты:", res.fun)
print("Распределение (матрицей 3x3):")
print(res.x.reshape(3,3))