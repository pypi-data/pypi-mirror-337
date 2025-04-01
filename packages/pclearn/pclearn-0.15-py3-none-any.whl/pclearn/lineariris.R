# Load the Iris dataset
data(iris)
# Scatterplot to visualize the relationship
plot(iris$Sepal.Width, iris$Sepal.Length, main = "Sepal.Width vs Sepal.Length",
     xlab = "Sepal Width (cm)", ylab = "Sepal Length (cm)",
     pch = 19, col = "blue")
abline(lm(Sepal.Length ~ Sepal.Width, data = iris), col = "red") # Add regression line
# Build the linear regression model
model <- lm(Sepal.Length ~ Sepal.Width, data = iris)
summary(model)
res <- resid(model)
# Residual vs. Fitted Plot
plot(fitted(model), res, main = "Residuals vs Fitted",
     xlab = "Fitted values", ylab = "Residuals", pch = 19)
abline(0, 0)
# Predict Sepal.Length for sepal.width = 3.5
new_data <- data.frame(Sepal.Width = 3.5)
predicted_sepal_length <- predict(model, newdata = new_data)
# Output the predicted value
predicted_sepal_length