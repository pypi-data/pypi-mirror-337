install.packages("dplyr")  
library(dplyr)  
summary(mtcars)  
install.packages("caTools")   
install.packages("ROCR")     
library(caTools)  
library(ROCR)  
split <- sample.split(mtcars, SplitRatio = 0.8)  
train_reg <- subset(mtcars, split == "TRUE")  
test_reg <- subset(mtcars, split == "FALSE")  
# Train model  
logistic_model <- glm(vs ~ wt + disp, data = train_reg, family = "binomial")  
summary(logistic_model)  
# Predictions  
predict_reg <- predict(logistic_model, test_reg, type = "response")  
predict_reg <- ifelse(predict_reg > 0.5, 1, 0)  
# Accuracy  
table(test_reg$vs, predict_reg)  
missing_classerr <- mean(predict_reg != test_reg$vs)  
print(paste('Accuracy =', 1 - missing_classerr))  
# ROC-AUC  
ROCPred <- prediction(predict_reg, test_reg$vs)  
ROCPer <- performance(ROCPred, measure = "tpr", x.measure = "fpr")  
auc <- performance(ROCPred, measure = "auc")  
auc <- auc@y.values[[1]]  
auc  
# Plot ROC  
plot(ROCPer, colorize = TRUE, print.cutoffs.at = seq(0.1, by = 0.1), main = "ROC CURVE")  
abline(a = 0, b = 1)  
auc <- round(auc, 4)  
legend(.6, .4, auc, title = "AUC", cex = 1)  
