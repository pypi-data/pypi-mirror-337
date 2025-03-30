# Load necessary packages
if (!require(ClusterR)) install.packages("ClusterR")
if (!require(cluster)) install.packages("cluster")
library(ClusterR)
library(cluster)

# Remove the Species column for clustering
iris_1 <- iris[, -5]

# Set seed for reproducibility
set.seed(240)

# Perform K-means clustering with 3 clusters
kmeans.re <- kmeans(iris_1, centers = 3, nstart = 20)

# Display clustering results
print(kmeans.re)

# Compare clustering results with actual species
cm <- table(iris$Species, kmeans.re$cluster)
print(cm)

# Visualize clusters (Sepal.Length vs Sepal.Width)
plot(iris_1[c("Sepal.Length", "Sepal.Width")], 
     col = kmeans.re$cluster,
     main = "Clusters: Sepal Length vs Sepal Width",
     xlab = "Sepal Length",
     ylab = "Sepal Width",
     pch = 19)

# Add cluster centers to the plot
points(kmeans.re$centers[, c("Sepal.Length", "Sepal.Width")], 
       col = 1:3, 
       pch = 8, 
       cex = 3)

# Visualize using clusplot
clusplot(iris_1[, c("Sepal.Length", "Sepal.Width")],
         kmeans.re$cluster,
         lines = 0,
         shade = TRUE,
         color = TRUE,
         labels = 2,
         plotchar = FALSE,
         span = TRUE,
         main = "Cluster Visualization (K-means)",
         xlab = "Sepal Length",
         ylab = "Sepal Width")

