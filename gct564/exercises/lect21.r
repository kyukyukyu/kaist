# 2017 Spring KAIST GCT564 Lecture 21 Exercises
# 20163204 Sanggyu Nam

## Exercise 1
library(bnlearn)
bnh <- hc(asia, score = "bic")
bnfit <- bn.fit(bnh, data = asia, method = "bayes")

# (1) Extract the DAG, nodes and arcs of the bnh object.
edges <- arcs(bnh); vertices <- nodes(bnh)
net <- graph.data.frame(edges, directed = TRUE, vertices = vertices)
net

# (2) Compute the conditional probability distributions of X node and plot it
# with barchart.
bnfit$X
bn.fit.barchart(bnfit$X,
                main = "Chest X-Ray Against Tuberculosis Versus Lung Cancer/Bronchitis",
                xlab = "Pr(X|E)", ylab = "")

# (3) Patient has recently visited Asia and does not smoke. Which is most likely?
#     a) the patient is more likely to have tuberculosis then anything else.
#     b) the chance that the patient has lung cancer is higher than he/she having tuberculosis
#     c) the patient is more likely to have bronchitis then anything else
#     d) the chance that the patient has tuberculosis is higher than he/she having bronchitis
cpquery(bnfit, T == "yes", (A == "yes" & S == "no"), n = 10^7)
cpquery(bnfit, L == "yes", (A == "yes" & S == "no"), n = 10^7)
cpquery(bnfit, B == "yes", (A == "yes" & S == "no"), n = 10^7)
# Hence, c is most likely.

# (4) Plot the DAG for hc object.
library(igraph)
plot(net, vertex.label = V(net)$name, vertex.size = 30,
     edge.arrow.size = 0.3, vertex.color = "cornsilk")