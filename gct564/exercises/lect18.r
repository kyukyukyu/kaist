# 2017 Spring KAIST GCT564 Lecture 18 Exercises
# 20163204 Sanggyu Nam

## Exercise 1
web = "http://www.rd.com/true-stories/inspiring/inspirational-quotes-for-mornings/1/"
library(XML); library(RCurl)
htm <- getURL(web); doc = htmlParse(htm, asText = TRUE)

ptx <- xpathSApply(doc, "//p", xmlValue)
star <- paste(ptx, collapse = "\\n")

# Load the text data as a corpus
library(NLP); library(tm)
corp <- Corpus(VectorSource(star))
# Data cleaning
corp = tm_map(corp, removePunctuation)
corp = tm_map(corp, tolower)
corp = tm_map(corp, removeNumbers)
corp = tm_map(corp, removeWords, stopwords("english"))
corp = tm_map(corp, PlainTextDocument)

# Build a term-document matrix
dtm <- DocumentTermMatrix(corp)
Freq <- sort(colSums(as.matrix(dtm)), decreasing = TRUE)
wf <- data.frame(Word = names(Freq), Freq = Freq)

## (1) Generate the word cloud.
library(RColorBrewer); library(wordcloud)
wordcloud(words = wf$Word, freq = wf$Freq, min.freq = 2,
          random.order = FALSE, rot.per = 0.35,
          colors = brewer.pal(8, "Dark2"))

## (2) Plot word frequencies (min.freq = 2)
library(ggplot2)
ggplot(subset(wf, Freq > 2), aes(Word, Freq)) +
  geom_bar(stat = "identity", fill = "green") + theme_bw() +
  theme(axis.text.x = element_text(angle = 0, hjust = 1)) + coord_flip()
