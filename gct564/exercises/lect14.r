# 2017 Spring KAIST GCT564 Lecture 14 Exercises
# 20163204 Sanggyu Nam

## Exercise 1
# (a) Perform kmeans clustering and plot the result.
library(HSAUR3)
dat <- toothpaste[, -c(1, 2, 5)]

# Determine the best number of clusters.
kmax = 8
wss <- sapply(1:kmax,
              function (k) { kmeans(dat, k, nstart = 10)$tot.withinss })
plot(1:kmax, wss, type = "b", pch = 21, frame = FALSE, bg = "blue",
     xlab = "# of clusters", ylab = "Total within-clusters sum of squares")
# We might conclude that 3 clusters would be indicated by this method.
kc <- kmeans(dat, 3, nstart = 10)

# (b) Draw a silhouette plot using the clusters obtained from kmeans analysis.
library(cluster)
pamd <- pam(dist(dat), 3)
sobj <- silhouette(pamd)
summary(sobj)

par(mar = c(5.1, 7, 2.5, 2))
plot(sobj, col = 2:4, names.arg = toothpaste$Study)

## Exercise 2
# (a) How would you know if your data exhibits enough clustering so that results
# from kmeans is actually meaningful?
# With Silhouette analysis.
# Before that, we should know the best number of clusters.
dat <- heptathlon[, -8]
library(NbClust)
NbClust(data = dat, distance = "euclidean", method = "complete")  # ...which is 3.

library(cluster)
ds <- dist(dat)
pamd <- pam(ds, 3)
sobj <- silhouette(pamd)
summary(sobj)
# Since average (i.e. mean) Silhouette width is larger than 0.4,
# we can say that the results from kmeans is actually meaningful.

# (b) Plot a cluster dendrogram.

hcst <- hclust(ds, method = "complete")
par(mfrow = c(1, 1))
plot(hcst, labels = rownames(heptathlon), cex = 0.8)
rect.hclust(hcst, 3)
