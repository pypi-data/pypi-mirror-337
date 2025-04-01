data <- data.frame(
  HomeSize = c(1400, 1300, 1200, 950, 900, 1000, 1300, 850, 1100),
  SellingPrice = c(70, 62, 65, 45, 40, 53, 68, 40, 55)
)
# Scatter plot
plot(data$HomeSize, data$SellingPrice, main = "Home size vs. selling Price",
     xlab = "Home Size (sq ft)", ylab = "Selling Price (lakh Rs.)", pch = 19, col = "blue")
abline(lm(SellingPrice ~ HomeSize, data = data), col = "red") # Add regression line
# Build the linear regression model
model <- lm(SellingPrice ~ HomeSize, data = data)
summary(model)
res <- resid(model)
# Residual vs. Fitted Plot
plot(fitted(model), res, main = "Residuals vs Fitted",
     xlab = "Fitted values", ylab = "Residuals", pch = 19)
abline(0, 0)
# Predict selling price for a home of size 1500 sq ft
new_data <- data.frame(HomeSize = 1500)
predicted_price <- predict(model, newdata = new_data)
# Output the predicted price
predicted_price
