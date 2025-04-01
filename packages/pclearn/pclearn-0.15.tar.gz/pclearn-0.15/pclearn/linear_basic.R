data<- data.frame(
  Height=c(151,174,138,186,128,136,179,163,152),
  Weight=c(63,81,56,91,47,57,76,72,62)
)
#scatter plot
plot(data$Height,data$Weight,main="Height vs Weight",xlab="Height",ylab="Weight",pch=19)
abline(lm(Weight~Height,data=data))
summary(data)
model<- lm(formula = Weight~Height, data=data)
#residual
res<- resid(model)
plot(fitted(model),res,main = "Residual vs Fitted")
abline(0,0)
#predict weight for height of 140cm
new_data<-data.frame(Height=140)
predicted_weight<-predict(model,newdata=new_data)
predicted_weight
