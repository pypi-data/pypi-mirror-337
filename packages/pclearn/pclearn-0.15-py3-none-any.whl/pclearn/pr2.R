#1
weights<-c(63, 63, 66, 67, 68, 69, 70, 70, 71, 71)
t.test(weights, mu=66)
#2
weights<-c(50, 49, 52, 44, 45, 48, 46, 45, 49, 45)
t.test(x=weights, mu=50)
#3
weights<-c(70, 120, 110, 101, 88, 83, 95, 88, 107, 100)
t.test(x=weights, mu=100)
#4
data("mtcars")
mpg=(mtcars$mpg)
t.test(mpg,mu=20)

#5 6
s1<-c(53,28,31,48,50,42)
s2<-c(58,29,30,55,56,45)
t.test(s1, s2, paired = TRUE)

#7
library (MASS)
data=table(survey$Smoke, survey$Exer)
chisq.test(data)

#8
data=table(mtcars$cyl, mtcars$carb)
chisq.test(data)

#9
Data <- matrix(c(35, 15, 50, 10, 30, 60), nrow = 2, ncol = 3, byrow = T)
rownames(Data) <- c('Female', 'Male')
colnames(Data) <- c('Archery', 'Boxing', 'Cycling')
Data
chisq.test(Data)

#10
data=matrix(c(8,10,12,178,21,21), nrow=2, ncol=3, byrow=T)
rownames(data)= c("Left", "Right")
colnames(data)=c("0","1","2")
data
chisq.test(data)

#11
HouseTask= read.csv(file.choose(), sep=",", header=TRUE)
data=HouseTask[,-1]
chisq.test(data)