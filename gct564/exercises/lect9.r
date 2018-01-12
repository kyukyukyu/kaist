# 2017 Spring KAIST GCT564 Lecture 9 Exercises
# 20163204 Sanggyu Nam

# Exercise 1
bp <- read.table(text = "
                 Subject  Standing  Supine
                 1  132 136
                 2  146 145
                 3  135 140
                 4  141 147
                 5  139 142
                 6  162 160
                 7  128 137
                 8  137 136
                 9  145 149
                 10 151 158
                 11 131 120
                 12 143 150", header = TRUE)

# 1 (a)
tt <- t.test(bp$Standing, bp$Supine, paired = TRUE, alternative = "two.sided")
a = 0.05; dfn = tt$parameter
t.crit = qt(a / 2, df = dfn)
t.cal = tt$statistic
# Since t.cal < 0 and t.cal < t.crit, we retain the null hypothesis.

# 1 (b)
# Assuming that glib.Rdata is in the working directory.
load("glib.Rdata")
x1=-5; x2=5; x <- seq(x1,x2,0.05)
tc = round(t.crit,3)
axisplot(x1,x2,tc,"t value")
fillpolygon(x1,tc,"cyan"); fillpolygon(-tc,x2,"cyan")
lines(x, dnorm(x))
t = round(t.cal,3)
text(t,0.15,paste("t =",t)); abline(v=t)

# Exercise 2
nos = matrix(c(15, 19, 13, 11, 18, 14, 12, 16, 17, 19,
               8, 11, 13, 10, 6, 7, 4, 9, 12, 2),
             byrow = TRUE,
             nrow = 2, dimnames = list(list("Females", "Males")))
nos.t.test = t.test(x = nos[1,], y = nos[2,], var.equal = TRUE, alternative = "two.sided")
paste("Since t.cal =", nos.t.test$statistic, "is larger than t.crit =",
      qt(1 - 0.05 / 2, nos.t.test$parameter),
      "we reject the null hypothesis.")

# Exercise 3
dt <- read.table("DRPScores.txt", header = TRUE)
attach(dt); head(dt)
table(Treatment)
dt.treated = dt[Treatment == "Treated", 2]
dt.control = dt[Treatment == "Control", 2]

# 3 (1)
m.treated = mean(dt.treated)
m.control = mean(dt.control)
m.treated - m.control

# 3 (2)
dt.test = t.test(x = dt.treated, y = dt.control, var.equal = TRUE, alternative = "two.sided")
paste("Since t.cal =", dt.test$statistic, "is larger than t.crit =",
      qt(1 - 0.05 / 2, dt.test$parameter),
      "we reject the null hypothesis.",
      "This means that there is a statistically significant difference between two groups.")
