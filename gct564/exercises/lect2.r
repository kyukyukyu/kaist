# 2017 Spring KAIST GCT564 Lecture 2 Exercises
# 20163204 Sanggyu Nam

# Exercise 1 (1)
library(MASS)
attach(Animals)
log_brain = log(brain)
log_body = log(body)
plot(log_brain, log_body)
text(log_brain, log_body, labels = row.names(Animals), pos = 4)
detach(Animals)

# Exercise 1 (2)
library(ggplot2)
attach(Animals)
ggplot(Animals, aes(log(brain), log(body), label = row.names(Animals))) +
  geom_point() + geom_label(aes(vjust = "middle", hjust = "left"))
detach(Animals)

# Exercise 2
library(ggplot2)
attach(iris)
ggplot(iris, aes(x = Sepal.Length, fill = Species)) +
  geom_histogram(color = "black") +
  facet_grid(Species ~ .)
detach(iris)

# Exercise 3
library(ggplot2)
attach(airquality)
ggplot(airquality, aes(x = Day, y = Ozone, color = factor(Month), size = Wind)) +
  geom_point() +
  scale_x_continuous(breaks = seq(1, 31, 5))
detach(airquality)