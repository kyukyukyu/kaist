# 2017 Spring KAIST GCT564 Lecture 7 Exercises
# 20163204 Sanggyu Nam

# Exercise 1
library(maps)
library(mapdata)
map('worldHires',
    c('UK', 'Ireland', 'Isle of Man','Isle of Wight', 'Wales:Anglesey'),
    xlim=c(-11,3), ylim=c(49,60.9))
map.cities(country = "UK", capitals = 1, col = "red")

# TA's tip: When using coordinates in R, we need to convert it into decimal
# numbers.

# Exercise 2
library(maps)
library(googleVis)
map('usa')
map("state", boundary = F, col = "blue", add = T)
text(x = state.center$x, y = state.center$y, state.abb, cex = 0.5)
points(Andrew$Long, Andrew$Lat)

# Exercise 3 (1)
# Assume that KOR_adm1.rds is in the working directory.
library(sp)
gadm <- readRDS("KOR_adm1.rds")
n <- length(gadm$NAME_1)
gadm$names <- as.factor(gadm$NAME_1)
spplot(gadm, "names", col.regions = rainbow(n), col = "black",
       main = "Administrative Divisions of South Korea")

# Exercise 3 (2)
# Assume that KOR_adm1.rds is in the working directory.
library(sp)
gadm <- readRDS("KOR_adm1.rds")
n <- length(gadm$NAME_1)
gadm$population <- c(
  3498529,      # Busan
  1591625,      # Chungbuk
  2096727,      # Chungnam
  2484557,      # Daegu
  1514370,      # Daejeon
  1550806,      # Gangwon
  1469214,      # Gwangju
  12716780,     # Gyeonggi
  2700398,      # Gyeongbuk
  3373871,      # Gyeongnam
  2943069,      # Incheon
  641597,       # Jeju
  1864791,      # Jeonbuk
  1903914,      # Jeonnam
  243048,       # Sejong
  9930616,      # Seoul
  1172304       # Ulsan
  )
spplot(gadm, "population", cuts = 8, col.regions = cm.colors(9),
       col = "black", main = "Regional Population (2016)",
       colorkey = list(height = 0.5))
