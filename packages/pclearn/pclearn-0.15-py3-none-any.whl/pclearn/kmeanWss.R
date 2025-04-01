data("iris")
names(iris)
# Subset the dataset to exclude the Species column
new_data <- subset(iris, select = -Species)
new_data
# Perform K-means clustering with 3 clusters
cl <- kmeans(new_data, 3)
cl
# Calculate the total within-cluster sum of squares (WSS) for different values of k
wss <- sapply(1:15, function(k) {
  kmeans(new_data, k)$tot.withinss
})
wss
# Visualize the WSS values to determine the optimal number of clusters
plot(1:15, wss,
     type = "b", pch = 19, frame = FALSE, 
     xlab = "Number of clusters K",
     ylab = "Total within-clusters sum of squares")
# Install and load the 'cluster' package
install.packages("cluster")
library(cluster)
# Visualize the clusters
clusplot(new_data, cl$cluster, color = TRUE, shade = TRUE, labels = 2, lines = 0)
# Display cluster assignments for each data point
cl$cluster
# Display the centroids of the clusters
cl$centers
