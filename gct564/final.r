setwd("~/kaist/gct564/final/")

## Problem 1
library(car)
library(MVN)
head(Soils)
hzTest(Soils[, c(6, 14)], qqplot = TRUE)

Y <- cbind(Soils$pH, Soils$Conduc)
fit <- manova(Y ~ Soils$Block + Soils$Contour)
summary(fit, test = "Wilks")

## Problem 2
usdat <- read.csv("USCityCrime1975.csv", header = TRUE)
library(NbClust)
library(stats)
dat <- usdat[, -1]
NbClust(data = dat, distance = "euclidean", method = "complete")
ds <- dist(dat, method = "euclidean")
hcst <- hclust(ds, method = "complete")
plot(hcst, labels = usdat[, 1], cex = 0.8)

## Problem 3
library(psych)
ffdat <- read.csv("FastFoodSurvey.csv", header = TRUE)
fit <- fa(ffdat, nfactors = 3, rotate = "varimax", fm = "ml")
fit$communality

## Problem 4
scree(attitude, factors = FALSE, pc = TRUE)
pc <- principal(attitude, rotate = "none")
pc$loadings

## Problem 5
library(ca)
pc <- principal(smoke, nfactors = 3)
pc$values

## Problem 6
library(rpart)
dat <- subset(airquality, !is.na(Ozone))
ozoneRank <- order(dat$Ozone)
fit <- rpart(Ozone ~ Solar.R + Wind + Temp,
             data = subset(airquality, !is.na(Ozone)),
             method = "anova",
             control = rpart.control(minsplit = 10))
library(grid); library(partykit)
plot(as.party(fit), tp_args = list(id = FALSE))

library(party)
out.tree <- ctree(Ozone ~ Solar.R + Wind + Temp, data = subset(airquality, !is.na(Ozone)))
plot(out.tree)

## Problem 7

## Problem 8
library(igraphdata)
data(kite)
kt <- cluster_fast_greedy(kite)
sizes(kt)
plot_dendrogram(kt)

## Problem 9
library(bnlearn)
data(asia)
bnh <- hc(asia, score = "bic")
bnfit <- bn.fit(bnh, data = asia, method = "bayes")
bnfit$X
attach(asia)
cpquery(bnfit, event = (T == "yes"), (A == "yes" & S == "no"), method = "ls", n = 10^7)
cpquery(bnfit, event = (L == "yes"), (A == "yes" & S == "no"), method = "ls", n = 10^7)
cpquery(bnfit, event = (B == "yes"), (A == "yes" & S == "no"), method = "ls", n = 10^7)
