# Load dataset  
data(Titanic)  
# Convert to dataframe  
data <- as.data.frame(Titanic)  
# Train model  
model <- glm(Survived ~ Class + Sex + Age, family = binomial, data = data)  
summary(model)  
# Install & Load package  
install.packages("ROCR")  
library(ROCR)  
# Predictions  
predictions <- predict(model, type = "response")  
# ROC Curve  
prediction_objects <- prediction(predictions, data$Survived)  
roc_object <- performance(prediction_objects, measure = "tpr", x.measure = "fpr")  
# Plot ROC  
plot(roc_object, main = "ROC Curve", col = "blue", lwd = 2)  
legend("bottomright", legend = paste("AUC =", round(performance(prediction_objects, measure = "auc")@y.values[[1]], 2)), col = "blue", lwd = 2)  
