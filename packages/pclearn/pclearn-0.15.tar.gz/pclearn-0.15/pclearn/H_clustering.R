# Load dataset
data("iris")
names(iris)
# Perform hierarchical clustering on Petal.Length and Petal.Width
clusters <- hclust(dist(iris[, 3:4]))
# Plot the dendrogram
plot(clusters, main = "Dendrogram - Single Linkage")
# Cut the dendrogram into 3 clusters
clusterCut <- cutree(clusters, 3)
# Compare cluster assignments with actual species
table(clusterCut, iris$Species)
# Install & load ggplot2 if not installed
if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
library(ggplot2)
# Scatter plot of actual species
ggplot(iris, aes(x = Petal.Length, y = Petal.Width, color = Species)) + 
  geom_point(alpha = 0.4, size = 3.5) +
  ggtitle("Petal Length vs Petal Width - Actual Species")
# Scatter plot with hierarchical clustering results
ggplot(iris, aes(x = Petal.Length, y = Petal.Width)) + 
  geom_point(aes(color = as.factor(clusterCut)), size = 3.5) + 
  scale_color_manual(values = c('black', 'red', 'green')) +
  ggtitle("Hierarchical Clustering (Single Linkage)")
# Perform hierarchical clustering with 'average' linkage
clusters_avg <- hclust(dist(iris[, 3:4]), method = 'average')
# Cut the dendrogram into 3 clusters
clusterCut1 <- cutree(clusters_avg, 3)
# Compare cluster assignments with actual species
table(clusterCut1, iris$Species)
# Plot the new dendrogram
plot(clusters_avg, main = "Dendrogram - Average Linkage")

# Scatter plot with hierarchical clusters (Average Linkage)
ggplot(iris, aes(x = Petal.Length, y = Petal.Width)) + 
  geom_point(aes(color = as.factor(clusterCut1)), size = 3.5) + 
  scale_color_manual(values = c('black', 'red', 'green')) +
  ggtitle("Hierarchical Clustering (Average Linkage)")

