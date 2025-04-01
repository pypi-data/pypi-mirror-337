data(mtcars)
head(mtcars)
summary(mtcars)
# Perform PCA
mypr_mtcars <- prcomp(mtcars, scale = TRUE)
# Scatter Plot
plot(mtcars$mpg, mtcars$hp)
plot(scale(mtcars$mpg), scale(mtcars$hp))
# PCA Summary
summary(mypr_mtcars)
str(mypr_mtcars)
# Scree Plot & Biplot
plot(mypr_mtcars, type = "l")
biplot(mypr_mtcars, scale = 0)
# PCA Scores & Append to Data
mypr_mtcars$x
mtcars2 <- cbind(mtcars, mypr_mtcars$x[, 1:2])
head(mtcars2)
# Correlation with PCA Components
cor(mtcars[, -1], mtcars2[, 12:13])
install.packages("pls")
library(pls)
# Perform PCR
pcmodel_mtcars <- pcr(mpg ~ ., ncomp = 3, data = mtcars, scale = TRUE)
# Predict Using PCR
mtcars$pred <- predict(pcmodel_mtcars, mtcars, ncomp = 2)
head(mtcars)