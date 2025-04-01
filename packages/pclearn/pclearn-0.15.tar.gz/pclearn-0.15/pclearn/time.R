data("AirPassengers")
class(AirPassengers)  
str(AirPassengers)
# Start and end year, frequency of observations
start(AirPassengers)  
end(AirPassengers)  
frequency(AirPassengers)  
# Statistical summary
summary(AirPassengers)
# Plot original time series
title_main <- "Air Passenger Traffic (1949-1960)"
plot(AirPassengers, main=title_main, ylab="Passengers", xlab="Year")
# Add a trend line
abline(reg=lm(AirPassengers ~ time(AirPassengers)))  
# Check monthly cycle pattern
cycle(AirPassengers)
# Yearly average passenger count
plot(aggregate(AirPassengers, FUN=mean), main="Yearly Avg Passenger Count")
# Boxplot for monthly variation
boxplot(AirPassengers ~ cycle(AirPassengers), 
        main="Monthly Passenger Variation", xlab="Month", ylab="Passengers")
#Stationarity Check 
acf(AirPassengers, main="ACF: Original Data")  # Autocorrelation (raw data)
acf(log(AirPassengers), main="ACF: Log-Transformed")  # Log transformation check
acf(diff(log(AirPassengers)), main="ACF: Differenced Log")  # Stationarity test
pacf(diff(log(AirPassengers)), main="PACF: Differenced Log") # Partial ACF
# Plot differenced log data
plot(diff(log(AirPassengers)), main="Differenced Log Data")
# Fit ARIMA model (Trend & Seasonality handled)
fit <- arima(log(AirPassengers), 
             order = c(0,1,1), 
             seasonal = list(order = c(0,1,1), period = 12))
#Forecasting 
pred <- predict(fit, n.ahead = 10*12)  # Predict for 10 years (120 months)
# Convert forecast to original scale
pred1 <- round(exp(pred$pred), 0)
# Print forecast (1961-1970)
print(pred1)
# Plot: Original vs Forecast
ts.plot(AirPassengers, pred1, log="y", lty=c(1,3), main="Original vs Predicted")
# Extract first 12 forecasted values
data1 <- head(pred1, 12)
data1
# Train ARIMA using 1949-1959 data only
datawide <- ts(AirPassengers, frequency=12, start=c(1949,1), end=c(1959,12))
datawide
# Fit ARIMA model on training data
fit1 <- arima(log(datawide), 
              order=c(0,1,1), 
              seasonal=list(order=c(0,1,1), period=12))
# Predict 1960-1970
pred2 <- predict(fit1, n.ahead=10*12)
# Convert forecast to original scale
pred2_original <- round(exp(pred2$pred), 0)
# Print forecast values
print(pred2_original)

