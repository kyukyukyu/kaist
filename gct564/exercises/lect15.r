# 2017 Spring KAIST GCT564 Lecture 15 Exercises
# 20163204 Sanggyu Nam

# Exercise 1
ff <- read.csv("FastFood.csv", header = TRUE)

# (1) Determine the number of factors.
library(nFactors)
corff <- cor(ff[, -1])
eig <- eigen(corff)
mod <- parallel(subject = nrow(ff), var = ncol(ff) - 1,
                model = "factors")
nsc <- nScree(x = eig$values, aparallel = mod$eigen$qevpea)
plotnScree(nsc, xlab = "Factors")
abline(h = 1, col = "black")
# The number of factor should be >= 3.

# (2) Conduct EFA using fm="ml" and rotation="varimax" arguments.
# Plot factor diagram and report EFA results.
library(psych)
efa <- fa(ff[, -1], nfactors = 3, rotate = "varimax", fm = "ml")
fa.diagram(efa, cut = 0.3, digits = 3)
fs <- efa$loadings
print(fs, cutoff = 0.3)

# (3) Cronbach's α is a measure of internal consistency of a questionnaire
# or test. It says how correlated the items are that are included in the scale.
# Compute Cronbach's reliability coefficient alpha.
library(psych)
alpha(corff)
