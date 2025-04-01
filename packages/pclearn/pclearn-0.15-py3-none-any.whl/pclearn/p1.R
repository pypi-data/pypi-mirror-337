# Reading the CSV file and loading the dataset
eda_data <- read.csv(file.choose(), header = TRUE, sep = ",")
eda_data  
head(eda_data)  
summary(eda_data)  
str(eda_data)  
# Display the first 8 rows of the dataset
eda_data[1:8,]
# Display the first 3 and 8 rows specifically
head(eda_data, 3)
head(eda_data, 8)
# Display the last 8 rows
tail(eda_data, 8)
# Display the first 8 rows and columns 1 and 5
eda_data[1:8, c(2,3)]
# Display the first 5 columns of the dataset
eda_data[, 1:2]
# Subsetting data: Selecting rows where Education is "Grad"
newdata1 <- subset(eda_data, eda_data$Education == "Grad")
newdata1
# Subsetting data: Selecting rows where Age is 51 and Gender is Male
newdata2 <- subset(eda_data, eda_data$Age == "51" & eda_data$Gender == "M")
newdata2
# Sorting data by Name column in ascending order
a <- eda_data[order(eda_data$Name),]
a
# Sorting data by Education column in ascending order
a <- eda_data[order(eda_data$Education),]
a
# Sorting data by Education column in descending order
a <- eda_data[order(eda_data$Education, decreasing = TRUE),]
a
# Counting missing values (NA) in each column
a <- colSums(is.na(eda_data))
a
# Create a histogram of the Age column
hist(eda_data$Age)
# Create a boxplot of the Age column
boxplot(eda_data$Age)
# Statistical measures for Age column
mean(eda_data$Age)  # Mean
min(eda_data$Age)  # Minimum value
max(eda_data$Age)  # Maximum value
median(eda_data$Age)  # Median
mode(eda_data$Garage)  # Mode (this function is missing, you will define it later)
# Frequency table for the Garage column
y <- table(eda_data$Garage)
y
# Display the most frequent value in the Garage column
names(y)[which(y == max(y))]
# Find the maximum count and the index of the most frequent value
ma <- max(y)
ma
whch <- which(y == ma)
whch
names(y)[whch]

# Create a frequency table for the Garage column
x <- eda_data$Garage
x
y <- unique(x)
y
mat <- match(x, y)
mat
tab <- tabulate(mat)
tab
m <- max(tab)
m
y[tab == m]
# Define a function to calculate the mode of a given vector
my_mode <- function(x) {  # Mode function
  unique_x <- unique(x)
  tabulate_x <- tabulate(match(x, unique_x))
  unique_x[tabulate_x == max(tabulate_x)]
}
# Apply the mode function to the Age column
x <- eda_data$Age
my_mode(x)
# Example of using the mode function on a custom vector
x <- c(0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 4)
x
y <- table(x)
y
y[max(y)]
# Histograms for other columns
hist(eda_data$Rooms)
hist(eda_data$Salary)
# Create a two-way table of Education vs Gender
counts = table(eda_data$Education, eda_data$Gender)
counts
# Barplot of Education vs Gender distribution
barplot(counts, main = "Data distribution by Education Vs Gender", col = c("blue", "red"))
# Scatterplot of Age vs Salary
plot(eda_data$Age, eda_data$Salary)
# Skewness of the Rooms column
library(PerformanceAnalytics)
a <- skewness(eda_data$Rooms)
a
hist(eda_data$Rooms)

# Skewness of the Garage column
library(e1071)
b <- skewness(eda_data$Garage)
b
hist(eda_data$Garage)

# Imputing missing values: Replace NA in Garage with the mean
eda_data$Garage[is.na(eda_data$Garage)] <- mean(eda_data$Garage, na.rm = TRUE)
View(eda_data)

# Imputing missing values in Rooms: Replace NA with the median
skewness(eda_data$Rooms)
a
hist(a)

hist(eda_data$Rooms)
b <- eda_data$Rooms[is.na(eda_data$Rooms)] <- median(eda_data$Rooms, na.rm = TRUE)
b
hist(b)
View(eda_data)

