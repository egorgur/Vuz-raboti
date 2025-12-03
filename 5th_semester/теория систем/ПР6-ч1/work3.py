import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("ЗАДАЧА 3: Оптимизация процесса тестирования ПО")
print("=" * 70)

# ============================================================================
# 1. ПОСТАНОВКА ЗАДАЧИ
# ============================================================================
print("\n" + "=" * 70)
print("1. УСЛОВИЯ ЗАДАЧИ")
print("=" * 70)

print("""
Модульные тесты:
• Производительность: 60 тест-кейсов/час
• Покрытие: 75%
• Минимум: 800 тест-кейсов

Интеграционные тесты:
• Производительность: 35 тест-кейсов/час  
• Покрытие: 85%
• Минимум: 400 тест-кейсов

Общие ограничения:
• Доступное время: 50 часов
""")

# ============================================================================
# 2. МАТЕМАТИЧЕСКАЯ МОДЕЛЬ
# ============================================================================
print("\n" + "=" * 70)
print("2. МАТЕМАТИЧЕСКАЯ МОДЕЛЬ")
print("=" * 70)

print("""
Переменные:
x₁ - часов на модульные тесты
x₂ - часов на интеграционные тесты

Целевая функция (максимизация покрытия):
Z = 0.75 × (60×x₁) + 0.85 × (35×x₂)
Z = 45x₁ + 29.75x₂ → max

Ограничения:
1) x₁ + x₂ ≤ 50        (ограничение по времени)
2) 60x₁ ≥ 800         (минимум модульных тестов)
3) 35x₂ ≥ 400         (минимум интеграционных тестов)
4) x₁ ≥ 0, x₂ ≥ 0     (неотрицательность)

В упрощенном виде:
1) x₁ + x₂ ≤ 50
2) x₁ ≥ 800/60 ≈ 13.333
3) x₂ ≥ 400/35 ≈ 11.429
4) x₁, x₂ ≥ 0
""")

# ============================================================================
# 3. РЕШЕНИЕ С ПОМОЩЬЮ ЛИНЕЙНОГО ПРОГРАММИРОВАНИЯ
# ============================================================================
print("\n" + "=" * 70)
print("3. РЕШЕНИЕ МЕТОДОМ ЛИНЕЙНОГО ПРОГРАММИРОВАНИЯ")
print("=" * 70)

# Целевая функция (для максимизации меняем знак)
c = [-45, -29.75]  # коэффициенты с минусом

# Матрица ограничений неравенств (A_ub * x <= b_ub)
A_ub = [
    [1, 1],      # x₁ + x₂ ≤ 50
    [-60, 0],    # -60x₁ ≤ -800 (эквивалентно 60x₁ ≥ 800)
    [0, -35]     # -35x₂ ≤ -400 (эквивалентно 35x₂ ≥ 400)
]
b_ub = [50, -800, -400]

# Решаем задачу
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None), (0, None)], method='highs')

if result.success:
    x1_opt, x2_opt = result.x
    max_coverage = -result.fun  # меняем знак обратно
    
    print(f"✓ Оптимальное решение найдено!")
    print(f"\nОПТИМАЛЬНЫЕ ЗНАЧЕНИЯ:")
    print(f"• Часы на модульные тесты (x₁): {x1_opt:.3f} ч")
    print(f"• Часы на интеграционные тесты (x₂): {x2_opt:.3f} ч")
    print(f"• Максимальное покрытие: {max_coverage:.2f} усл. ед.")
    
    # Детальный расчет
    print(f"\nДЕТАЛЬНЫЙ РАСЧЕТ:")
    print(f"Модульные тесты: {60*x1_opt:.0f} тестов × 75% = {0.75*60*x1_opt:.2f} ед.")
    print(f"Интеграционные тесты: {35*x2_opt:.0f} тестов × 85% = {0.85*35*x2_opt:.2f} ед.")
    
    # Проверка ограничений
    print(f"\nПРОВЕРКА ОГРАНИЧЕНИЙ:")
    print(f"1. Время: {x1_opt + x2_opt:.2f} ч ≤ 50 ч ✓")
    print(f"2. Модульные: {60*x1_opt:.0f} ≥ 800 ✓")
    print(f"3. Интеграционные: {35*x2_opt:.0f} ≥ 400 ✓")
else:
    print("✗ Решение не найдено!")
    exit()

