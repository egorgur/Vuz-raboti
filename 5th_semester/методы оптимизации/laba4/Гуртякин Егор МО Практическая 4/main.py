from experiment import GeneticAlgorithmExperiments  # твой класс
from funcs import (
    objective_function,
    rastrigin_2d,
    rosenbrock,
    sombrero,
    function_12,
)
import tkinter as tk
from tkinter import ttk, messagebox
import traceback


# --- Настройки экспериментов ---

functions = {
    "Ф1": {"func": objective_function, "target": 0.0, "boundaries": [(-1, 1), (-1, 1)]},
    "Ф3": {"func": rastrigin_2d, "target": 0.0, "boundaries": [(-16, 16), (-16, 16)]},
    "Ф5": {"func": rosenbrock, "target": 0.0, "boundaries": [(-2, 2), (-2, 2)]},
    "Ф8": {"func": sombrero, "target": 0.0, "boundaries": [(-10, 10), (-10, 10)]},
    "Ф12": {"func": function_12, "target": 0.0, "boundaries": [(0, 4), (0, 4)]},
}

"""
functions = {
    "Ф2": {"func": "rastrigin_rotated", "target": 0.5},
    "Ф4": {"func": "griewank", "target": 1.0},
    "Ф6": {"func": "custom_function", "target": 0.7},
    "Ф7": {"func": "fox_hole", "target": 2.0},
    "Ф15": {"func": "de_jong", "target": 3.0},
}
"""


class ExperimentGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Настройки эксперимента ГА")
        self.geometry("1200x800")
        self.resizable(True, True)

        # Заголовок
        tk.Label(
            self, text="Параметры генетического алгоритма", font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Контейнер формы
        form = tk.Frame(self)
        form.pack(padx=20, pady=10, fill="x")
        

        self.entries = {}

        # --- выбор тестовой функции ---
        self._add_combo(
            form,
            "function",
            "Тестовая функция:",
            values=list(functions.keys()),
            default="Ф1",
        )

        # --- числовые параметры ---
        self._add_entry(form, "pop_size", "Размер популяции:", default="50")
        self._add_entry(form, "generations", "Количество поколений:", default="50")

        # --- выпадающие списки ---
        self._add_combo(
            form,
            "selection_method",
            "Метод селекции:",
            values=["rank", "tournament", "proportional"],
            default="tournament",
        )

        self._add_combo(
            form,
            "crossover_method",
            "Метод кроссовера:",
            values=["one_point", "two_point", "uniform"],
            default="one_point",
        )

        self._add_combo(
            form,
            "mutation_strength",
            "Сила мутации:",
            values=["weak", "strong"],
            default="weak",
        )

        # --- кнопка запуска ---
        ttk.Button(
            self, text="Запустить эксперимент", command=self.run_experiment, 
        ).pack(pady=20, anchor="w")

        ttk.Button(self, text="Построить графики", command=self.create_plot).pack(
            pady=20, anchor="w",
        )

        # --- Таблица результатов ---
        columns = [
            "Тестовая задача",
            "Тип селекции",
            "Надежность",
            "Ср. итерации",
        ]

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", padx=15, pady=15, expand=True)

    # --- Вспомогательные функции ---
    def _add_entry(self, parent, key, label, default=""):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=5)
        tk.Label(row, text=label, width=20, anchor="w").pack(side="left")
        entry = ttk.Entry(row)
        entry.insert(0, default)
        entry.pack(side="right", expand=True, fill="x")
        self.entries[key] = entry

    def _add_combo(self, parent, key, label, values, default=None):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=5)
        tk.Label(row, text=label, width=20, anchor="w").pack(side="left")
        combo = ttk.Combobox(row, values=values, state="readonly")
        if default:
            combo.set(default)
        combo.pack(side="right", expand=True, fill="x")
        self.entries[key] = combo

    def create_plot(self):
        """Здесь подключается твой GeneticAlgorithmExperiments"""
        try:
            # Считываем параметры

            func_name = self.entries["function"].get()

            config = {
                "pop_size": int(self.entries["generations"].get()),
                "num_vars": int(self.entries["pop_size"].get()),
                "mutation_rate": 1 / 64,
                "elit_ratio": 0.01,
                "selection_method": self.entries["selection_method"].get(),
                "crossover_method": self.entries["crossover_method"].get(),
                "mutation_strength": self.entries["mutation_strength"].get(),
                "crossover_probability": 0.5,
                "parents_portion": 0.3,
            }

            ga_exp = GeneticAlgorithmExperiments(
                functions[f"{func_name}"]["func"],
                functions[f"{func_name}"]["boundaries"],
                64,
            )

            target_value = float(functions[f"{func_name}"]["target"])

            ga_exp.run_experiments([config], target_value=target_value)

            ga_exp.compare_results()
            ga_exp.compare_results(metric="mean")
            ga_exp.compare_results(metric="worst")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить эксперимент:\n{e}")
            error_msg = traceback.format_exc()
            print(error_msg)

    def run_experiment(self):
        """Здесь подключается твой GeneticAlgorithmExperiments"""
        try:
            # Считываем параметры

            func_name = self.entries["function"].get()

            config = {
                "pop_size": int(self.entries["generations"].get()),
                "num_vars": int(self.entries["pop_size"].get()),
                "mutation_rate": 1 / 64,
                "elit_ratio": 0.01,
                "selection_method": self.entries["selection_method"].get(),
                "crossover_method": self.entries["crossover_method"].get(),
                "mutation_strength": self.entries["mutation_strength"].get(),
                "crossover_probability": 0.5,
                "parents_portion": 0.3,
            }

            ga_exp = GeneticAlgorithmExperiments(
                functions[f"{func_name}"]["func"],
                functions[f"{func_name}"]["boundaries"],
                64,
            )

            target_value = float(functions[f"{func_name}"]["target"])

            ga_exp.run_experiments([config], target_value=target_value)

            res = ga_exp.results[0]
            reliability = round(res["reliability"], 1)
            avg_iters = (
                round(res["average_iters"], 1)
                if res["average_iters"] != float("inf")
                else "—"
            )

            fake_result = {
                "Тестовая задача": func_name,
                "Тип селекции": "Ранговая"
                if config["selection_method"] == "rank"
                else "Турнирная"
                if config["selection_method"] == "tournament"
                else "Пропорциональная",
                "Надежность": reliability,
                "Ср. итерации": avg_iters,
            }

            self.tree.insert("", tk.END, values=list(fake_result.values()))

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить эксперимент:\n{e}")
            error_msg = traceback.format_exc()
            print(error_msg)


if __name__ == "__main__":
    app = ExperimentGUI()
    app.mainloop()
