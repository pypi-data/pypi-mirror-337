# Load the mtcars dataset
data(mtcars)
# Scatterplot to visualize the relationship
plot(mtcars$hp, mtcars$mpg, main = "Horsepower vs Miles per Gallon",
     xlab = "Horsepower", ylab = "Miles per Gallon (mpg)",
     pch = 19, col = "blue")
abline(lm(mpg ~ hp, data = mtcars), col = "red") #Add regression line
#Build the linear regression model
model <- lm(mpg ~ hp, data = mtcars)
# Summary of the model
summary(model)
# Residuals
res <- resid(model)
# Residual vs Fitted Plot
plot(fitted(model), res, main = "Residuals vs Fitted",
     xlab = "Fitted values", ylab = "Residuals", pch = 19)
abline(0, 0)
# Predict mpg for a car with 150 horsepower
new_data <- data.frame(hp = 150)
predicted_mpg <- predict(model, newdata = new_data)
predicted_mpg
