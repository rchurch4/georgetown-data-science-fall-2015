# Nathan Hauke
# Droptable-teamname
# Project 3
# Word Frequency Analysis

# I followed the word cloud tutorial here in conducting this analysis:
# https://georeferenced.wordpress.com/2013/01/15/rwordcloud/

# Load the data
# yelp_data.Rdata is in our repository, use the correct full path below
# Replace yelp_data with tripadvisor_data for TripAdvisor analysis
load("yelp_data.Rdata")

# Get text of all the local / nonlocal reviews
local <- yelp_data[yelp_data[,"user_is_local"], "user_review"]
nonlocal <- yelp_data[!yelp_data[,"user_is_local"], "user_review"]

# Because our sample size is so large we use random subsets of size 5000 for this analysis
# We could have repeated this with all reviews if we had found anything worth examining further
sm_local <- sample(local, 5000)
sm_nonlocal <- sample(nonlocal, 5000)

# Combine all reviews into a single string
local_text <- paste(sm_local, collapse=" ")
nonlocal_text <- past(sm_nonlocal, collapse=" ")

# Create a Corpus with the text-mining package 'tm'
local_source <- VectorSource(local_text)
nonlocal_source <- VectorSource(nonlocal_text)

local_corpus <- Corpus(local_source)
nonlocal_corpus <- Corpus(nonlocal_source)

# Lowercase all letters, remove punctuation, whitespace, and stop words
local_corpus <- tm_map(local_corpus, tolower)
nonlocal_corpus <- tm_map(nonlocal_corpus, tolower)

local_corpus <- tm_map(local_corpus, removePunctuation)
nonlocal_corpus <- tm_map(nonlocal_corpus, removePunctuation)

local_corpus <- tm_map(local_corpus, stripWhitespace)
nonlocal_corpus <- tm_map(nonlocal_corpus, stripWhitespace)

local_corpus <- tm_map(local_corpus, removeWords, stopwords("english"))
nonlocal_corpus <- tm_map(nonlocal_corpus, removeWords, stopwords("english"))

# Create a sorted matrix of word frequencies
local_dtm <- DocumentTermMatrix(local_corpus)
nonlocal_dtm <- DocumentTermMatrix(nonlocal_corpus)

local_dtm <- as.matrix(local_dtm)
nonlocal_dtm <- as.matrix(nonlocal_dtm)

local_freq <- colSums(local_dtm)
nonlocal_freq <- colSums(nonlocal_dtm)

local_freq <- sort(local_frequency, decreasing=TRUE)
nonlocal_freq <- sort(nonlocal_frequency, decreasing=TRUE)

# Get just the words used in reviews
local_words <- names(local_freq)
nonlocal_words <- names(nonlocal_freq)

# Compare word frequencies:

head(local_freq)
head(nonlocal_freq)

local_freq[1:100]
nonlocal_freq[1:100] 

# Make wordclouds
wordcloud(local_words, local_freq, scale=c(8,.3),min.freq=2,max.words=100, random.order=F, rot.per=.15, colors=pal, vfont=c("sans serif","plain"))
wordcloud(nonlocal_words, nonlocal_freq, scale=c(8,.3),min.freq=2,max.words=100, random.order=F, rot.per=.15, colors=pal, vfont=c("sans serif","plain"))
