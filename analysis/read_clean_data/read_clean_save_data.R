################
# Script to read in and clean data to prepare for analyses. 
# Author: Ravi Makhija
# Version 2
#
# Description:
# Read in csv data files of cleaned data with extra features for DC. Creates 
# one data.table for Yelp and one data.table for TripAdvisor. Then, saves
# these data.tables into two .Rdata files for quick loading in the future. This
# last step is commented out since it only needed to be done once. 
# 
# A few features are also added for TripAdvisor. And, some faulty data is 
# omitted. Details are all in this script. 
# 
# File Dependencies:
#   Yelp DC data:
#   for X = 0:19:
#      data/yelp_dc_X_cleaned_features.csv
#   TripAdvisor data:
#   for X = 0:50:
#      data/Washington_DC_District_of_Columbia_review_listX_cleaned_features.csv

require(data.table)
require(bit64)

################
# Set working directory to data directory.
# Makes use of location of this script to set data path relatively. 
################

path_to_this_script <- parent.frame(2)$ofile # must be sourced (rathern than run)
setwd(gsub("analysis/read_data/read_data_csv.R", 
           "data", 
           path_to_this_script))

################
# Read in data for Yelp DC
################

# Read in all Yelp dc data. There are a small number of rows (254798-254726=72)
# that contained review data broken across multiple rows. Due to this being a
# very rare event, we omit these rows. 

yelp_column_data_types <- c("character", "numeric", "character", "character", "character", "numeric", "character", "character", "character", "numeric", "numeric", "character", "character", "numeric", "numeric", "numeric", "numeric", "numeric", "logical", "numeric", "numeric", "numeric", "numeric")

yelp_data <- data.frame()
for (i in 0:19){
  tryCatch(
{ 
  print(paste("reading yelp dc dataset", i))
  yelp_data <- rbind(yelp_data, read.csv(file=paste("yelp_dc_", i, "_cleaned_features.csv", sep=""), 
                                         header=TRUE, 
                                         stringsAsFactors = FALSE
  ))
},
error = function(e)
{ 
  warning(paste("there was an error in reading yelp dc dataset", i))
}
  )
}

# Take out the broken reviews. 

yelp_data <- yelp_data[!is.na(yelp_data$user_rating_mean_for_restaurant_yelp_non_local), ] 

# Coerce some data types manually. The broken reviews (e.g. ones split across
# multiple reviews had to be fixed) first, that is why these data types were
# not set from the beginning. (e.g. faulty string data had to be removed
# before creating the numeric variables.)

yelp_data$user_is_local <- as.logical(as.character(yelp_data$user_is_local))
yelp_data$restaurant_overall_rating <- as.numeric(yelp_data$restaurant_overall_rating)
yelp_data$user_num_reviews <- as.numeric(yelp_data$user_num_reviews)
yelp_data$user_rating <- as.numeric(yelp_data$user_rating)
yelp_data$restaurant_num_reviews <- as.numeric(yelp_data$restaurant_num_reviews)

# Make data.table and set key. 
yelp_data <- data.table(yelp_data)
setkey(yelp_data, restaurant_name)

################
# Read in data for TripAdvisor DC
################

# Read in all TripAdvisor DC data. 

tripadvisor_column_data_types <- c("numeric", "character", "character", "character", "numeric", "numeric", "character", "character", "character", "numeric", "numeric", "character", "character", "numeric", "numeric", "numeric", "numeric", "numeric", "logical", "numeric")

tripadvisor_data <- data.table()
for (i in 0:50){
  tryCatch(
    { 
      print(paste("reading tripadvisor dc dataset", i))
      tripadvisor_data <- rbind(tripadvisor_data, read.csv(paste("Washington_DC_District_of_Columbia_review_list", 5, "_cleaned_features.csv", sep=""), 
                                                           stringsAsFactors=FALSE, 
                                                           header=TRUE, 
                                                           colClasses = tripadvisor_column_data_types))
    },
    error = function(e)
    { 
      warning(paste("there was an error in reading tripadvisor dc dataset", i))
    }
  )
}

# Omit data that does not have a value for the user_is_local field. This occurs 
# more often in TripAdvisor than Yelp since there are many missing values or
# faulty data included for user_location. 

tripadvisor_data <- tripadvisor_data[tripadvisor_data$user_is_local != ""]

# Generate the mean user rating features. This was done for yelp in the
# first part of the project, but for TripAdvisor we do this now, creating the
# following three features:
#   user_rating_mean_for_restaurant_tripadvisor
#   user_rating_mean_for_restaurant_tripadvisor_local
#   user_rating_mean_for_restaurant_tripadvisor_non_local

setkey(tripadvisor_data, restaurant_name)
# user_rating_mean_for_restaurant_tripadvisor
tripadvisor_data[ , user_rating_mean_for_restaurant_tripadvisor := mean(user_rating), by=restaurant_name]
# user_rating_mean_for_restaurant_tripadvisor_local
tripadvisor_data_local_means <- tripadvisor_data[user_is_local == TRUE , mean(user_rating), by=restaurant_name]
names(tripadvisor_data_local_means) <- c("restaurant_name", "user_rating_mean_for_restaurant_tripadvisor_local")
tripadvisor_data <- tripadvisor_data[tripadvisor_data_local_means]
# user_rating_mean_for_restaurant_tripadvisor_non_local
tripadvisor_data_non_local_means <- tripadvisor_data[user_is_local == FALSE , mean(user_rating), by=restaurant_name]
names(tripadvisor_data_non_local_means) <- c("restaurant_name", "user_rating_mean_for_restaurant_tripadvisor_non_local")
tripadvisor_data <- tripadvisor_data[tripadvisor_data_non_local_means]
# Remove temp variables
rm(tripadvisor_data_local_means, 
   tripadvisor_data_non_local_means,
   i,
   path_to_this_script,
   yelp_column_data_types,
   tripadvisor_column_data_types)

################
# Save as Rdata files for quick loading in the future.
################

# Commented out since this was already done, and only needs to be saved once,
# unless changes are made. 

save(tripadvisor_data, file="tripadvisor_data.Rdata")
save(yelp_data, file="yelp_data.Rdata")

