# 2017 Spring KAIST GCT564 Lecture 13 Exercises
# 20163204 Sanggyu Nam

## Exercise 1
# (1) Input Baumann data from the car library
library(car)
attach(Baumann); head(Baumann)
table(group)

# (2) Conduct a one-way multivariate analysis of variance.
library(MVN)
hzTest(Baumann[, 4:6], qqplot = TRUE)   # Data are multivariate normal.
Y <- cbind(post.test.1, post.test.2, post.test.3)
fit <- manova(Y ~ group)
summary(fit, test = "Pillai")

tapply(post.test.1, group, mean)
tapply(post.test.2, group, mean)
tapply(post.test.3, group, mean)

# (3) Explain the results.
# The groups differ across all three dependent variables simultaneously.

## Exercise 2
# (1) Input Soils data from the car library
data("Soils", package = "car")
head(Soils)
table(Soils$Contour)
table(Soils$Block)

# (2) Compute means of independent variables over Blocks and Contours
aggregate(Soils$pH, list(Block = Soils$Block, Contour = Soils$Contour), mean)
aggregate(Soils$Dens, list(Block = Soils$Block, Contour = Soils$Contour), mean)
aggregate(Soils$Conduc, list(Block = Soils$Block, Contour = Soils$Contour), mean)

# (3) Conduct a factorial multivariate analysis of variance.
# Since Contour and Block are already factorized, we don't have to factorize them here.
y = cbind(Soils$pH, Soils$Dens, Soils$Conduc)
fit = manova(y ~ Soils$Block * Soils$Contour)
summary(fit, test = "Pillai")

# (4) Explain the MANOVA results
# The block variable rejects the null hypothesis and thus is significant.
# The contour is not significant.
# The interaction between block and contour is also not statistically significant.