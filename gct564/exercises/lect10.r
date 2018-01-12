# 2017 Spring KAIST GCT564 Lecture 10 Exercises
# 20163204 Sanggyu Nam

# Exercise 1
# 1 (a)
dat = matrix(c(16, 12, 9, 4,
               1, 4, 5, 14),
             nrow = 2, byrow = TRUE)
rownames(dat) <- c("For", "Against")
colnames(dat) <- c("Grades 1-4", "Grades 5-8", "High School", "College-University")
names(dimnames(dat)) <- c("Internet Censorship", "Level of Teaching")

# 1 (b)
ct = chisq.test(dat)
ct.dof = ct$parameter
chisq.cal = ct$statistic
chisq.crit = qchisq(1 - 0.05, ct.dof)
paste("Since chisq.cal =", chisq.cal, "is larger than",
      "chisq.crit =", chisq.crit, "we reject the null hypothesis.",
      "This indicates that the teacher's views of Internet censorship varies with the level of education")

# Exercise 2
#dat = matrix(c(45, 56, 35, 47), nrow = 2, byrow = TRUE,
#             dimnames = list(list("Favorable", "Unfavorable"), list("Week 1", "Week 2")))
p.test = prop.test(c(45, 56), c(45 + 35, 56 + 47), correct = FALSE)
paste("Since p-value =", p.test$p.value, "is larger than 0.05, we reject the null hypothesis.")
