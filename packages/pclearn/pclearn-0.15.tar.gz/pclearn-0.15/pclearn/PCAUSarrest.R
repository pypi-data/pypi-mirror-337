data(USArrests)
head(USArrests)
summary(USArrests)
# Perform PCA
mypr_usa <- prcomp(USArrests, scale = TRUE)
# Scatter Plot
plot(USArrests$Murder, USArrests$Assault)
plot(scale(USArrests$Murder), scale(USArrests$Assault))
# PCA Summary
summary(mypr_usa)
str(mypr_usa)
# Scree Plot & Biplot
plot(mypr_usa, type = "l")
biplot(mypr_usa, scale = 0)
# PCA Scores & Append to Data
mypr_usa$x
usarrests2 <- cbind(USArrests, mypr_usa$x[, 1:2])
head(usarrests2)
# Correlation with PCA Components
cor(USArrests, usarrests2[, 5:6])
install.packages("pls")
library(pls)
# Perform PCR
pcmodel_usa <- pcr(Murder ~ ., ncomp = 3, data = USArrests, scale = TRUE)
# Predict Using PCR
USArrests$pred <- predict(pcmodel_usa, USArrests, ncomp = 2)
head(USArrests)