# Mode function: Define a function to calculate the mode
getmode <- function(v) {
  v = v[nchar(as.character(v)) > 0]
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

# Identifying duplicate data in specific columns
data <- eda_data[1:5, 3:4]
data
duplicated(data)

# Removing duplicate data
a <- data[!duplicated(data),]
a

# Removing an outlier from the AppraisedValue column
boxplot(eda_data$AppraisedValue)

plot(eda_data$AppraisedValue)
x <- eda_data$AppraisedValue
x
out <- boxplot.stats(x)$out  # Identifying the outlier
out  # Boxplot identified the 1200 value as an outlier
x <- x[!(x %in% out)]  # Removing outliers
x  # This removes 1200 from x
boxplot(x)  # Display boxplot after outlier removal

# Imputing missing values by replacing values greater than 1000 with 850
q <- quantile(eda_data$AppraisedValue, .95)  # 95th percentile
q  # 850
summary(eda_data$AppraisedValue)
app_val <- ifelse(eda_data$AppraisedValue >= 1000, 850, eda_data$AppraisedValue)
app_val
boxplot(app_val)

# Conversion: Character to numeric values
str <- eda_data$Gender
str
str(eda_data$Gender)
str(eda_data$Education)
num <- as.numeric(str)  # Convert to numeric
num
str(num)

# Check data type and class of the numeric variable
typeof(num)
class(num)

# Convert to factor (categorical variable)
num <- as.factor(num)
num
class(num)

# Convert back to character
num <- as.character(num)
num
class(num)
typeof(num)

# Numeric to logical conversion
v <- c(0, 0, 1, 1)
v
logi <- as.logical(v)  # Convert numeric to logical
logi

# Logical to numeric conversion
int <- as.integer(logi)
int
typeof(int)

# Convert integer to factor
fact <- as.factor(int)
fact

# Display the structure of the Name column
str(eda_data$Name)



# 1. Create Student.csv file with fields(rollno, name, gender, class, Tmarks)
student_data <- read.csv("Student.csv", header = TRUE)
head(student_data)
# 3. Check the data type of dataset's fields
str(student_data)
# 4. Get the summary of data set
summary(student_data)
# 5. Check the dimensions of dataset and list column names
dim(student_data)  # Dimensions (rows, columns)
colnames(student_data) # Column names
# 6. List the row sets where total marks are more than 750
high_marks_students <- subset(student_data, student_data$Tmarks > 750)
high_marks_students
# 7. List only the first 2 columns where total marks are more than 750 and class is SYCS
filtered_data <- subset(student_data, student_data$Tmarks > 750 & student_data$class == "SYCS", select = c(rollno, name))
filtered_data
# 8. Sort the data in ascending order of total marks
sorted_data <- student_data[order(student_data$Tmarks), ]
sorted_data
# 9. List the records where total marks are not entered.
missing_marks_students <- subset(student_data, is.na(student_data$Tmarks))
missing_marks_students
# 10. Plot the scatter plot which shows relation between average marks and class.
plot(as.factor(student_data$class), student_data$Tmarks,
     xlab = "Class", ylab = "Total Marks",
     main = "Total Marks vs. Class")
# 11. Draw the box plot for totalmarks
boxplot(student_data$Tmarks, ylab = "Total Marks", main = "Boxplot of Total Marks")
# 12. Get the summary of data set
summary(student_data)
# 13. Check the dimensions of dataset and list column names
dim(student_data)
colnames(student_data)
# 14. List the row sets where total marks are more than 750
high_marks_students_2 <- subset(student_data, student_data$Tmarks > 750)
high_marks_students_2
# 15. List only the first 2 columns where total marks are more than 750 and class is SYCS
filtered_data_2 <- subset(student_data, student_data$Tmarks > 750 & student_data$class == "SYCS", select = c(rollno, name))
filtered_data_2
# 16. Sort the data in ascending order of total marks
sorted_data_2 <- student_data[order(student_data$Tmarks), ]
sorted_data_2
# 17. List the records where total marks are not entered.
missing_marks_students_2 <- subset(student_data, is.na(student_data$Tmarks))
missing_marks_students_2
# 18. Plot the scatter plot which shows relation between average marks and class.
plot(as.factor(student_data$class), student_data$Tmarks,
     xlab = "Class", ylab = "Total Marks",
     main = "Total Marks vs. Class")
