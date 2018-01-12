# 2017 Spring KAIST GCT564 Lecture 4 Exercises
# 20163204 Sanggyu Nam

# Exercise 1.a
a <- 100 * pnorm(23, mean = 26, sd = 2)

# Exercise 1.b
b1 <- 100 * pnorm(30, mean = 26, sd = 2)
b2 <- 100 - b1

# Exercise 1.c
c1 <- 100 * pnorm(18, mean = 26, sd = 2)
c2 = c1

# Exercise 2 (a)
# Assume that viszarea.R is in the working directory.
source("viszarea.R")
m = 10; s = 1.5
z1 = (8 - m) / s; z2 = (12 - m) / s
a = pnorm(z1) + (1 - pnorm(z2))

# Exercise 2 (b)
zCurve(-4, z1, 4)
fillpolygon(z2, 4, "cyan")
