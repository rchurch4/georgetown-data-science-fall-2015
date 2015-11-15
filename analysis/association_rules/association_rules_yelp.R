################
# Association Rules for Yelp
# Author: Ravi Makhija
# Team: droptable
# Project 2
# Version 1.1
#
# Description:
# We explore the Yelp dataset using association rule mining.  
#
# File Dependencies:
#   'data/yelp_data.Rdata'
#
# How to run:
#    Source this script (no need to set wd beforehand if directory structure is
#    maintained as downloaded). Alternatively, set working directory to data
# 	 directory manually. 
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
# for setting the working directory manually. 

# Alternatively, set working directory to data directory manually. 

path_to_this_script <- parent.frame(2)$ofile 
setwd(gsub("analysis/association_rules/association_rules_yelp.R", 
           "data", 
           path_to_this_script))
rm(path_to_this_script) # clean up

################
# Load in data
################

load("tripadvisor_data.Rdata")
load("yelp_data.Rdata")

################
# Prep data for association rules
################

# Create a new data.frame for the data set we want to use association rules on. 
# We want to create categorical variables for this purpose. 

yelp_data_categorical <- data.frame(user_is_local = as.factor(yelp_data$user_is_local))

# Now, we bin some continuous variables and add to this new data set. 

###################
# user_review_length

# Explore data
summary(yelp_data$user_review_length)
hist(yelp_data$user_review_length)

# Bin and add to new data set:
# small: [0 to 300)
# medium: [300 to 1000)
# large: [1000 and up)
yelp_data_categorical$user_review_length <- cut2(x=yelp_data$user_review_length, cut=c(0, 300, 1000))

###################
# user_rating

# Explore data
table(yelp_data$user_rating)

# Bin and add to new data set:
# For the time being, we keep all five categories, since we have plenty of
# observations. 
yelp_data_categorical$user_rating <- as.factor(yelp_data$user_rating)

###################
# user_num_reviews

# Explore data
summary(yelp_data$user_num_reviews)
hist(yelp_data$user_num_reviews)

# Bin and add to new data set:
# low: [1 to 12)
# medium: [12 to 134)
# high: [134 and up)
yelp_data_categorical$user_num_reviews <- cut2(x=yelp_data$user_num_reviews, 
                                               cut=c(1, 12, 134))

###################
# user_review_date

# Explore data
table(substring(yelp_data$user_review_date, first=1, last=4))

# Bin and add to new data set:
# old: [2005, 2008]
# less_recent: [2009, 2012]
# recent: [2013, 2015]
yelp_data_categorical$user_review_time_period <- cut2(x=as.numeric(substring(yelp_data$user_review_date, first=1, last=4)), cut=c(2005, 2009, 2013))

###################
# Check out the new data set
head(yelp_data_categorical)

################
# Start association rules mining for Yelp
################

attach(yelp_data_categorical)

# Since a central question we are asking is whether or not local or non-local
# ratings are higher, we start association rule mining with the binary
# user_is_local on the right, to see if we can find any implications. We 
# adjust the minimum support and confidence levels to obtain the most 
# meaningful rule set. 

# A first look shows that the four rules returned all suggest that longer
# reviews may be associated with local reviewers. Rule 2 and 3 also 
# may inadvertently be suggesting that user ratings of 2 and 3 are associated
# with longer reviews --- something to keep in mind and consider exploring
# further. 

yelp_rules_1 <- apriori(yelp_data_categorical, 
                        parameter = list(minlen=1, supp=.01, conf=0.75),
                        appearance = list(rhs=c("user_is_local=FALSE", "user_is_local=TRUE"), default="lhs"),
                        control = list(verbose=F))
inspect(yelp_rules_1)
plot(yelp_rules_1)

# Bringing the confidence level down, we get many more rules. We can see that
# among the top 17 rules, all rules have ratings of at most 3. E.g. the lower
# half of ratings imply local reviews with the highest confidence. This is
# in accordance with the t-tests conducted, which showed local reviewer mean
# rating is less than that of non-local reviewers.   

yelp_rules_2 <- apriori(yelp_data_categorical, 
                        parameter = list(minlen=1, supp=.01, conf=0.70),
                        appearance = list(rhs=c("user_is_local=FALSE", "user_is_local=TRUE"), default="lhs"),
                        control = list(verbose=F))
inspect(yelp_rules_2)
plot(yelp_rules_2)

# Raising the minimum support, we see that a large user_review_length seems to 
# often imply a local reviewer. This includes two rules with support .06 and
# .08, higher than in the previous rule sets. 

yelp_rules_3 <- apriori(yelp_data_categorical, 
                        parameter = list(minlen=1, supp=.02, conf=0.70),
                        appearance = list(rhs=c("user_is_local=FALSE", "user_is_local=TRUE"), default="lhs"),
                        control = list(verbose=F))
inspect(yelp_rules_3)
plot(yelp_rules_3)

# It does not seem like the year provided any useful information here, so we
# also try mining rules without this variable. Doing this shows more clearly
# that longer reviews seem to imply local reviewers. 

yelp_rules_4 <- apriori(yelp_data_categorical[ , -5], 
                        parameter = list(minlen=1, supp=.01, conf=0.70),
                        appearance = list(rhs=c("user_is_local=FALSE", "user_is_local=TRUE"), default="lhs"),
                        control = list(verbose=F))
inspect(yelp_rules_4)
plot(yelp_rules_4)

# We use a third support level to look for the most frequent item sets overall. 
# We see here with rule 3 that user number of reviews in the medium category
# [12, 134) are commonly associated with local reviewers. 
yelp_rules_5 <- apriori(yelp_data_categorical, 
                        parameter = list(minlen=1, supp=.25, conf=0.1),
                        appearance = list(rhs=c("user_is_local=FALSE", "user_is_local=TRUE"), default="lhs"),
                        control = list(verbose=F))
inspect(yelp_rules_5)
plot(yelp_rules_5)