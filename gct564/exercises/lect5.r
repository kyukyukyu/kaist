# 2017 Spring KAIST GCT564 Lecture 5 Exercises
# 20163204 Sanggyu Nam

# Exercise 1
baseball = data.frame(team = c("Team A", "Team B", "Team C", "Team D", "Team E"),
                      batting = runif(25, .200, .400))
tapply(baseball$batting, baseball$team, mean)

# Exercise 2
boxplot(ToothGrowth$len ~ ToothGrowth$supp * ToothGrowth$dose, data = ToothGrowth,
        col = rainbow(2, 0.3),
        xlab = "Suppliment and Dose",
        notch = TRUE)

# Exercise 3
Titan = matrix(c(659, 146, 670, 192, 106, 296, 3, 20), nrow = 4, ncol = 2,
               byrow = TRUE,
               dimnames = list(c("PassMale", "CrewMale", "PassFemale", "CrewFemale"),
                               c("Died", "Survived")))
barplot(t(Titan), legend.text = TRUE, col = rainbow(2, 0.3))
