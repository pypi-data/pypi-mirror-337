library(rpart)      
library(rpart.plot) 
library(tree)        # Tree-Based Models
library(party)       # Conditional Inference Trees
library(caret)       # Machine Learning Utilities
library(e1071)       # SVM & ML Tools
data(iris)
mydata <- data.frame(iris)
# Decision Tree - rpart
model_rpart <- rpart(Species ~ ., data = mydata, method = "class")
rpart.plot(model_rpart, type = 3, extra = 101, fallen.leaves = TRUE)
# Decision Tree - tree
model_tree <- tree(Species ~ ., data = mydata)
plot(model_tree)
text(model_tree, all = TRUE, cex = 0.6)
# Decision Tree - party (ctree)
model_ctree <- ctree(Species ~ ., data = mydata)
plot(model_ctree)
# Tuning - tree (Min Split Control)
model_tree_tuned <- tree(Species ~ ., data = mydata, control = tree.control(nobs = nrow(mydata), mincut = 10))
plot(model_tree_tuned)
text(model_tree_tuned, all = TRUE, cex = 0.6)
# Predictions - Tuned Tree
predict(model_tree_tuned, iris)
predict(model_tree_tuned, iris, type = "class")
# Controlling Depth - party (ctree)
model_ctree_tuned <- ctree(Species ~ ., data = mydata, controls = ctree_control(maxdepth = 2))
plot(model_ctree_tuned)
# Train-Test Split
set.seed(123)
train_index <- createDataPartition(mydata$Species, p = 0.7, list = FALSE)
train_data <- mydata[train_index, ]
test_data <- mydata[-train_index, ]
# rpart
model_rpart_eval <- rpart(Species ~ ., data = train_data, method = "class")
pred_rpart <- predict(model_rpart_eval, test_data, type = "class")
conf_matrix_rpart <- confusionMatrix(pred_rpart, test_data$Species)
# tree
model_tree_eval <- tree(Species ~ ., data = train_data)
pred_tree <- predict(model_tree_eval, test_data, type = "class")
conf_matrix_tree <- confusionMatrix(pred_tree, test_data$Species)
# ctree
model_ctree_eval <- ctree(Species ~ ., data = train_data)
pred_ctree <- predict(model_ctree_eval, test_data)
conf_matrix_ctree <- confusionMatrix(pred_ctree, test_data$Species)
# Accuracy Comparison
accuracy_results <- data.frame(Model = c("rpart", "tree", "ctree"),
                               Accuracy = c(conf_matrix_rpart$overall["Accuracy"],
                                            conf_matrix_tree$overall["Accuracy"],
                                            conf_matrix_ctree$overall["Accuracy"]))
print(accuracy_results)
# Accuracy Visualization
barplot(accuracy_results$Accuracy, names.arg = accuracy_results$Model,
        col = c("red", "blue", "green"), main = "Decision Tree Model Accuracy",
        ylab = "Accuracy", ylim = c(0, 1))