# ============================================================================
# 4. АНАЛИЗ ВЕРШИН ОБЛАСТИ ДОПУСТИМЫХ РЕШЕНИЙ
# ============================================================================
print("\n" + "=" * 70)
print("4. АНАЛИЗ ВЕРШИН ОБЛАСТИ ДОПУСТИМЫХ РЕШЕНИЙ")
print("=" * 70)

# Точные значения вершин
x1_min = 800/60  # 13.333...
x2_min = 400/35  # 11.4286...

# Вершины области допустимых решений
vertices = [
    (x1_min, x2_min),                 # A: пересечение x₁=min и x₂=min
    (x1_min, 50 - x1_min),           # B: x₁=min и x₁+x₂=50
    (50 - x2_min, x2_min)            # C: x₂=min и x₁+x₂=50
]

print("\nВершины области допустимых решений:")
for i, (x1, x2) in enumerate(vertices):
    Z = 45*x1 + 29.75*x2
    print(f"\nВершина {chr(65+i)}:")
    print(f"  x₁ = {x1:.3f} ч, x₂ = {x2:.3f} ч")
    print(f"  Z = 45×{x1:.3f} + 29.75×{x2:.3f} = {Z:.2f}")
    print(f"  Модульные: {60*x1:.0f} тестов")
    print(f"  Интеграционные: {35*x2:.0f} тестов")

# Определяем оптимальную вершину
optimal_idx = np.argmax([45*v[0] + 29.75*v[1] for v in vertices])
optimal_vertex = vertices[optimal_idx]
print(f"\n✓ Оптимальная вершина: {chr(65+optimal_idx)}")

# ============================================================================
# 5. ГРАФИЧЕСКОЕ РЕШЕНИЕ
# ============================================================================
print("\n" + "=" * 70)
print("5. ГРАФИЧЕСКОЕ РЕШЕНИЕ")
print("=" * 70)

print("Строим график области допустимых решений...")

# Создаем фигуру с двумя подграфиками
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# ==================== ЛЕВЫЙ ГРАФИК: ОБЛАСТЬ ДОПУСТИМЫХ РЕШЕНИЙ ====================
ax1.set_title('ОБЛАСТЬ ДОПУСТИМЫХ РЕШЕНИЙ', fontsize=14, fontweight='bold', pad=20)
ax1.set_xlabel('Часы на модульные тесты, x₁', fontsize=12)
ax1.set_ylabel('Часы на интеграционные тесты, x₂', fontsize=12)
ax1.grid(True, alpha=0.3)

# Создаем сетку для построения
x1_vals = np.linspace(0, 55, 500)

# 1. Ограничение по времени: x₁ + x₂ ≤ 50
x2_time = 50 - x1_vals
ax1.plot(x1_vals, x2_time, 'b-', linewidth=2.5, label='x₁ + x₂ ≤ 50')
ax1.fill_between(x1_vals, 0, x2_time, alpha=0.1, color='blue')

# 2. Минимум модульных тестов: x₁ ≥ 13.333
ax1.axvline(x=x1_min, color='r', linestyle='--', linewidth=2.5, label='x₁ ≥ 13.333')
ax1.fill_betweenx([0, 55], x1_min, 55, alpha=0.1, color='red')

# 3. Минимум интеграционных тестов: x₂ ≥ 11.429
ax1.axhline(y=x2_min, color='g', linestyle='--', linewidth=2.5, label='x₂ ≥ 11.429')
ax1.fill_between(x1_vals, x2_min, 55, alpha=0.1, color='green')

# Область допустимых решений (пересечение всех ограничений)
x1_feasible = np.linspace(x1_min, 50 - x2_min, 100)
x2_lower = np.full_like(x1_feasible, x2_min)
x2_upper = 50 - x1_feasible
ax1.fill_between(x1_feasible, x2_lower, x2_upper, color='yellow', alpha=0.4, 
                label='Область допустимых решений')

# Отмечаем вершины
colors = ['red', 'blue', 'green']
for i, (x1, x2) in enumerate(vertices):
    ax1.plot(x1, x2, 'o', markersize=12, color=colors[i], 
            markeredgecolor='black', markeredgewidth=2, zorder=5)
    ax1.annotate(f'{chr(65+i)}\n({x1:.1f}, {x2:.1f})', 
                (x1, x2), 
                xytext=(10, 10), 
                textcoords='offset points',
                fontsize=11,
                fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))

