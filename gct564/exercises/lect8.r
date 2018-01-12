# 2017 Spring KAIST GCT564 Lecture 8 Exercises
# 20163204 Sanggyu Nam

# Exercise 1
X <- c(3.3, 2.9, 2.5, 4.0, 2.8, 2.5, 3.7, 3.8, 3.5, 2.7, 2.6, 4.0)
Y <- c(2.7, 2.5, 1.9, 3.3, 2.7, 2.2, 3.1, 4.0, 2.9, 2.0, 3.1, 3.2)
m = lm(Y ~ X)

# 1 (a)
intercept <- as.numeric(m$coefficients[1])
slope <- as.numeric(m$coefficients[2])

# 1 (b)
plot(x = X, y = Y)
abline(intercept, slope, col = "blue")

# 1 (c)
answer <- slope * 3.0 + intercept

# 1 (d)
coeff.det <- summary(m)$r.squared
coeff.nondet <- 1 - coeff.det
# The value around 0.6 means that the linear regression is neither good or bad.

# 1 (e)
rtest = cor.test(X, Y)
a = 0.05; dof = rtest$parameter; t.crit = qt(1 - a / 2, dof)
t.cal = rtest$statistic
cat("t.cal =", t.cal, "t.crit =", t.crit, "\n")
# Since t.cal > t.crit, we can reject the null hypothesis and say that there
# is a strong correlation between high school score and college score.

# 1 (f)
plot(x = X, y = Y)
abline(intercept, slope, col = "blue")
pre <- predict(m)
segments(X, Y, y1 = pre)

# Exercise 2
library(ISwR)
group = juul2[juul2$age > 25,]

# 2 (a)
m = lm(sqrt(group$igf1) ~ group$age)
summary(m)

# 2 (b)
m2 = lm(sqrt(group$igf1) ~ group$age + group$weight + group$height)
anova(m2)

# 2 (c): Any of factors is not analyzed to be significant. It's because we are
# working on the group of people whose age is over 25.
