################
# Association Rules for TripAdvisor
# Author: Ravi Makhija
# Version 1.1
#
# Description:
# We explore the TripAdvisor dataset using association rule mining. 
# 
# File Dependencies:
#   'data/tripadvisor_data.Rdata'
#
# How to run:
#    Source this script (no need to set wd beforehand if directory structure is
#    maintained as downloaded).
#
# References
#   1) Set working directory to the file path of a script:
#      http://stackoverflow.com/questions/13672720/r-command-for-setting-working-directory-to-source-file-location
#   2) Tutorial on association rules in R:
#      http://www.rdatamining.com/examples/association-rules
#   3) Renaming levels of a factor:
#      http://www.cookbook-r.com/Manipulating_data/Renaming_levels_of_a_factor/
#   4) Installing package from a source file:
#      https://cran.r-project.org/web/packages/arules/index.html

require("arules")   # version 2.2 is needed, which required installing from source
require("arulesViz")
require("Hmisc")
require("data.table")
require("plyr")

################
# Set working directory to data directory.
# Makes use of location of this script to set data path relatively. 
################

# Script must be sourced (rather than run.) this is a convenience so that the 
# working directory will point to the data using a relative path, without need 
# for setting the working directory manually. This assumes directory structure
# was maintained.

path_to_this_script <- parent.frame(2)$ofile 
setwd(gsub("analysis/association_rules/association_rules_tripadvisor.R", 
           "data", 
           path_to_this_script))
rm(path_to_this_script) # clean up

################
# Load in data
################

load("tripadvisor_data.Rdata")

################
# Prep data for association rules
################

# Create a new data.frame for the data set we want to use association rules on. 
# We want to create categorical variables for this purpose. 

tripadvisor_data_categorical <- data.frame(user_is_local = as.factor(tripadvisor_data$user_is_local))

# Now, we bin some continuous variables and add to this new data set. 

###################
# user_review_length
# We omit this for TripAdvisor, since the data is incomplete with some of the
# reviews being cut off (e.g. they end with the word "More").

###################
# user_rating

# Explore data
table(tripadvisor_data$user_rating)

# Bin and add to new data set:
# For the time being, we keep all five categories:
tripadvisor_data_categorical$user_rating <- as.factor(tripadvisor_data$user_rating)

###################
# user_num_reviews

# Explore data
summary(tripadvisor_data$user_num_reviews)
hist(tripadvisor_data$user_num_reviews)

# Bin and add to new data set:
# low: [1 to 16)
# medium: [16 to 93)
# high: [83 and up)
tripadvisor_data_categorical$user_num_reviews <- cut2(x=tripadvisor_data$user_num_reviews, 
                                                      cut=c(1, 16, 83))

###################
# Check out the new data set
head(tripadvisor_data_categorical)

################
# Start association rules mining for tripadvisor
################

attach(tripadvisor_data_categorical)

# Since a central question we are asking is whether or not local or non_local
# ratings are higher, we start association rule mining with the binary
# user_is_local on the right, to see if we can find any implications. We 
# adjust the minimum support and confidence levels to obtain the most 
# meaningful rule set. Just as we did for Yelp. 

# A first look shows us that  the higher user ratings 4 and 5 are associated
# with non_local reviews with a higher confidence then with local reviews.

tripadvisor_rules_1 <- apriori(tripadvisor_data_categorical, 
                               parameter = list(minlen=1, supp=.01, conf=.5),
                               appearance = list(rhs=c("user_is_local=FALSE", "user_is_local=TRUE"), default="lhs"),
                               control = list(verbose=F))
inspect(tripadvisor_rules_1)
plot(tripadvisor_rules_1)

# Narrowing down by increasing the minimum support shows again that higher
# ratings are associated with non_local reviewers. Of course, the non_local
# reviews are being prioritized with a higher support, due to the class
# imbalance with TripAdvisor data being in favor of non_local. 

tripadvisor_rules_2 <- apriori(tripadvisor_data_categorical, 
                               parameter = list(minlen=1, supp=.2, conf=.5),
                               appearance = list(rhs=c("user_is_local=FALSE", "user_is_local=TRUE"), default="lhs"),
                               control = list(verbose=F))
inspect(tripadvisor_rules_2)
plot(tripadvisor_rules_2)

# Bringing the support level down to .1, but minimum confidence up to .7, we
# see again that higher ratings imply non_local reviews first. We also see that
# reviewers that have at least 16 reviews on TripAdvisor seem to also imply
# non_local reviews (as opposed to those who have very few reviews).

tripadvisor_rules_3 <- apriori(tripadvisor_data_categorical, 
                               parameter = list(minlen=1, supp=.1, conf=.7),
                               appearance = list(rhs=c("user_is_local=FALSE", "user_is_local=TRUE"), default="lhs"),
                               control = list(verbose=F))
inspect(tripadvisor_rules_3)
plot(tripadvisor_rules_3)