# Отмечаем оптимальное решение
ax1.plot(x1_opt, x2_opt, 's', markersize=14, color='gold', 
        markeredgecolor='black', markeredgewidth=2, zorder=10,
        label=f'Оптимальное решение\n({x1_opt:.2f}, {x2_opt:.2f})')

# Линии уровня целевой функции (изолинии)
x1_grid, x2_grid = np.meshgrid(np.linspace(0, 55, 200), np.linspace(0, 55, 200))
Z_grid = 45*x1_grid + 29.75*x2_grid

# Рисуем изолинии
levels = [800, 1200, 1600, 2000, 2076, 2200]
CS = ax1.contour(x1_grid, x2_grid, Z_grid, levels=levels, colors='purple', 
                alpha=0.7, linestyles='dotted', linewidths=1.5)
ax1.clabel(CS, inline=1, fontsize=9, fmt='Z=%1.0f')

# Настройка графика
ax1.set_xlim(0, 55)
ax1.set_ylim(0, 55)
ax1.set_aspect('equal', adjustable='box')
ax1.legend(loc='upper right', fontsize=10)
ax1.set_xticks(np.arange(0, 56, 5))
ax1.set_yticks(np.arange(0, 56, 5))

# ==================== ПРАВЫЙ ГРАФИК: АНАЛИЗ РЕШЕНИЯ ====================
ax2.set_title('АНАЛИЗ ОПТИМАЛЬНОГО РЕШЕНИЯ', fontsize=14, fontweight='bold', pad=20)

# Создаем таблицу с результатами
results_text = f"""
ОПТИМАЛЬНОЕ РЕШЕНИЕ:

Время распределения:
• Модульные тесты: {x1_opt:.3f} ч
• Интеграционные тесты: {x2_opt:.3f} ч
• Всего времени: {x1_opt + x2_opt:.2f} ч / 50 ч

Выполнено тестов:
• Модульные: {60*x1_opt:.0f} тестов
• Интеграционные: {35*x2_opt:.0f} тестов

Покрытие тестами:
• От модульных: {0.75*60*x1_opt:.2f} ед.
• От интеграционных: {0.85*35*x2_opt:.2f} ед.
• ОБЩЕЕ ПОКРЫТИЕ: {max_coverage:.2f} ед.

Анализ вершин:
"""
for i, (x1, x2) in enumerate(vertices):
    Z = 45*x1 + 29.75*x2
    marker = "✓" if i == optimal_idx else " "
    results_text += f"\n{marker} Вершина {chr(65+i)}: Z = {Z:.0f}"

ax2.text(0.1, 0.95, results_text, fontsize=11, fontfamily='monospace',
        verticalalignment='top', transform=ax2.transAxes,
        bbox=dict(boxstyle="round,pad=1", facecolor='lightyellow', alpha=0.9))

# График сравнения покрытия (ИСПРАВЛЕНО: используем числовые индексы вместо букв)
ax2_sub = ax2.inset_axes([0.1, 0.1, 0.8, 0.4])
indices = [0, 1, 2]  # Используем числовые индексы вместо букв
vertices_Z = [45*v[0] + 29.75*v[1] for v in vertices]
bars = ax2_sub.bar(indices, vertices_Z, color=['red', 'blue', 'green'], alpha=0.7)
bars[optimal_idx].set_edgecolor('black')
bars[optimal_idx].set_linewidth(2)

# Устанавливаем подписи для столбцов
ax2_sub.set_xticks(indices)
ax2_sub.set_xticklabels(['A', 'B', 'C'])

ax2_sub.axhline(y=max_coverage, color='gold', linestyle='--', linewidth=2, 
               label=f'Максимум: {max_coverage:.0f}')
ax2_sub.set_title('Значение целевой функции в вершинах', fontsize=11)
ax2_sub.set_ylabel('Покрытие Z', fontsize=10)
ax2_sub.legend()
ax2_sub.grid(True, alpha=0.3)

# Скрываем оси основного правого графика
ax2.set_xticks([])
ax2.set_yticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)

