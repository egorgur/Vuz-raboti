import matplotlib.pyplot as plt
import numpy as np

# Ограничения
x1 = np.linspace(0, 50, 400)

# Программисты: 3x1 + 5x2 = 150
x2_prog = (150 - 3*x1) / 5

# Тестировщики: 4x1 + 2x2 = 120
x2_test = (120 - 4*x1) / 2

# Бюджет: 20x1 + 30x2 = 800
x2_budget = (800 - 20*x1) / 30

plt.figure(figsize=(10, 8))

# Границы области
plt.fill_between(x1, 0, np.minimum(np.minimum(x2_prog, x2_test), x2_budget), 
                 alpha=0.3, label='Допустимая область')

# Линии ограничений
plt.plot(x1, x2_prog, 'r-', label='Программисты')
plt.plot(x1, x2_test, 'g-', label='Тестировщики') 
plt.plot(x1, x2_budget, 'b-', label='Бюджет')

# Оси
plt.axhline(0, color='k', linewidth=0.5)
plt.axvline(0, color='k', linewidth=0.5)

# Оптимальная точка
plt.plot(25, 10, 'ro', markersize=10, label='Оптимум (25,10)')

plt.xlim(0, 35)
plt.ylim(0, 30)
plt.xlabel('x₁ (Мобильное приложение)')
plt.ylabel('x₂ (Веб-сервис)')
plt.title('Графическое решение задачи')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
