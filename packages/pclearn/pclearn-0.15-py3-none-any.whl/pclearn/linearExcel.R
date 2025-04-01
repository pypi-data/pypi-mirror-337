library(ggplot2)
index_data <- read.csv(file.choose(), header = TRUE)
model <- lm(index ~ written + language + tech + gk, 
            data = index_data) 
summary(model)
new_data <- data.frame(written = 48, language = 67, 
                       tech = 56, gk = 54) 
predicted_index <- predict(model, 
                           newdata = new_data)
cat("Predicted Performance Index: ", predicted_index, "\n")
pairs(~index + written + language + tech + gk, data = index_data, main = "Pairwise Scatter 
Plot Matrix") 
ggplot(index_data, aes(x = factor(1), y = written)) +
  geom_boxplot() +
  labs(title = "Box Plot: Written Skills", y = 
         "Written Skills") + theme_minimal()
ggplot(index_data, aes(x = factor(1), y = 
                         language)) + geom_boxplot() +
  labs(title = "Box Plot: Language Skills", y = 
         "Language Skills") + theme_minimal()
ggplot(index_data, aes(x = factor(1), 
                       y = tech)) + geom_boxplot() +
  labs(title = "Box Plot: Technical Knowledge", y = 
         "Technical Knowledge") + theme_minimal()
ggplot(index_data, aes(x = factor(1), 
                       y = gk)) + geom_boxplot() +
  labs(title = "Box Plot: General Knowledge", y = "General 
Knowledge") + theme_minimal()
qqnorm(model$residuals, main = "QQ Plot of 
Residuals") 
qqline(model$residuals, col = "red")
ggplot(data.frame(Fitted = model$fitted.values, Residuals = model$residuals), aes(x = 
                                                                                    Fitted, y = Residuals)) +
  geom_point() +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed") +
  labs(title = "Residuals vs Fitted Values", x = "Fitted Values", y = 
         "Residuals") + theme_minimal()

