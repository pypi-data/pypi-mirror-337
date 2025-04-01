loan <- read.csv(file.choose(), header = T, sep = ",")  
head(loan)  
summary(loan)  
str(loan)  
# Convert AGE to categorical  
loan$AGE <- as.factor(loan$AGE)  
# Check updated structure  
str(loan)  
# Train logistic regression model  
model1 <- glm(DEFAULTER ~ ., family = binomial, data = loan)  
summary(model1)  
# Null model for comparison  
null <- glm(DEFAULTER ~ 1, family = binomial, data = loan)   
#ANOVA test  
anova(null, model1, test = "Chisq")  
# Predicted probabilities  
loan$predprob <- round(fitted(model1), 2)  
# Display first few rows with predictions  
head(loan)  
# Generate predictions  
pred <- predict(model1, loan, type = "response")  
install.packages("ROCR")  
library(ROCR)  
# ROC curve - Prepare prediction object  
rocrpred <- prediction(pred, loan$DEFAULTER)  
# Performance evaluation  
rocrperf <- performance(rocrpred, "tpr", "fpr")  
# Plot ROC curve  
plot(rocrperf, colorize = TRUE, print.cutoffs.at = seq(0.1, by = 0.1))  
# Compute AUC  
auc <- performance(rocrpred, measure = "auc")  
auc <- auc@y.values[[1]]  
auc  
# Coefficients of the model  
coef(model1)  
# Exponentiated coefficients (odds ratio)  
exp(coef(model1))  
