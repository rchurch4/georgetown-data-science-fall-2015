# Nathan Hauke
# Droptable-teamname
# Project 3
# Sentiment Analysis

# I adapted code from this site in training our sentiment classifier:
# http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/

# Description:
# Trains a sentiment analyzer using Naive Bayes Classification, and then evaluates the sentiment of all user reviews
# Compares the number of positive reviews for local and non-local users on yelp and TripAdvisor
# It may be necessary to download the movie reviews corpus locally from nltk before running this script

import csv
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk import word_tokenize

# Given a list of words, returns a dictionary with words as keys, each with a value of True
def word_feats(words):
    return dict([(word, True) for word in words])

# Get the id of all positive and negative movie review examples
negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

# Get all positive and negative reviews, and break them into the words they contain
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

# Use all positive and negative movie reviews as our training set
trainfeats = negfeats + posfeats

# There should be 2000 movie reviews in the training set
print 'train on %d movie reviews' % len(trainfeats)

# Train a classifier using the training set
classifier = NaiveBayesClassifier.train(trainfeats)


local = []
nonlocal = []
local_sentiment = []
nonlocal_sentiment = []
# Assumes you are running this file from its location in our github repository
# Change the path as necessary to point to the right location
with open("../../data/yelp_data.csv", 'rb') as data:
    count = 0
    reader = csv.DictReader(data)
    for row in reader:

        #Uncomment to print summary statistics every 10000 examples to track progress
        #count += 1
        #if count%10000 == 0:
            #print count
            #print len(local), len(nonlocal)
            #print local_sentiment.count('pos'), nonlocal_sentiment.count('pos')
            #print local_sentiment.count('pos') / float(len(local)),
            #print nonlocal_sentiment.count('pos')/ float(len(nonlocal))

        # Tokenize the review into words, and use our classifier to analyze the sentiment
        rev = row['user_review'].decode('utf-8')
        tokens = word_tokenize(rev)
        words = [word.encode('utf-8') for word in tokens]

        # sentiment will be one of 'pos', 'neg'
        sentiment = classifier.classify(word_feats(words))

        # Add the row and sentiment to either the local or nonlocal lists
        if row['user_is_local'] == 'TRUE':
            local.append(row)
            local_sentiment.append(sentiment)
        else:
            nonlocal.append(row)
            nonlocal_sentiment.append(sentiment)


# Repeat for TripAdvisor
talocal = []
tanonlocal = []
talocal_sentiment = []
tanonlocal_sentiment = []
with open("ta_data.csv", 'rb') as data:
    count = 0
    reader = csv.DictReader(data)
    for row in reader:
        
        #count += 1
        #if count%10000 == 0:
            #print count
            #print len(talocal), len(tanonlocal)
            #print talocal_sentiment.count('pos'), tanonlocal_sentiment.count('pos')
            #print talocal_sentiment.count('pos') / float(len(talocal)),
            #print tanonlocal_sentiment.count('pos')/ float(len(tanonlocal))
        
        rev = row['user_review'].decode('utf-8')
        tokens = word_tokenize(rev)
        words = [word.encode('utf-8') for word in tokens]
        sentiment = classifier.classify(word_feats(words))
        
        if row['user_is_local'] == 'TRUE':
            talocal.append(row)
            talocal_sentiment.append(sentiment)
        else:
            tanonlocal.append(row)
            tanonlocal_sentiment.append(sentiment)


