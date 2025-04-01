data("iris")  
head(iris)  
summary(iris)  
# Perform PCA  
mypr <- prcomp(iris[, -5], scale = TRUE)  
# Scatter Plot  
plot(iris$Sepal.Length, iris$Sepal.Width)  
plot(scale(iris$Sepal.Length), scale(iris$Sepal.Width))  
# PCA Summary  
summary(mypr)  
str(mypr)  
# Scree Plot & Biplot  
plot(mypr, type = "l")  
biplot(mypr, scale = 0)  
# PCA Scores & Append to Data  
mypr$x  
iris2 <- cbind(iris, mypr$x[, 1:2])  
head(iris2)  
# Correlation with PCA Components  
cor(iris[, -5], iris2[, 6:7])  
install.packages("pls")  
library(pls)  
# Perform PCR  
pcmodel <- pcr(Sepal.Length ~ Species + Sepal.Width + Petal.Length + Petal.Width, ncomp = 3, data = iris, scale = TRUE)  
# Predict Using PCR  
iris$pred <- predict(pcmodel, iris, ncomp = 2)  
head(iris)  
