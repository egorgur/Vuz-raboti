import numpy as np
import matplotlib.pyplot as plt
from gen import GeneticAlgorithm


class GeneticAlgorithmExperiments:
    """
    Класс для проведения и анализа серии экспериментов с генетическим алгоритмом.
    """

    def __init__(self, objective_func, bounds, bits_per_var):
        """
        Инициализация класса экспериментов.

        Параметры:
        ----------
        objective_func : function
            Целевая функция оптимизации (например, sphere, rastrigin и т.д.).
        bounds : list[tuple[float, float]]
            Границы области поиска [(xmin, xmax), ...].
        bits_per_var : int
            Количество бит для кодирования каждой переменной.
        """
        self.objective_func = objective_func
        self.bounds = bounds
        self.bits_per_var = bits_per_var
        self.results = []

    def run_experiments(self, configs, num_runs=100, verbose=False, target_value=0.3):
        """
        Запускает серию экспериментов с разными конфигурациями ГА.

        Параметры:
        ----------
        configs : list[dict]
            Список словарей, каждый содержит параметры для GA.run().
            Например:
            [
                {"pop_size": 30, "generations": 50, "selection_method": "rank"},
                {"pop_size": 50, "generations": 50, "selection_method": "tournament"}
            ]
        num_runs : int
            Количество повторов для усреднения результата.
        verbose : bool
            Печатать ход выполнения.
        """
        self.results = []

        for i, config in enumerate(configs):
            if verbose:
                print(f"\n=== Эксперимент {i + 1}/{len(configs)} ===")
                print(f"Параметры: {config}")

            best_values = []
            histories = []
            table_results = []

            # Повторяем несколько запусков для усреднения
            for run in range(num_runs):
                if verbose:
                    print(f"  Запуск {run + 1}/{num_runs}...")

                ga = GeneticAlgorithm(
                    self.bounds, self.bits_per_var, self.objective_func
                )

                best_solution, best_value = ga.run(
                    pop_size=config.get("pop_size", 30),
                    num_vars=len(self.bounds),
                    generations=config.get("generations", 50),
                    crossover_rate=config.get("crossover_rate", 0.8),
                    mutation_rate=config.get("mutation_rate", 1 / 64),
                    selection_method=config.get("selection_method", "rank"),
                    crossover_method=config.get("crossover_method", "one_point"),
                    mutation_strength=config.get("mutation_strength", "weak"),
                    elite_size=config.get("elite_size", 1),
                    verbose=False,
                )

                """
                ga = geneticalgorithm(self.objective_func, self.bits_per_var, algorithm_parameters=configs)

                '''
                def __init__(self, function, dimension, variable_type='bool', \
                 variable_boundaries=None,\
                 variable_type_mixed=None, \
                 function_timeout=10,\
                 algorithm_parameters={'max_num_iteration': None,\
                                       'population_size':100,\
                                       'mutation_probability':0.1,\
                                       'elit_ratio': 0.01,\
                                       'crossover_probability': 0.5,\
                                       'parents_portion': 0.3,\
                                       'crossover_type':'uniform',\
                                       'max_iteration_without_improv':None},\
                     convergence_curve=True,\
                         progress_bar=True):
                '''
                """

                best_values.append(best_value)
                histories.append(ga.history)

                limit = 0.003

                if self.objective_func.__name__ == "sombrero":
                    limit = 0.00000003
                elif self.objective_func.__name__ == "rosenbrock":
                    limit = 0.04

                # Считаем запуск успешным, если значение < порога
                if (
                    best_value < target_value + limit
                    and best_value > target_value - limit
                ):
                    first_appropriate = None
                    for num, besty in enumerate(histories[0].get("best")):
                        # print(
                        #    besty,
                        #    target_value,
                        #    target_value + 0.01,
                        #    target_value - 0.01,
                        # )
                        if (
                            besty < target_value + limit
                            and besty > target_value - limit
                        ):
                            if not first_appropriate:
                                first_appropriate = num
                            table_results.append(first_appropriate)
                        else:
                            table_results.append(None)

                print(best_value)

            successful = [i for i in table_results if i is not None]
            reliability = (
                len(successful) / len(table_results) * 100
                if len(table_results) > 0
                else float("inf")
            )
            average_iters = (
                sum(successful) / len(successful) if successful else float("inf")
            )

            print(f"Тип history: {type(histories[0])}")
            print(f"Пример history: {histories[0]}")

            # Средние значения динамики по нескольким запускам
            avg_best = np.mean([h["best"] for h in histories], axis=0)
            avg_mean = np.mean([h["mean"] for h in histories], axis=0)
            avg_worst = np.mean([h["worst"] for h in histories], axis=0)

            # Сохраняем результаты
            self.results.append(
                {
                    "config": config,
                    "best_value_mean": np.mean(best_values),
                    "best_value_std": np.std(best_values),
                    "avg_history": {
                        "best": avg_best,
                        "mean": avg_mean,
                        "worst": avg_worst,
                    },
                    "reliability": reliability,
                    "average_iters": average_iters,
                }
            )

        print("\nВсе эксперименты завершены!")

    def compare_results(self, metric="best", show_plots=True):
        """
        Сравнивает результаты проведённых экспериментов.

        Параметры:
        ----------
        metric : str
            Ключ метрики для сравнения ('best').
        show_plots : bool
            Если True — отображает графики сходимости.
        """

        if not self.results:
            print("Нет результатов для сравнения. Сначала запустите run_experiments().")
            return

        print("\n=== Сравнение результатов ===")
        for i, res in enumerate(self.results):
            print(f"Эксперимент {i + 1}: {res['config']}")
            print(f"  Среднее значение f(x): {res['best_value_mean']}")
            print(f"  Стандартное отклонение: {res['best_value_std']}")

        if show_plots:
            plt.figure(figsize=(10, 6))
            for i, res in enumerate(self.results):
                hist = res["avg_history"]
                plt.plot(
                    hist[metric],
                    label=f"Exp {i + 1}: {res['config']['selection_method']}",
                )

            plt.xlabel("Поколение")
            plt.ylabel("Лучшее значение функции пригодности")
            plt.title(
                f"Сравнение динамики сходимости {metric} значения ГА по нескольким запускам"
            )
            plt.legend()
            plt.grid(True)
            plt.show()

    def get_table_data(self, configs):
        """
        Запускает серию экспериментов с разными конфигурациями ГА.

        Параметры:
        ----------
        configs : list[dict]
            Список словарей, каждый содержит параметры для GA.run().
            Например:
            [
                {"pop_size": 30, "generations": 50, "selection_method": "rank"},
                {"pop_size": 50, "generations": 50, "selection_method": "tournament"}
            ]
        num_runs : int
            Количество повторов для усреднения результата.
        verbose : bool
            Печатать ход выполнения.
        """
        self.results = []

        for i, config in enumerate(configs):
            best_values = []
            histories = []

            ga = GeneticAlgorithm(self.bounds, self.bits_per_var, self.objective_func)

            best_solution, best_value = ga.run(
                pop_size=config.get("pop_size", 40),
                num_vars=len(self.bounds),
                generations=config.get("generations", 200),
                crossover_rate=config.get("crossover_rate", 0.8),
                mutation_rate=config.get("mutation_rate", 0.1),
                selection_method=config.get("selection_method", "rank"),
                crossover_method=config.get("crossover_method", "one_point"),
                mutation_strength=config.get("mutation_strength", "weak"),
                elite_size=config.get("elite_size", 1),
                verbose=False,
            )

            print(best_solution, best_value)

        print("\nВсе эксперименты завершены!")


