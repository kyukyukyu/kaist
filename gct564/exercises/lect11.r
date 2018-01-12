# 2017 Spring KAIST GCT564 Lecture 11 Exercises
# 20163204 Sanggyu Nam

# Exercise 1
data(womensrole, package="HSAUR3")
head(womensrole)

# 1 (a)
resp = cbind(womensrole$agree, womensrole$disagree)
out1 = glm(resp ~ factor(womensrole$gender) + womensrole$education,
           family = binomial(logit), data = womensrole)
summary(out1)
# P-value for Female is bigger than 0.05, which means that the respondent's
# gender is apparently unimportant.
# In contrast, the p-value for education is much smaller than 0.05, which
# means that education has a significant part to play in predicting whether
# a respondent will agree with the statement read to them.

# 1 (b)
agreeRatio = womensrole$agree / (womensrole$agree + womensrole$disagree)
rowsMale <- womensrole$gender == "Male"
plot(agreeRatio ~ education, data = womensrole)
lines(womensrole$education[rowsMale], out1$fitted[rowsMale],
      type = "l", col = "blue")
lines(womensrole$education[!rowsMale], out1$fitted[!rowsMale],
      type = "l", col = "red")
legend("topright", c("Male", "Female"), col = c("blue", "red"), lty = 1)

# Exercise 2
snoring <- matrix(c(24,35,21,30,1355,603,192,224), nc=2)
rownames(snoring) <- c("Never", "Occasional", "Nearly every night", "Every night")
colnames(snoring) <- c("Yes", "No")
names(dimnames(snoring)) <- list("Snoring", "Heart Disease")
snoringLevel = c(0, 2, 4, 5)

# Exercise 2 (a)
glm1 <- glm(snoring ~ snoringLevel, family = binomial(logit))
summary(glm1)
# Since p-value of snoring level < 0.05, snoring plays a significant role
# in predicting the heart disease.

# Exercise 2 (b)
oddsRatio = exp(coef(glm1)[2])
confint(glm1)

# Exercise 3
library(LOGIT)
data("edrelig")

# (1) Read data and look how many unique values
sapply(edrelig, function (x) length(unique(x)))

# (3) Logistic Regression Model
glm2 <- glm(religious ~ age + male + kids + factor(educlevel), family = binomial(logit),
        data = edrelig)
summary(glm2)
# Both age and educlevel predictors are statisically significant since their
# p-values are smaller than 0.05.
# However, male and kids are not statistically significant.

# (4) Odds Ratio
coeffs = coef(glm2)
cat("Subjects in a higher 5-year age group have a",
    100 * (exp(5 * coeffs["age"]) - 1),
    "% greater odds of being religious than those in the lower age division.")
cat("Males have a some",
    100 * (exp(coeffs["male"]) - 1),
    "% greater odds of being religious than females.")
cat("Study subjects having children have a",
    100 * (exp(coeffs["kids"]) - 1),
    "% higher odds of being religious than are those without children.")
cat("Those in the study whose highest degree is a BA have a",
    100 * (exp(coeffs["factor(educlevel)BA"]) - 1),
    "% greater odds of being nonreligious compared to those whose highest degree is an AA.")
cat("Those in the study whose highest degree is a MA/PhD have a",
    100 * (exp(coeffs["factor(educlevel)MA/PhD"]) - 1),
    "% greater odds of being nonreligious compared to those whose highest degree is an AA.")
