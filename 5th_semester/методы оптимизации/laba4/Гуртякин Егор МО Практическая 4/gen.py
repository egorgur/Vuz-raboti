import random
import numpy as np


class GeneticAlgorithm:
    def __init__(self, bounds, bits_per_var, objective_func):
        """
        bounds : list[tuple[float, float]]
            Границы области поиска для каждой переменной [(xmin, xmax), ...]
        bits_per_var : int
            Количество бит для кодирования каждой переменной.
        objective_func : function
            Целевая функция (например, sphere, rastrigin и т.д.)
        """
        self.bounds = bounds
        self.bits_per_var = bits_per_var
        self.objective_func = objective_func

    def initialize_population(self, pop_size, num_vars):
        """
        Инициализация начальной популяции для генетического алгоритма.

        Параметры:
        ----------
        pop_size : int
            Размер популяции (количество особей).
        num_vars : int
            Количество оптимизируемых переменных.

        Возвращает:
        -----------
        population : list[list[int]]
            Список бинарных хромосом (каждая — список бит 0/1).
        """
        population = []
        for _ in range(pop_size):
            chromosome = [
                random.randint(0, 1) for _ in range(num_vars * self.bits_per_var)
            ]
            population.append(chromosome)

        return population

    def decode(self, chromosome):
        """
        Декодирует бинарную хромосому в вещественные переменные.

        chromosome : list[int] — список бит (0/1)
        """
        num_vars = len(self.bounds)
        decoded = []

        for i in range(num_vars):
            # выделяем подстроку для конкретной переменной
            start = i * self.bits_per_var
            end = start + self.bits_per_var
            bits = chromosome[start:end]

            # бинарное → целое
            int_value = int("".join(map(str, bits)), 2)

            # масштабирование в диапазон [xmin, xmax]
            xmin, xmax = self.bounds[i]
            real_value = xmin + (xmax - xmin) * int_value / (2**self.bits_per_var - 1)
            decoded.append(real_value)

        return decoded

    def evaluate(self, population):
        """
        Оценка приспособленности всей популяции.

        population : list[list[int]]
            Список бинарных хромосом (каждая — список 0/1)

        Возвращает:
        ------------
        np.ndarray
            Массив значений функции (fitness) для каждой особи.
            Если задача минимизации, то меньшее значение — лучше.
        """
        fitness_values = []

        for chromosome in population:
            # 1. Декодируем хромосому (генотип → фенотип)
            phenotype = self.decode(chromosome)

            # 2. Вычисляем значение целевой функции
            fitness = self.objective_func(*phenotype)

            fitness_values.append(fitness)

        return np.array(fitness_values)

    def selection(self, population, fitness, method="tournament", tournament_size=3):
        """
        Выполняет селекцию (отбор родителей) в соответствии с выбранным методом.

        Параметры
        ----------
        population : list[list[int]]
            Список бинарных хромосом (текущая популяция).
        fitness : np.ndarray
            Массив пригодностей (меньше — лучше, если задача минимизации).
        method : str
            'rank' — ранговая селекция, 'tournament' — турнирная.
        tournament_size : int
            Размер турнира (t ≥ 2).

        Возвращает
        ----------
        parents : list[list[int]]
            Новое поколение родителей (список хромосом).
        """
        n = len(population)
        parents = []

        # ---------- РАНГОВАЯ СЕЛЕКЦИЯ ----------
        # на основании пригодности: больше пригодность - выше ранг
        # ранг / сумма_рангов - вероятность выбора особи с данным рангом
        # мы как раз и выбираем по этим критериям
        if method == "rank":
            sorted_idx = np.argsort(fitness)
            ranked_population = [population[i] for i in sorted_idx]
            ranks = np.arange(n, 0, -1)
            probs = 2 * ranks / (n * (n + 1))
            for _ in range(n):
                selected_idx = np.random.choice(
                    n, p=probs
                )  # <-- индекс по ranked_population
                parents.append(ranked_population[selected_idx])

        # ---------- ТУРНИРНАЯ СЕЛЕКЦИЯ ----------
        # несколько групп в составе tournament_size выдают самого пригодного
        # самые пригодные становятся родителями

        elif method == "tournament":
            for _ in range(n):
                # выбираем случайных участников турнира (их индексы)
                contenders_idx = np.random.choice(
                    n, size=tournament_size, replace=False
                )

                contenders = [population[i] for i in contenders_idx]
                contenders_fitness = fitness[contenders_idx]

                # выбираем победителя — с наименьшим fitness
                winner = contenders[
                    np.argmin(contenders_fitness)
                ]  # np.argmin() возвращает мин. индекс, но по логике элемента с минимальным fitness
                parents.append(winner)

        elif method == "proportional":
            # Кол-во особей
            r = len(fitness)

            # Для минимизации: чтобы вероятности были неотрицательными
            C = np.max(fitness) + 1e-10  # добавляем малое число для устойчивости

            # Вычисляем вероятности по формуле
            probs = (-fitness + C) / (r * C - np.sum(fitness))

            # Нормализация (на всякий случай, чтобы сумма = 1)
            probs = probs / np.sum(probs)

            # Отбор родителей по вероятностям
            for _ in range(r):
                selected_idx = np.random.choice(r, p=probs)
                parents.append(population[selected_idx])

        else:
            raise ValueError(
                "Неизвестный метод селекции. Используйте 'rank' или 'tournament'."
            )

        return parents

    def crossover(self, parents, crossover_rate=0.8, method="one_point"):
        """
        Выполняет скрещивание (кроссовер) между родителями.

        Параметры
        ----------
        parents : list[list[int]]
            Список бинарных хромосом (родителей).
        crossover_rate : float
            Вероятность применения кроссовера к паре родителей (0..1).
        method : str
            Тип скрещивания: 'one_point' — одноточечное, 'uniform' — равномерное.

        Возвращает
        ----------
        offspring : list[list[int]]
            Новое поколение потомков.
        """
        offspring = []
        num_parents = len(parents)

        for i in range(0, num_parents, 2):
            parent1 = parents[i].copy()
            parent2 = parents[(i + 1) % num_parents].copy()

            # случайное применение кроссовера
            if random.random() < crossover_rate:
                if method == "one_point":
                    # Одноточечный кроссовер
                    point = random.randint(1, len(parent1) - 1)
                    child1 = parent1[:point].copy() + parent2[point:].copy()
                    child2 = parent2[:point].copy() + parent1[point:].copy()

                elif method == "uniform":
                    # Равномерный кроссовер (каждый бит выбирается с вероятностью 0.5)
                    child1 = []
                    child2 = []
                    for b1, b2 in zip(parent1, parent2):
                        if random.random() < 0.5:
                            child1.append(b1)
                            child2.append(b2)
                        else:
                            child1.append(b2)
                            child2.append(b1)
                elif method == "two_point":
                    point1 = random.randint(1, len(parent1) - 2)
                    point2 = random.randint(point1 + 1, len(parent1) - 1)
                    child1 = (
                        parent1[:point1] + parent2[point1:point2] + parent1[point2:]
                    )
                    child2 = (
                        parent2[:point1] + parent1[point1:point2] + parent2[point2:]
                    )
                else:
                    raise ValueError(
                        "Неизвестный тип кроссовера: используйте 'one_point' или 'uniform'."
                    )
            else:
                # Без кроссовера — потомки идентичны родителям
                child1, child2 = parent1.copy(), parent2.copy()

            offspring.extend([child1, child2])

        return offspring

    def mutate(self, population, mutation_rate=1 / 64, mutation_strength="weak"):
        """
        Мутация хромосом популяции.

        Параметры
        ----------
        population : list[list[int]]
            Список бинарных хромосом.
        mutation_rate : float
            Вероятность мутации гена (0..1).
        mutation_strength : str
            'weak' — слабая мутация (низкая вероятность);
            'strong' — сильная мутация (высокая вероятность).

        Возвращает
        ----------
        mutated_population : list[list[int]]
            Популяция после мутации.
        """
        mutated_population = []

        # Настраиваем вероятность мутации в зависимости от силы
        if mutation_strength == "weak":
            rate = mutation_rate
        elif mutation_strength == "strong":
            rate = mutation_rate * 5
        else:
            raise ValueError("mutation_strength должно быть 'weak' или 'strong'.")

        for chromosome in population:
            mutated = []
            for gene in chromosome:
                if random.random() < rate:
                    mutated.append(1 - gene)  # инвертируем бит
                else:
                    mutated.append(gene)
            mutated_population.append(mutated)

        return mutated_population

    def form_new_population(self, population, offspring, fitness, elite_size=1):
        """
        Формирует новое поколение популяции с учётом элитизма.

        Параметры
        ----------
        parents : list[list[int]]
            Родители (до скрещивания).
        offspring : list[list[int]]
            Потомки после crossover и mutation.
        fitness : np.ndarray
            Значения пригодности текущей популяции.
        elite_size : int
            Количество лучших особей, которые переходят в следующее поколение без изменений.

        Возвращает
        ----------
        new_population : list[list[int]]
            Новое поколение популяции.
        """
        new_population = []

        # --- 1. Элитизм: сохраняем лучших особей ---
        elite_indices = np.argsort(fitness)[:elite_size]  # для задачи минимизации
        elites = [population[i] for i in elite_indices]
        new_population.extend(elites)

        # --- 2. Остальных добираем из потомков ---
        remaining = len(population) - elite_size
        offspring = random.sample(offspring, len(offspring))
        new_population.extend(offspring[:remaining])

        return new_population

    def run(
        self,
        pop_size,
        num_vars,
        generations,
        crossover_rate=0.8,
        mutation_rate=1 / 64,
        selection_method="proportional",
        crossover_method="one_point",
        mutation_strength="weak",
        elite_size=1,
        verbose=True,
    ):
        """
        Основной цикл генетического алгоритма.

        Параметры
        ----------
        pop_size : int
            Размер популяции.
        num_vars : int
            Количество переменных.
        bits_per_var : int
            Количество бит для кодирования каждой переменной.
        bounds : list[tuple[float, float]]
            Границы поиска для каждой переменной.
        generations : int
            Количество поколений.
        crossover_rate : float
            Вероятность скрещивания (0–1).
        mutation_rate : float
            Вероятность мутации каждого бита (0–1).
        selection_method : str
            'tournament' или 'rank'.
        crossover_method : str
            'one_point' или 'uniform'.
        mutation_strength : str
            'weak' или 'strong'.
        elite_size : int
            Количество элитных особей, переходящих без изменений.
        verbose : bool
            Печать статистики по поколениям.
        """

        # --- 1. Инициализация популяции ---
        population = self.initialize_population(pop_size, num_vars)

        # Для хранения статистики
        best_fitness_history = []
        mean_fitness_history = []
        worst_fitness_history = []

        # --- 2. Основной эволюционный цикл ---

        for gen in range(generations):
            # --- 2.1. Оценка текущей популяции ---

            fitness = self.evaluate(population)

            # Сохранение статистики
            best_fitness = np.min(fitness)
            worst_fitness = np.max(fitness)
            mean_fitness = np.mean(fitness)

            best_fitness_history.append(best_fitness)
            worst_fitness_history.append(worst_fitness)
            mean_fitness_history.append(mean_fitness)

            if verbose:
                print(
                    f"Поколение {gen + 1}: min={best_fitness:.6f}, mean={mean_fitness:.6f}, max={worst_fitness:.6f}"
                )

            # --- 2.2. Отбор родителей ---
            parents = self.selection(population, fitness, method=selection_method)
            # print("parents after selection", parents)

            # --- 2.3. Скрещивание ---
            offspring = self.crossover(parents, crossover_rate, method=crossover_method)

            # print("after crossover", offspring)

            # --- 2.4. Мутация ---
            offspring = self.mutate(
                offspring, mutation_rate, mutation_strength=mutation_strength
            )

            # print("after mutation", offspring)

            # --- 2.5. Формирование нового поколения ---
            population = self.form_new_population(
                population, offspring, fitness, elite_size
            )

        # --- 3. Финальная оценка и результат ---
        final_fitness = self.evaluate(population)
        best_idx = np.argmin(final_fitness)
        best_chromosome = population[best_idx]
        best_solution = self.decode(best_chromosome)
        best_value = final_fitness[best_idx]

        # --- 4. Сохраняем статистику ---
        self.history = {
            "best": best_fitness_history,
            "mean": mean_fitness_history,
            "worst": worst_fitness_history,
        }

        if verbose:
            print("\nЛучшее найденное решение:")
            print(f"x = {best_solution}")
            print(f"f(x) = {best_value:.60f}")

        return best_solution, best_value
