# 2017 Spring KAIST GCT564 Lecture 17 Exercises
# 20163204 Sanggyu Nam

## Exercise 1
# (a) Compare the conditional tree models fitted to the titanic_train data
# against a simple binomial logistic regression model.
install.packages('titanic')
library(titanic)
tt <- na.omit(titanic_train[, -c(1, 4, 9, 11)])

# Simple binomial logistic regression model.
lrm <- glm(factor(Survived) ~ factor(Pclass) + factor(Sex) + Age + SibSp + Parch + Fare,
           data = tt, family = binomial(logit))

# Conditional tree models
library(party)
c.tree <- ctree(factor(Survived) ~ factor(Pclass) + factor(Sex) + Age + SibSp + Parch + Fare,
                data = tt)
c.tree
plot(c.tree, type = "simple")
