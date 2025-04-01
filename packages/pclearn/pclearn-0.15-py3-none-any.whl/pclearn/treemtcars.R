library(rpart)        # CART Model
library(rpart.plot)   # Visualization for rpart Trees
library(tree)         # Tree-Based Models
library(party)        # Conditional Inference Trees
library(caret)        # ML Utilities (Cross-Validation, Confusion Matrix)
library(e1071)        # SVM & ML Tools
# Load & Prepare Data
mydata <- data.frame(mtcars)
mydata$cyl <- as.factor(mydata$cyl)  
# Train-Test Split (70% Train, 30% Test)
set.seed(123)
train_index <- createDataPartition(mydata$cyl, p = 0.7, list = FALSE)
train_data <- mydata[train_index, ]
test_data <- mydata[-train_index, ]
# Decision Tree - rpart (CART)
model_rpart <- rpart(cyl ~ mpg + hp + wt + disp, data = train_data, method = "class")
rpart.plot(model_rpart, type = 3, extra = 101)  # Plot rpart Tree
pred_rpart <- predict(model_rpart, test_data, type = "class")
conf_matrix_rpart <- confusionMatrix(pred_rpart, test_data$cyl)
# Decision Tree - tree (Standard Tree Model)
model_tree <- tree(cyl ~ mpg + hp + wt + disp, data = train_data)
plot(model_tree)
text(model_tree, all = TRUE, cex = 0.6)  # Add Labels
pred_tree <- predict(model_tree, test_data, type = "class")
conf_matrix_tree <- confusionMatrix(pred_tree, test_data$cyl)
print(conf_matrix_tree)
# Decision Tree - ctree (Conditional Inference Tree)
model_ctree <- ctree(cyl ~ mpg + hp + wt + disp, data = train_data)
plot(model_ctree)
pred_ctree <- predict(model_ctree, test_data)
conf_matrix_ctree <- confusionMatrix(pred_ctree, test_data$cyl)
# Hyperparameter Tuning - rpart (Control Depth)
model_rpart_tuned <- rpart(cyl ~ mpg + hp + wt + disp, data = train_data, method = "class", control = rpart.control(maxdepth = 3))
pred_rpart_tuned <- predict(model_rpart_tuned, test_data, type = "class")
conf_matrix_rpart_tuned <- confusionMatrix(pred_rpart_tuned, test_data$cyl)
# Hyperparameter Tuning - tree (Min Split Control)
model_tree_tuned <- tree(cyl ~ mpg + hp + wt + disp, data = train_data, control = tree.control(nobs = nrow(train_data), mincut = 5))
pred_tree_tuned <- predict(model_tree_tuned, test_data, type = "class")
conf_matrix_tree_tuned <- confusionMatrix(pred_tree_tuned, test_data$cyl)
# Hyperparameter Tuning - ctree (Max Depth & Min Split)
model_ctree_tuned <- ctree(cyl ~ mpg + hp + wt + disp, data = train_data, controls = ctree_control(maxdepth = 3, minsplit = 5))
pred_ctree_tuned <- predict(model_ctree_tuned, test_data)
conf_matrix_ctree_tuned <- confusionMatrix(pred_ctree_tuned, test_data$cyl)
# Cross-Validation - rpart (10-Fold CV)
set.seed(123)
train_control <- trainControl(method = "cv", number = 10)
cv_model_rpart <- train(cyl ~ mpg + hp + wt + disp, data = train_data, method = "rpart", trControl = train_control)
pred_cv_rpart <- predict(cv_model_rpart, test_data)
conf_matrix_cv_rpart <- confusionMatrix(pred_cv_rpart, test_data$cyl)
# Accuracy Comparison of Models
accuracy_results <- data.frame(Model = c("rpart", "tree", "ctree", "rpart (Tuned)", "tree (Tuned)", "ctree (Tuned)"),
                               Accuracy = c(conf_matrix_rpart$overall["Accuracy"],
                                            conf_matrix_tree$overall["Accuracy"],
                                            conf_matrix_ctree$overall["Accuracy"],
                                            conf_matrix_rpart_tuned$overall["Accuracy"],
                                            conf_matrix_tree_tuned$overall["Accuracy"],
                                            conf_matrix_ctree_tuned$overall["Accuracy"]))
# Accuracy Visualization
barplot(accuracy_results$Accuracy, names.arg = accuracy_results$Model,
        col = rainbow(6), main = "Decision Tree Model Accuracy (mtcars)",
        ylab = "Accuracy", ylim = c(0, 1))
