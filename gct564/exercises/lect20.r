# 2017 Spring KAIST GCT564 Lecture 20 Exercises
# 20163204 Sanggyu Nam

## Exercise 1
library(ergm)
fmh <- faux.magnolia.high
fit <- ergm(fmh ~ edges + nodematch("Race"))
# The log-odds of any tie occuring and Race match are:
plogis(coef(fit))
# Corresponding probability for the change in the number of ties with maching Race = 1 is:
x = sum(coef(fit))
p = exp(x) / (1 + exp(x))

# Simulation
sim <- simulate(fit)

# Visualization
plot.network(sim, displayisolates = FALSE, vertex.col = "Race")
races <- c("White", "Black", "Hispanic", "Asian", "Native American", "Other")
legend("topright", fill = factor(races), legend = races, cex = 0.8, bty = "n")

## Exercise 2
library(igraph)
dmt <- read.graph("drug_main.txt", format = "edgelist")
G <- as.undirected(dmt)
E(G)$color <- "red"
V(G)$size <- 6
L2 <- layout.fruchterman.reingold(G, niter = 500)
plot.igraph(G, layout = L2, vertex.label = NA)

cores <- coreness(G)
G2 <- induced.subgraph(G, as.vector(which(cores > 1)))
E(G2)$color <- "red"
V(G2)$size <- 6
L2_ <- layout.fruchterman.reingold(G2, niter = 500)
plot.igraph(G2, layout = L2_, vertex.label = NA)
