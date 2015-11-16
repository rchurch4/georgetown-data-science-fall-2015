# Nathan Hauke
# Drop Table - Teamname
# Project 2
# Classifiers
#
# This file shows the code, results and analysis of three different data driven predictive models
# https://cran.r-project.org/web/packages/caret/vignettes/caret.pdf was used as a source for the caret package

library(rpart)
library(lazy)
library(caret)
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
# Here the confusion matrix shows our classifier has only 56% accuracy; much worse than always guessing a user is local

# Naive Bayes
# Finally we attempt the classification task using a naive bayes classifier
# We use the caret package for 5-fold cross validation
# This time we usthe TripAdvisor data as our example:

model <- train(as.factor(user_is_local)~restaurant_overall_rating+
 			   restaurant_num_reviews+user_rating+
 			   user_num_reviews+user_review_length, 
 			   data=tripadvisor_data, 
 			   method="nb", 
 			   trControl=trainControl(method="cv",number=5), 
 			   metric="Accuracy")
 			   
# > model
# 100831 samples
     # 5 predictors
     # 2 classes: 'FALSE', 'TRUE' 

# No pre-processing
# Resampling: Cross-Validation (5 fold) 

# Summary of sample sizes: 80665, 80665, 80664, 80665, 80665 

# Resampling results across tuning parameters:

  # usekernel  Accuracy  Kappa   Accuracy SD  Kappa SD
  # FALSE      0.711     0.0481  0.00213      0.00604 
  # TRUE       0.723     0.0273  0.000657     0.00255 

# Tuning parameter 'fL' was held constant at a value of 0
# Accuracy was used to select the optimal model using  the largest value.
# The final values used for the model were fL = 0 and usekernel = TRUE.

# Now that we have this model, we use it to make our predictions
p <- predict(model, tripadvisor_data)

# We check the accuracy and the confusion matrix:
mean(p==tripadvisor_data$user_is_local)
# [1] 0.7236366

table(p,tripadvisor_data$user_is_local)
# p       FALSE  TRUE
#   FALSE 72292 27588
#   TRUE    278   673

# As in the parametric test, we can see that the abundance of non-local users dominate,
# but the model does correctly identify over 70% of the few reviews it marks as local.
# The overall accuracy is slightly better than the total percentage of non-local users (71.97%),
# which leaves open the possibility that the user ratings and other variables carry some predictive power.