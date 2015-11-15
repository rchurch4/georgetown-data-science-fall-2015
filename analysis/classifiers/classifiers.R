# Nathan Hauke
# Drop Table - Teamname
# Project 2
# Classifiers

library(rpart)
library(lazy)
library(naiveBayes)
load("yelp_data.Rdata")

# Decision Tree
# We try to construct a decision tree that will predict whether or not a user is local:
yelp.rpart <- rpart(user_is_local~restaurant_overall_rating+restaurant_num_reviews+user_rating+user_num_reviews+user_review_length, yelp_data, method="class")

# The result is a tree with a single root node, indicating that no split was found 
# which would improve the fit by a large enough margin to grow the tree.
# The result is the same for the TripAdvisor dataset.
# This indicates that rpart was unable to find individual parameters which would do better than always guessing
# local in the yelp case (61%), or non-local for TripAdvisor (72%)

# Lazy Learner 
# We attempt the same classification task using a lazy learner:
yelp.lazy <- lazy(user_is_local~restaurant_overall_rating+restaurant_num_reviews+user_rating+user_num_reviews+user_review_length, yelp_data)
yelp_pred.lazy <- predict(yelp.lazy, yelp_data[1:10000,])$h
table(yelp_pred.lazy>.5, yelp_data[1:10000, "user_is_local"])

#        FALSE TRUE
#  FALSE  1400  717
#  TRUE   1984 5899
#
# With an accuracy of 73% we seem to have succeeded on this small test subset...
# But we suspect this is overfitting and try again, this time withholding the test data from our model:
yelp.lazy <- lazy(user_is_local~restaurant_overall_rating+restaurant_num_reviews+user_rating+user_num_reviews+user_review_length, yelp_data, subset=100000:200000)
yelp_pred.lazy <- predict(yelp.lazy, yelp_data[1:10000,])$h
table(yelp_pred.lazy>.5, yelp_data[1:10000, "user_is_local"])

#        FALSE TRUE
#  FALSE  1403 2403
#  TRUE   1981 4213
#
# Here our classifier has only 56% accuracy; much worse than always guessing a user is local

# NaiveBayes
# Having failed twice, we try a new task with the naive bayes classifier.
# We will see if user location has any predictive power in determining user_rating
yelp.bayes <- naiveBayes(user_rating~restaurant_overall_rating+restaurant_num_reviews+user_restaurant_distance+user_num_reviews+user_review_length, yelp_data, subset=100000:200000)


