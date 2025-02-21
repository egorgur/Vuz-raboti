data <- c(2,20,2,0,1,0,0,0,0,1,5,0,3,5,4,4,2,11,5,5) #пОМЕНЯЙ

empirical_function <- ecdf(data)

print(empirical_function(5)) #ПОМЕНЯЙ ЗНАЧЕНИЕ!!!



#===============================================================================






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

