data <- c(4,4,4,4 
          1, 1, 1, 1, 
          1, 1, 
          1, 1, 
          1, 1, 2, 2, 3, 5) #МЕТОД ПОДБОРА, САМОПРОВЕРКА!!!
print(data) # Вывод выборки


#=====================================================================================





# Создание эмпирической функции распределения
empirical_function <- ecdf(data)

# Построение графика
plot(empirical_function, 
     main = "Эмпирическая функция распределения", 
     xlab = "x", 
     ylab = "F(x)", 
     col = "blue", 
     lwd = 2)
grid()

# Добавление подписей к точкам
points(sort(data), empirical_function(sort(data)), col = "red", pch = 16)
text(sort(data), empirical_function(sort(data)), 
     labels = round(empirical_function(sort(data)), 3), 
     pos = 3, col = "red")

# --------------------------------------------
# Наблюдаемые частоты
observed <- c(60, 15, 9, 6)

# Параметр показательного распределения
lambda <- 0.6

# Общая сумма наблюдаемых частот
n <- sum(observed)

# Ожидаемые частоты для каждого интервала
expected <- numeric(length(observed))
for (i in seq_along(expected)) {
  lower_bound <- (i - 1) * 10
  upper_bound <- i * 10
  expected[i] <- n * (pexp(upper_bound, rate = lambda) - pexp(lower_bound, rate = lambda))
}

# Расчет статистики хи-квадрат
chi_squared <- sum((observed - expected)^2 / expected)

# Степени свободы
df <- length(observed) - 1

# Уровень значимости
alpha <- 0.01

# Критическое значение из таблицы хи-квадрат
critical_value <- qchisq(1 - alpha, df)

# Результаты
cat("Статистика хи-квадрат:", chi_squared, "\n")
cat("Критическое значение:", critical_value, "\n")

if (chi_squared > critical_value) {
  cat("Нулевая гипотеза отвергается: данные не соответствуют показательному распределению.\n")
} else {
  cat("Нулевая гипотеза не отвергается: данные соответствуют показательному распределению.\n")
}

# ==========
# Создаем вектор данных
set.seed(123) # Для воспроизводимости
n <- 100 # количество наблюдений
rate <- 1/5 # параметр лямбда для показательного распределения
data <- rexp(n, rate) # Генерируем данные из показательного распределения

# Определяем интервалы для хи-квадрат теста
breaks <- seq(0, max(data), by=1)
observed_freq <- hist(data, breaks=breaks, plot=FALSE)$counts

# Найти теоретические вероятности для каждого интервала
expected_prob <- diff(pexp(breaks, rate))
expected_freq <- expected_prob * n

# Применяем хи-квадрат тест
chisq_test <- chisq.test(observed_freq, p=expected_prob, rescale.p=TRUE)

# Результат
print(chisq_test)
