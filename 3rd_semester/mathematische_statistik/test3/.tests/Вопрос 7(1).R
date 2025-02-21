
# Рассчитываем критическое значение хи-квадрат для уровня значимости 0.05
alpha <- 0.01 #МЕНЯЕМ ЗНАЧЕНИЕ!!!

observed <- matrix(c(2721, 345, 
                     129, 138), 
                   nrow = 2, byrow = TRUE) 
print(observed)

#МЕНЯЕМ ЗНАЧЕНИЕ, КАК В ТАБЛИЦЕ, МЕНЯЕМ КОЛИЧЕСТВО СТРОК (nrow)!!!







#===================================================================================================


# Сумма по строкам (для каждой группы)
row_sums <- rowSums(observed)

# Сумма по столбцам (для каждого продукта)
col_sums <- colSums(observed)

# Общая сумма (n)
total_sum <- sum(observed)

# Рассчитываем статистику хи-квадрат вручную по формуле
chi_square_statistic <- 0

# Идем по всем ячейкам таблицы
for (i in 1:nrow(observed)) {
  for (j in 1:ncol(observed)) {
    # Ожидаемое значение для ячейки
    expected_value <- (row_sums[i] * col_sums[j]) / total_sum
    # Добавляем вклад в статистику хи-квадрат
    chi_square_statistic <- chi_square_statistic + ((observed[i, j] - expected_value)^2) / expected_value
  }
}

# Выводим результат
cat("Выборочное значение статистики хи-квадрат:", chi_square_statistic, "\n")

# Рассчитываем число степеней свободы (df)
df <- (nrow(observed) - 1) * (ncol(observed) - 1)
print(df)
critical_value <- qchisq(1 - alpha, df)

cat("Критическое значение хи-квадрат при уровне значимости 0.025:", critical_value, "\n")

# Проверка гипотезы
if (chi_square_statistic > critical_value) {
  cat("\nГипотеза о независимости отвергается (наблюдаемое значение больше критического).\n")
} else {
  cat("\nНет оснований отвергнуть гипотезу о независимости (наблюдаемое значение меньше или равно критическому).\n")
}
