import pulp

# Задача минимизации затрат
prob = pulp.LpProblem("Server_Optimization", pulp.LpMinimize)

x = pulp.LpVariable('x', lowBound=0, cat='Integer')  # серверы X
y = pulp.LpVariable('y', lowBound=0, cat='Integer')  # серверы Y

# Целевая функция
prob += 60*x + 45*y, "Total_Cost"

# Ограничения
prob += 1200*x + 900*y >= 15000, "Requests"
prob += 3*x + 2*y <= 25, "Power"
prob += x >= 0, "Nonnegativity_x"
prob += y >= 0, "Nonnegativity_y"

# Решение
prob.solve()
print("Статус:", pulp.LpStatus[prob.status])
if prob.status == 1:
    print(f"Оптимальное решение: x={x.varValue}, y={y.varValue}")
    print(f"Минимальные затраты: {pulp.value(prob.objective)} руб.")
else:
    print("Допустимое решение отсутствует.")