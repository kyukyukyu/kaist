# 2017 Spring KAIST GCT564 Lecture 12 Exercises
# 20163204 Sanggyu Nam

# Exercise 1
feeds = matrix(c(1.00, 6.50, 4.50, 2.00, 8.50,
                 1.50, 4.00, 3.50, 1.50, 5.00,
                 11.00, 6.50, 4.50, 7.50, 9.00),
               ncol = 3)
colnames(feeds) <- c("Less Than High School", "High Graduate", "College Graduate")
feeds.df <- data.frame(feeds = as.vector(feeds),
                       edulevel = gl(n = 3, k = 5, labels = colnames(feeds)))

# (a) Testing the null hypothesis.
shapiro.test(feeds)$p.value
# Since p-value is higher than 0.05,
# we can say that the length of breast-feeds has normality
# and we should use Bartlett's test.
bartlett.test(as.vector(feeds), gl(3, 5, labels = colnames(feeds)))
# Since p-value is higher than 0.05, we retain the null hypothesis
# and we can say that the length of breast-feeds has homogeneity.
oneway.test(feeds ~ edulevel, data = feeds.df)
# Since p-value is less than 0.05, we reject the null hypothesis that the means of the length of breast-feeds are the same.

# (b) Drawing density plots for the three groups with mean lines.
colors <- c("blue", "red", "green")
plot(0, 0, xlab = "Length of Breast-Feeding (month)", ylab = "Density",
    xlim = c(-5, 15), ylim = c(0.00, 0.20), type = "l")
for (i in 1:3) {
  f <- feeds[, i]
  m <- mean(f)
  d <- density(f)
  c <- colors[i]
  lines(d, col = c)
  abline(v = m, col = c)
}
legend("topright", legend = colnames(feeds), col = colors, lty = 1, bty = "n")

# Exercise 2
revenue <- matrix(c(15, 22, 18, 23, 23, 12, 26, 19, 15, 14, 14, 21,
                    18, 25, 22, 15, 15, 15, 12, 17, 14, 18, 22, 23,
                    22, 15, 15, 14, 26, 11, 23, 15, 18, 10, 19, 11,
                    23, 15, 19, 17, 18, 10, 15, 20, 19, 12, 17, 18,
                    24, 14, 21, 18, 14, 8, 18, 10, 20, 23, 11, 14),
                  nrow = 12, dimnames = list(month.name, sapply(1:5, function (x) paste("Year", x))))
revenue.df <- data.frame(month = gl(12, 1, len = length(revenue), labels = rownames(revenue)),
                         year = gl(5, 12, labels = colnames(revenue)),
                         rev = as.vector(revenue))
revenue.df$month = factor(revenue.df$month, rownames(revenue))
revenue.df$year = factor(revenue.df$year, colnames(revenue))

# (a) Testing the null hypothesis that the means of revenue evaluated according to the months and years are equal.
shapiro.test(revenue.df$rev)$p.value
# Since p-value is higher than 0.05,
# we can say that the revenue has normality
# and we should use Bartlett's test.
bartlett.test(rev ~ month, data = revenue.df)
bartlett.test(rev ~ year, data = revenue.df)
# We retain the null hypothesis since the p-values for both tests are larger than 0.05.
# This means that there is homogeneity for the variances among the months and years.
oneway.test(rev ~ month, data = revenue.df)
oneway.test(rev ~ year, data = revenue.df)
# We retain the null hypothesis since the p-values for both tests are larger than 0.05.
# This means that there is no significant difference among the means of revenue evaluated according to the months and years.

# (b) Drawing boxplots for Revenue ~ Months and Revenue ~ Year.
par(mfrow = c(2, 1))
boxplot(rev ~ month, data = revenue.df, xlab = "Months", ylab = "Revenue", col = rainbow(12, s = 0.3), las = 2)
boxplot(rev ~ year, data = revenue.df, xlab = "Years", ylab = "Revenue", col = rainbow(5, s = 0.7))

# Exercise 3
# Assumes that the data is stored as a file named fastfood3.csv in the working directory.
df3 = read.csv("fastfood3.csv")
attach(df3); df3

sales = c(t(as.matrix(df3)))
df3.new = data.frame(region = gl(2, length(sales) / 2, labels = c("East", "West")),
                     item = gl(3, 1, length(sales), labels = colnames(df3)),
                     sales = sales)
shapiro.test(df3.new$sales)
# Since p-value is greater than 0.05, the sales volume has normality.
# Therefore, we have to use Bartlett's test to test if there is a statistically significant difference among variances.

# (a) At 0.05 level of significance, test whether the mean sales volume for the new menu items are all equal.
bartlett.test(sales ~ item, data = df3.new)
# Since the p-value is greater than 0.05, we can say that there is homogeneity in the variances of sales.
# Therefore, we should conduct ANOVA.
oneway.test(sales ~ item, data = df3.new)
# We reject the null hypothesis that the mean sales volume for the new menu items are all equal.

# (b) Decide also whether the mean sales volume of the two coastal regions differs.
bartlett.test(sales ~ region, data = df3.new)
# Since the p-value is greater than 0.05, we can say that there is homogeneity in the variances of sales.
# Therefore, we can conduct ANOVA.
oneway.test(sales ~ region, data = df3.new)
# We reject the null hypothesis that the mean sales volume of the two coastal regions are equal.

# (c) Is there a interaction between the menu item and coast location?
summary(aov(sales ~ item * region, data = df3.new))
# The interaction between the menu item and coast location is statistically significant.