plt.suptitle('ГРАФИЧЕСКОЕ РЕШЕНИЕ ЗАДАЧИ ОПТИМИЗАЦИИ ТЕСТИРОВАНИЯ ПО', 
            fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

# ============================================================================
# 6. ИТОГОВЫЙ ВЫВОД
# ============================================================================
print("\n" + "=" * 70)
print("ИТОГОВОЕ РЕШЕНИЕ")
print("=" * 70)

print(f"""
Для достижения максимального покрытия тестами необходимо распределить 
время следующим образом:

▓▓▓ МОДУЛЬНЫЕ ТЕСТЫ: {x1_opt:.1f} часов ▓▓▓
• Выполнено тестов: {60*x1_opt:.0f}
• Покрытие: {0.75*60*x1_opt:.1f} условных единиц

▓▓▓ ИНТЕГРАЦИОННЫЕ ТЕСТЫ: {x2_opt:.1f} часов ▓▓▓
• Выполнено тестов: {35*x2_opt:.0f}
• Покрытие: {0.85*35*x2_opt:.1f} условных единиц

══════════════════════════════════════════════════════════════
▓ МАКСИМАЛЬНОЕ ПОКРЫТИЕ: {max_coverage:.2f} условных единиц ▓
══════════════════════════════════════════════════════════════

Примечания:
• Использовано {x1_opt + x2_opt:.1f} часов из 50 доступных
• Все минимальные требования выполнены
• Решение соответствует вершине C области допустимых решений
""")

# ============================================================================
# 7. ДОПОЛНИТЕЛЬНАЯ ВИЗУАЛИЗАЦИЯ: 3D ГРАФИК
# ============================================================================
print("\n" + "=" * 70)
print("ДОПОЛНИТЕЛЬНАЯ 3D ВИЗУАЛИЗАЦИЯ")
print("=" * 70)

try:
    from mpl_toolkits.mplot3d import Axes3D
    
    fig_3d = plt.figure(figsize=(14, 8))
    ax_3d = fig_3d.add_subplot(111, projection='3d')
    
    # Создаем сетку для x1 и x2
    X1 = np.linspace(x1_min, 50 - x2_min, 50)
    X2 = np.linspace(x2_min, 50 - x1_min, 50)
    X1_grid, X2_grid = np.meshgrid(X1, X2)
    
    # Вычисляем Z только в допустимой области
    Z_grid_3d = 45*X1_grid + 29.75*X2_grid
    # Маска для допустимой области
    mask = (X1_grid + X2_grid <= 50) & (X1_grid >= x1_min) & (X2_grid >= x2_min)
    Z_grid_3d = np.where(mask, Z_grid_3d, np.nan)
    
    # Поверхность целевой функции
    surf = ax_3d.plot_surface(X1_grid, X2_grid, Z_grid_3d, cmap='viridis', 
                             alpha=0.8, edgecolor='none')
    
    # Отмечаем вершины
    for i, (x1, x2) in enumerate(vertices):
        Z = 45*x1 + 29.75*x2
        ax_3d.scatter(x1, x2, Z, color=colors[i], s=100, 
                     edgecolor='black', linewidth=2, zorder=5)
        ax_3d.text(x1, x2, Z, f' {chr(65+i)}\nZ={Z:.0f}', 
                  fontsize=10, fontweight='bold')
    
    # Отмечаем оптимальное решение
    ax_3d.scatter(x1_opt, x2_opt, max_coverage, color='gold', s=150, 
                 marker='*', edgecolor='black', linewidth=2, zorder=10,
                 label=f'Оптимум: Z={max_coverage:.0f}')
    
    ax_3d.set_xlabel('Модульные тесты (x₁), ч', fontsize=11)
    ax_3d.set_ylabel('Интеграционные тесты (x₂), ч', fontsize=11)
    ax_3d.set_zlabel('Покрытие Z', fontsize=11)
    ax_3d.set_title('3D ВИЗУАЛИЗАЦИЯ ЦЕЛЕВОЙ ФУНКЦИИ', fontsize=14, fontweight='bold')
    ax_3d.legend()
    
    fig_3d.colorbar(surf, ax=ax_3d, shrink=0.5, aspect=5, label='Покрытие Z')
    plt.tight_layout()
    plt.show()
    
    print("✓ 3D визуализация построена успешно!")
    
except ImportError:
    print("Для 3D визуализации требуется mpl_toolkits.mplot3d")
    print("Установите: pip install matplotlib")

print("\n" + "=" * 70)
print("ГРАФИЧЕСКОЕ РЕШЕНИЕ ЗАВЕРШЕНО!")
print("=" * 70)