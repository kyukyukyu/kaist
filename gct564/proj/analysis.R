jin_Path = paste(c(path.expand("~"),"Dropbox/2017-1/GCT564/project/Data/chatroom_data_mingyu"), collapse='/')
han_path = "~/Dropbox/Project/Data/chatroom_data_seunghyun/"

setwd(han_path)
par(mfrow=c(1,1))

dat = fromJSON("chatroom.json")
str(dat)
individaulChatDat = dat[dat$pop == 2, ]
groupChatDat = dat[dat$pop > 2, ]
str(groupChatDat)


library(jsonlite)
dat = fromJSON("chatroom.json")[3:9]; dat
#dat$activeness = as.factor(dat$activeness)
#dat$sex = as.factor(dat$sex)
str(dat)
kmin=3
kmax=47
wss <- sapply(kmin:kmax,
              function(k){kmeans(dat, k, nstart=10)$tot.withinss}); wss
plot(kmin:kmax, wss, type="b", pch=21, frame=FALSE, bg="blue",
     xlab="Number of clusters K",
     ylab="Total within-clusters sum of squares")
abline(v = 3, lty = 2)

kc <- kmeans(dat, centers = 8)
cluster = as.factor(kc$cluster)
library(ggplot2)
str(dat)
ggplot(dat, aes(M, avgCharLen, color=cluster)) +
  geom_point() + theme_bw()

# Factor Analysis
library(psych)
dat = fromJSON("chatroom.json")[c(3,4,5,7,8,9)];
str(dat)
f5 = fa(dat, rotate="none", fm="wls")
f5$e.values
barplot(f5$e.values, col=ifelse(f5$e.values >= 1.0, "cyan", "grey"),
         ylab="Eigenvalues", xlab="Factor Number")
abline(h=1, col="black", lty=2)

fit = fa(dat, nfactors=3, rotate="varimax", fm="ml")
fs = fit$loadings # loadings are sort of paramters in a regression area.
print(fs, cutoff=0.3)

fa.diagram(fit, cut=0.3, digits=3)

# Linear Regression
dat = fromJSON("chatroom.json"); str(dat)

#lm.intimacy = lm(dat$intimacy ~ dat$pop + dat$activePop +
#                   dat$M + dat$avgCharLen + dat$dynamics + dat$interval)

lm.intimacy = lm(dat$intimacy ~ dat$avgCharLen)
summary(lm.intimacy)
plot(dat$avgCharLen, dat$intimacy, xlab="AvgCharLen", ylab="Chatroom Intimacy", pch=19)
grid()

abline(a=10.4081, b=-0.2025, col="blue", lwd=2)
text(2, 45, "Regression line\nY = 14 + 3x")

# Decision Tree
group_dat = fromJSON("chatroom.json"); str(dat)
out.tree = ctree(group_dat$intimacy ~ group_dat$pop + group_dat$activePop + group_dat$M +
                   group_dat$avgCharLen + group_dat$dynamics + group_dat$interval)
out.tree
plot(out.tree)
