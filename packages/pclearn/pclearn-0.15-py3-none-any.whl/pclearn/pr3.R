data = read.csv(file.choose(),header =T)
var.test(data$A, data$B)


#2
data = read.csv(file.choose(), header =T)
var.test(data$time_g1, data$time_g2)


#3
edu = read.csv(file.choose(),header =T)
var.test(edu$UK, edu$Germany)

#4
data = read.csv(file.choose(), header =T)
names(data)
result=aov(formula = SatIndex ~ Dept, data=data)
summary(result)

#5
#Load necessary library
library(ggplot2)
data = read.csv(file.choose(), header = TRUE)
names(data)
# Perform ANOVA
result = aov(SatIndex ~ Dept + Experience + Dept * Experience, data = data)
summary(result)
# Data visualization 
ggplot(data, aes(x = Dept, y = SatIndex, color = Experience)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Satisfaction Index by Department and Experience Level",
       x = "Department", 
       y = "Satisfaction Index")
plot(result)

#6
data = read.csv(file.choose(), header =T)
names(data)
result=aov(formula =  Pol_int ~ Gender+Edu+Gender*Edu, data=data)
summary(result)
