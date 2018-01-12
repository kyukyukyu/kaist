# 2017 Spring KAIST GCT564 Lecture 16 Exercises
# 20163204 Sanggyu Nam

# Exercise 1
library(datasets)

# (1) Report determinant, Bartlett chi-square test, and KMO.
cor_attitude <- cor(attitude)
det_attitude <- det(cor_attitude)
library(psych)
cortest.bartlett(cor_attitude, n = nrow(attitude))
KMO(cor_attitude)

# (2) How many principal components have eigenvalues >1.0?
# Using the scree plot, conform the number of principal components.
pca_attitude <- principal(cor_attitude, rotate = "none")
sum(pca_attitude$values > 1.0, na.rm = TRUE)
scree(cor_attitude, factors = FALSE, pc = TRUE)
# It seems 2 is the proper number of components.

# (3) What are the principal component equations to generate the scores?
pca_attitude <- principal(cor_attitude, nfactors = 2, rotate = "none")
for (x in 1:2) {
  cat("y", x, " = ", sep = "")
  cat(paste(pca_attitude$loadings[, x], colnames(attitude), sep = " * "), sep = " + ")
  cat("\n")
}
