# 2017 Spring KAIST GCT564 Lecture 19 Exercises
# 20163204 Sanggyu Nam

## Exercise 1
library(igraph)
gMsg <- graph.formula(A++B, A-+C, A-+D, B++D, B++E, C-+B, C++D, E-+C)
plot(gMsg)

## Exercise 2
edges <- read.table("edgesdata3.txt", header = TRUE)
net <- graph.data.frame(edges)
V(net)[name == "CA"]$color <- "blue"
V(net)[name != "CA"]$color <- "red"
V(net)$size <- degree(net) / 10
E(net)$color <- ifelse(E(net)$spec == "X", "red",
                       ifelse(E(net)$spec == "Y", "blue", "gray"))
par(mai=c(0,0,1,0))
plot(net,
     main = "Organizational network example",
     layout = layout.auto,
     edge.arrow.size = 0.2,
     vertex.label.cex = 0.6,
     vertex.frame.color = "blue",
     vertex.label.font = 2,
     vertex.label.color = "black",
     vertex.label = V(net)$name
     )
