# ================== 1 ==================
data <- read.csv("var8.csv", header=TRUE)$x
sample1 <- list(data=sort(data[1:10]), name="Выборка 10 элементов")
sample2 <- list(data=sort(data[1:50]), name="Выборка 50 элементов")
sample3 <- list(data=sort(data), name="Выборка 161 элемент")

print(sample1$data)
print(sample2$data)
print(sample3$data)

# мята #50c8b1
# голубое небо #2fa0d7
# чернилы #070C21
# Чисто белый #FFFFFF)))

# ================== 2 ==================

sample_parameters <- function(sample, name) {
  cat("\nВыборка:", name, "\n")
  # Выборочное среднее арифметическое 
  sample_mean <- mean(sample)
  
  # Несмещённая выб. дисперсия
  sample_var <- var(sample) 
  
  # Смещённая выб. дисперсия
  sample_biased_var <- sample_var * (length(sample) - 1) / length(sample)
  
  # Среднеквадратическое отклонение
  sample_sd <- sd(sample)
  
  # Квартили распределения
  sample_quantiles <- quantile(sample,c(0.25, 0.5, 0.75))
  
  cat("Среднее выборочное:", sample_mean, "\n")
  cat("Смещённая выборочная дисперсия:", sample_biased_var, "\n")
  cat("Несмещённая выборочная дисперсия:", sample_var, "\n")
  cat("Выборочные квантили:", sample_quantiles, "\n")
  
  # Выборочное среднее
  a <- sample_mean
  # Выборочная дисперсия (несм.)
  sigma_2 <- sample_var
  # Среднеквадратическое отклонение.
  sigma <- sample_sd
  print("Точечные оценки")
  print(a)
  print(sigma_2)
  print(sigma**2)
  
  
  # Норм. распределение по точечным оценкам
  len <- seq(sample_mean - 3*sigma, sample_mean + 3*sigma, length.out=200) # диапазон построения нормального распределения
  norma <- dnorm(len, mean=a, sd=sigma) # Функция плотности нормального распределения
  
  # Построение гистограммы относительных частот выборки
  hist(sample, freq = FALSE, breaks = "Sturges",
       main = paste("Гистограмма относительных частот\n", name),
       xlab = "Значения", ylab = "h_i", col = "#50c8b1", border = "#070C21",
       ylim=c(0, 1.4*max(norma)), xlim=range(len)
       )
  
  # Построение нормального распределения
  lines(len, norma, col="#070C21", lwd=2)
  
  # Эмпирическая функция нормального распределения
  f = ecdf(sample)
  plot(f, main = "Графики эмпирической функции распре-
деления и теоретической функции распределения", col="#070C21")
  norma <- pnorm(len, mean=a, sd=sigma) # Функия распределения нормального распределения
  lines(len, norma, col="#070C21")
}

sample_parameters(sample1$data, sample1$name)
sample_parameters(sample2$data, sample2$name)
sample_parameters(sample3$data, sample3$name)

# ================== 3 ==================

# устно

# ================== 4 ==================

confidence_intervals <- function(sample, q) {
  n <- length(sample)
  sample_mean <- mean(sample)
  sample_sigma <- sd(sample)
  
  # Доверительный интервал для мат. ожидания
  
  # квантиль распределения Стьюдента с n − 1 степенью свободы (Tn−1) уровня 1 − ε/2.
  t_student <- qt(1 - (1 - q) / 2, df = n - 1)
  mean_ci <- c(sample_mean - t_student * sample_sigma / sqrt(n), 
               sample_mean + t_student * sample_sigma / sqrt(n))
  
  # Доверительный интервал для дисперсии
  
  # квантиль распределения хи-квадрат с df степенями свободы уровня p
  chi2_low <- qchisq((1 - q) / 2, df = n - 1)
  chi2_high <- qchisq(1 - (1 - q) / 2, df = n - 1)
  variance_ci <- c((n - 1) * var(sample) / chi2_high, 
                   (n - 1) * var(sample) / chi2_low)
  
  return(list(mean_ci = mean_ci, variance_ci = variance_ci))
}

ci_sample <- confidence_intervals(sample1$data, 0.95)
cat(sample1$name,"\nДоверительный интервал для мат. ожидания (q=0.95): ", ci_sample$mean_ci, "\n")
cat(sample1$name,"\nДоверительный интервал для дисперсии (q=0.95): ", ci_sample$variance_ci, "\n")

ci_sample <- confidence_intervals(sample2$data, 0.95)
cat(sample2$name,"\nДоверительный интервал для мат. ожидания (q=0.95): ", ci_sample$mean_ci, "\n")
cat(sample2$name,"\nДоверительный интервал для дисперсии (q=0.95): ", ci_sample$variance_ci, "\n")

ci_sample <- confidence_intervals(sample3$data, 0.95)
cat(sample3$name,"\nДоверительный интервал для мат. ожидания (q=0.95): ", ci_sample$mean_ci, "\n")
cat(sample3$name,"\nДоверительный интервал для дисперсии (q=0.95): ", ci_sample$variance_ci, "\n")


create_mean_confidence_intervals_plots <- function(sample, name, q1, q2) {
  n <- length(sample)
  q_vals <- seq(q1, q2, length.out = 100)
  interval_lengths <- numeric(length(q_vals))
  
  for (i in seq_along(q_vals)) {
    # доверительные интервалы 
    ci <- confidence_intervals(sample, q_vals[i])
    # длины интервалов для мат. ожид.
    interval_lengths[i] <- diff(ci$mean_ci)
  }
  
  plot(q_vals, interval_lengths, type = "l", col = "#070C21", lwd = 2,
       main = paste("Длина доверительного интервала для мат. ожидания\n"),
       xlab = "Уровень доверия q", ylab = "Длина интервала")
  
  #for (i in seq_along(q_vals)) {
    # доверительные интервалы 
    #ci <- confidence_intervals(sample, q_vals[i])
    # длины интервалов для дисперсии
    #interval_lengths[i] <- diff(ci$variance_ci)
  #}
  
  #plot(q_vals, interval_lengths, type = "l", col = "#070C21", lwd = 2,
       #main = paste("Длина доверительного интервала для дисперсии\n", param, name),
       #xlab = "Уровень доверия q", ylab = "Длина интервала")
}

create_var_confidence_intervals_plots <- function(sample, name, q1, q2) {
  n <- length(sample)
  q_vals <- seq(q1, q2, length.out = 100)
  interval_lengths <- numeric(length(q_vals))
  
  for (i in seq_along(q_vals)) {
    # доверительные интервалы 
    ci <- confidence_intervals(sample, q_vals[i])
    # длины интервалов для дисперсии
    interval_lengths[i] <- diff(ci$variance_ci)
  }
  
  plot(q_vals, interval_lengths, type = "l", col = "#070C21", lwd = 2,
  main = paste("Длина доверительного интервала для дисперсии\n"),
  xlab = "Уровень доверия q", ylab = "Длина интервала")
}
par(mfrow = c(3,1))
create_mean_confidence_intervals_plots(sample1$data, sample$name, 0.9, 0.999999)
create_mean_confidence_intervals_plots(sample2$data, sample$name, 0.9, 0.999999)
create_mean_confidence_intervals_plots(sample3$data, sample$name, 0.9, 0.999999)
create_var_confidence_intervals_plots(sample1$data, sample$name, 0.9, 0.999999)
create_var_confidence_intervals_plots(sample2$data, sample$name, 0.9, 0.999999)
create_var_confidence_intervals_plots(sample3$data, sample$name, 0.9, 0.999999)





