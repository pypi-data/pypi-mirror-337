data(iris)
str(iris)
# Install required packages
install.packages("ClusterR")
install.packages("cluster")
library(ClusterR)
library(cluster)
# Remove the Species column
iris_1 <- iris[, -5]
# Set seed for reproducibility
set.seed(240)
# Perform K-means clustering with 3 clusters
kmeans.re <- kmeans(iris_1, centers = 3, nstart = 20)
kmeans.re
# Display cluster assignments
kmeans.re$cluster
# Create a confusion matrix to compare clustering results with actual species
cm <- table(iris$Species, kmeans.re$cluster)
cm
# Scatter plot of Sepal.Length vs Sepal.Width
plot(iris_1[c("Sepal.Length", "Sepal.Width")])
plot(iris_1[c("Sepal.Length", "Sepal.Width")], 
     col = kmeans.re$cluster, 
     main = "Clusters: Sepal Length vs Sepal Width", 
     xlab = "Sepal Length", 
     ylab = "Sepal Width", 
     pch = 19)
# Add cluster centers to the plot
points(kmeans.re$centers[, c("Sepal.Length", "Sepal.Width")], 
       col = 1:3, pch = 8, cex = 3)
# Visualize clusters using clusplot
y_kmeans <- kmeans.re$cluster
clusplot(iris_1[, c("Sepal.Length", "Sepal.Width")],
         y_kmeans,
         lines = 0,
         shade = TRUE,
         color = TRUE,
         labels = 2,
         plotchar = FALSE,
         span = TRUE,
         main = paste("Cluster iris"),
         xlab = "Sepal.Length",
         ylab = "Sepal.Width")