"""
def objective_function(x, y):
    return (1 - x)**2 + 100 * (y - x**2)**2

bounds = [(-2, 2), (-1, 3)]




#=== Начальная оценка ===

configs = [
    {"pop_size": 30, "generations": 50, "selection_method": "rank"},
    {"pop_size": 30, "generations": 50, "selection_method": "tournament"},
]

gen_alg = GeneticAlgorithmExperiments(objective_function, bounds, 8)
gen_alg.run_experiments(configs)
print('rely:', gen_alg.results[0].get('reliability'))
print('average_iters:', gen_alg.results[0].get('average_iters'))

gen_alg.compare_results(metric="worst")
gen_alg.compare_results(metric="best")
gen_alg.compare_results(metric="mean")
gen_alg.get_table_data(configs)

"""
"""
#=== Сила мутации, но точная для tournament===

configs = [
    {"pop_size": 30,  "selection_method": "rank", "mutation_rate": 0.001, "mutation_strength": "weak"},
    {"pop_size": 30,  "selection_method": "tournament", "mutation_rate": 0.01, "mutation_strength": "weak"},
    {"pop_size": 30,  "selection_method": "tournament", "mutation_rate": 0.125, "mutation_strength": "weak"},
    {"pop_size": 30,  "selection_method": "tournament", "mutation_rate": 0.25, "mutation_strength": "weak"},
]


gen_alg.run_experiments(configs)
gen_alg.compare_results(metric="mean")

#=== Сила мутации, но точная для ranked===

configs = [
    {"pop_size": 30,  "selection_method": "rank", "mutation_rate": 0.001, "mutation_strength": "weak"},
    {"pop_size": 30,  "selection_method": "rank", "mutation_rate": 0.01, "mutation_strength": "weak"},
    {"pop_size": 30,  "selection_method": "rank", "mutation_rate": 0.125, "mutation_strength": "weak"},
    {"pop_size": 30,  "selection_method": "rank", "mutation_rate": 0.25, "mutation_strength": "weak"},
]

gen_alg.run_experiments(configs)
gen_alg.compare_results(metric="mean")

#=== Методы кроссоверов ===

configs = [
    {"pop_size": 10,  "selection_method": "tournament", "crossover_method": "one_point"},
    {"pop_size": 10, "selection_method": "tournament", "crossover_method": "uniform"},
]

gen_alg.run_experiments(configs)
gen_alg.compare_results(metric="mean")

#=== Сила мутации ===

configs = [
    {"pop_size": 10,  "selection_method": "tournament", "mutation_strength": "weak"},
    {"pop_size": 10, "selection_method": "tournament", "mutation_strength": "strong"},
]

gen_alg.run_experiments(configs)
gen_alg.compare_results(metric="mean")

#=== Кол-во элитных особей ===

configs = [
    {"pop_size": 30,  "selection_method": "tournament", "elite_size": 1},
    {"pop_size": 30,  "selection_method": "tournament", "elite_size": 3},
    {"pop_size": 30,  "selection_method": "tournament", "elite_size": 5},
    {"pop_size": 30,  "selection_method": "tournament", "elite_size": 8},
    {"pop_size": 30,  "selection_method": "tournament", "elite_size": 10},
    {"pop_size": 30,  "selection_method": "tournament", "elite_size": 20},

]

gen_alg.run_experiments(configs)
gen_alg.compare_results(metric="mean")


#=== Кол-во бит на генотип особи ===

configs = [
    {"pop_size": 30,  "selection_method": "tournament", "bits_per_var": 8},
    {"pop_size": 30,  "selection_method": "tournament", "bits_per_var": 16},
    {"pop_size": 30,  "selection_method": "tournament", "bits_per_var": 20},

]


gen_alg.run_experiments(configs)
gen_alg.compare_results(metric="mean")
"""

"""
Надежность – процент успешных
запусков (решение найдено) к общему числу запусков алгоритма. Среднее
число итераций – номер итерации, когда найдено решение, усредненный по
успешным прогонам. Алгоритм с наибольшей надежностью всегда считается
лучшим. Среди алгоритмов с одинаковой надежностью – лучший тот, у
которого наименьшее среднее число итераций.
"""
