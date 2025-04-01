# Create the dataset
data <- data.frame(
  Yearsofservice = c(11, 7, 9, 5, 8, 6, 10),
  Income = c(17, 15, 13, 12, 16, 14, 18)
)
# Scatterplot
plot(data$Yearsofservice, data$Income, main = "Years of Service vs. Income",
     xlab = "Years of Service", ylab = "Income (in thousands of Rs.)",
     pch = 19, col = "blue")
abline(lm(Income ~ Yearsofservice, data = data), col = "red") # Add regression line
# Build the linear regression model
model <- lm(Income ~ Yearsofservice, data = data)
summary(model)
res <- resid(model)
# Residual vs. Fitted Plot
plot(fitted(model), res, main = "Residuals vs Fitted",
     xlab = "Fitted values", ylab = "Residuals", pch = 19)
abline(0, 0)
# Predict income for 12 years of service
new_data <- data.frame(Yearsofservice = 12)
predicted_income <- predict(model, newdata = new_data)
# Output the predicted income
predicted_income