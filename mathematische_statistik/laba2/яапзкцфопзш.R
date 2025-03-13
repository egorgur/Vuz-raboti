# ================== 1 ==================
data <- read.csv("var8.csv", header=TRUE)$x
sample1 <- sort(data[1:10])
sample2 <- sort(data[1:50])
sample3 <- sort(data)


f1 = ecdf(sample1)
f2 = ecdf(sample2)
f3 = ecdf(sample3)


sample_var <- var(sample3) 
sample_mean <- mean(sample3)
sample_sd <- sd(sample3)

len <- seq(sample_mean - 3*sample_sd, sample_mean + 3*sample_sd, length.out=1000)
norma <- pnorm(-3, mean=sample_mean, sd=sample_sd) # Функия распределения нормального распределения



print(f1(-3))
print(f2(-3))
print(f3(-3))



norma <- pnorm(-3, mean=sample_mean, sd=sample_sd) # Функия распределения нормального распределения
print("norma")
print(norma)


print(f1(-1))
print(f2(-1))
print(f3(-1))

norma <- pnorm(-1, mean=sample_mean, sd=sample_sd) # Функия распределения нормального распределения

print("norma")
print(norma)

print(f1(0))
print(f2(0))
print(f3(0))

norma <- pnorm(-0, mean=sample_mean, sd=sample_sd) # Функия распределения нормального распределения
print("norma")
print(norma)



