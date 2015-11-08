################
# Parametric Analyses
# Author: Ravi Makhija
#
# Description:
# Parametric tests conducted on review data, including logistic regression and
# t-test. 
# 
# File Dependencies:
#   'data/tripadvisor_data.Rdata'
#   'data/yelp_data.Rdata'
#
# References
#   1) Set working directory to the file path of a script:
#      http://stackoverflow.com/questions/13672720/r-command-for-setting-working-directory-to-source-file-location

require(data.table)
require(bit64)

################
# Set working directory to data directory.
# Makes use of location of this script to set data path relatively. 
################

path_to_this_script <- parent.frame(2)$ofile # must be sourced (rathern than run)
setwd(gsub("analysis/parametric_tests/parametric_tests.R", 
           "data", 
           path_to_this_script))
rm(path_to_this_script) # clean up

################
# Load in data
################

load("tripadvisor_data.Rdata")
load("yelp_data.Rdata")

################
# t-tests
################

# We begin by conducting t-tests for our hypotheses. 

# ------------------------
# Yelp Hypothesis: 
# H_0: The mean user rating for local and non-local reviewers on Yelp is the same.  
# H_a: The mean user rating for local and non-local reviewers on Yelp is not the same.  

# Check how many user reviews are local/non-local. 

table(yelp_data$user_is_local)

# A cursory look at the mean for local and non_local ratings.
# The mean for local yelp reviews is 3.723254, while the mean for non-local
# yelp reviews is 3.819291. 

yelp_data[ , mean(user_rating), by=user_is_local]

# Now, we conduct a t-test. We use an independent 2-group t-test. We use the
# default test in R, which is a Welch Two Sample t-test, which handles the case
# of unequal variances. 

# With a p-value of 2.2e-16, we can see that there is indeed a statistically
# significant difference between the local and non-local yelp user ratings, 
# at the .05 significance level. We can also see this reflected in the 
# confidence interval for the difference in ratings, which does not include 0.
# The data suggests the mean yelp rating for non-local reviews is higher than
# or local reviews. 

t.test(yelp_data[user_is_local == 1]$user_rating, 
       yelp_data[user_is_local == 0]$user_rating)

# ------------------------
# TripAdvisor Hypothesis: 
# H_0: The mean user rating for local and non-local reviewers on TripAdvisor is the same.  
# H_a: The mean user rating for local and non-local reviewers on TripAdvisor is not the same.  

# Check how many user reviews are local/non-local. 

table(tripadvisor_data$user_is_local)

# A cursory look at the mean for local and non_local ratings.
# The mean for local TripAdvisor reviews is 4.222591, while the mean for 
# non-local TripAdvisor reviews is 4.243421. 

tripadvisor_data[ , mean(user_rating), by=user_is_local]

# Now, we conduct a t-test. We use an independent 2-group t-test. We use the
# default test in R, which is a Welch Two Sample t-test, which handles the case
# of unequal variances. 

# With a p-value of 0.0001664, we can see that there is indeed a statistically
# significant difference between the local and non-local yelp user ratings, 
# at the .05 significance level. We can also see this reflected in the 
# confidence interval for the difference in ratings, which does not include 0.
# The data suggests the mean TripAdvisor rating for non-local reviews is higher 
# than for local reviews, as was the case for Yelp reviews. 

t.test(tripadvisor_data[user_is_local == TRUE]$user_rating, 
       tripadvisor_data[user_is_local == FALSE]$user_rating)

################
# Logistic Regression
################

# Next, we try a logistic regression model, to try and predict user_is_local
# using the other variables in the data set. We fit two models, one for each
# website. 

# We assume the usual normal error logistic regression model. 

# ------------------------
# Yelp



# ------------------------
# TripAdvisor









