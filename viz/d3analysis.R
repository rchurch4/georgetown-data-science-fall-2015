# Supplementary analyses and data preparation for brainstorming and prepping d3/js visualizations. 

# Analytics Project 3
# Author: Ravi Makhija
# Team: Droptable
# Version: 1.2

require(data.table)

# Set the working directory to data directory. 
#setwd("please_change_me/data")
setwd("C:/Users/Ravi/Docs/Geekazoid/Courses/Intro_to_Analytics/Project/Git/georgetown-data-science-fall-2015/data")

# Load data
load("tripadvisor_data.Rdata")
load("yelp_data.Rdata")

################################
################################
# Analyses start below

################################
# Distribution of ratings for local vs. non-local
# Used for d3 bar charts

# yelp
setkey(yelp_data, user_is_local, user_rating)
# local
yelp_data[user_is_local==TRUE,.N/nrow(yelp_data[user_is_local==TRUE]),by=.(user_rating)]
# non-local
yelp_data[user_is_local==FALSE,.N/nrow(yelp_data[user_is_local==FALSE]),by=.(user_rating)]

# tripadvisor
setkey(tripadvisor_data, user_is_local, user_rating)
# local
tripadvisor_data[user_is_local==TRUE,.N/nrow(tripadvisor_data[user_is_local==TRUE]),by=.(user_rating)]
# non-local
tripadvisor_data[user_is_local==FALSE,.N/nrow(tripadvisor_data[user_is_local==FALSE]),by=.(user_rating)]

################################
# Annual ratings - local vs. non-local
# Used for d3 line graphs

# Basic Idea: If a pattern is consistent every year, we have a stronger argument for those patterns. 
# 			  E.g. less likely that they are due to chance. 

# YELP

# coerce dates to Date type, save features in a new data.table
yelp_data_new <- yelp_data[ , .(user_is_local, user_rating)]
yelp_data_new[ , user_review_date := .(as.Date(yelp_data$user_review_date))]
setkey(yelp_data_new)

# aggregate
yelp_annual_local <- yelp_data_new[ user_is_local == TRUE, .(.N, mean(user_rating)) , by=year(user_review_date)]
yelp_annual_nonlocal <- yelp_data_new[ user_is_local == FALSE, .(.N, mean(user_rating)) , by=year(user_review_date)]

setnames(yelp_annual_local, names(yelp_annual_local), c("year", "N", "mean_rating"))
setnames(yelp_annual_nonlocal, names(yelp_annual_nonlocal), c("year", "N", "mean_rating"))

yelp_annual_local[year >= 2010, .(year, mean_rating)]
yelp_annual_nonlocal[year >= 2010, .(year, mean_rating)]

write.csv(yelp_annual_local[year >= 2010, .(year, mean_rating)], file="yelp_annual_local.csv", row.names=FALSE)
write.csv(yelp_annual_nonlocal[year >= 2010, .(year, mean_rating)], file="yelp_annual_nonlocal.csv", row.names=FALSE)

# TRIPADVISOR

# coerce dates to Date type, save features in a new data.table
tripadvisor_data_new <- tripadvisor_data[ , .(user_is_local, user_rating)]
tripadvisor_data_new[ , user_review_date := .(as.Date(tripadvisor_data$user_review_date, format="%B %d, %Y"))]
setkey(tripadvisor_data_new)

# aggregate
tripadvisor_annual_local <- tripadvisor_data_new[ user_is_local == TRUE, .(.N, mean(user_rating)) , by=year(user_review_date)]
tripadvisor_annual_nonlocal <- tripadvisor_data_new[ user_is_local == FALSE, .(.N, mean(user_rating)) , by=year(user_review_date)]

setnames(tripadvisor_annual_local, names(tripadvisor_annual_local), c("year", "N", "mean_rating"))
setnames(tripadvisor_annual_nonlocal, names(tripadvisor_annual_nonlocal), c("year", "N", "mean_rating"))

tripadvisor_annual_local[year >= 2010, .(year, mean_rating)]
tripadvisor_annual_nonlocal[year >= 2010, .(year, mean_rating)]

write.csv(tripadvisor_annual_local[year >= 2010, .(year, mean_rating)], file="tripadvisor_annual_local.csv", row.names=FALSE)
write.csv(tripadvisor_annual_nonlocal[year >= 2010, .(year, mean_rating)], file="tripadvisor_annual_nonlocal.csv", row.names=FALSE)

################################
# Controlling for Restaurants - local vs. non-local mean ratings
# We were interested in seeing if locals/non-locals are prone to going to certain restaurants, and 
# the implications that may have on our results. But, this analysis didn't turn up anything worth
# including in a visualization. 

# prepare data for analysis

restaurant_nonlocal_N <- yelp_data[user_is_local == FALSE, .N , by=.(restaurant_name)]
restaurant_local_N <- yelp_data[user_is_local == TRUE, .N , by=.(restaurant_name)]
restaurant_total_N <- yelp_data[, .(.N, mean(user_rating)), by=.(restaurant_name)]

setnames(restaurant_nonlocal_N, names(restaurant_nonlocal_N), c("restaurant_name", "nonlocal_N"))
setnames(restaurant_local_N, names(restaurant_local_N), c("restaurant_name", "local_N"))
setnames(restaurant_total_N, names(restaurant_total_N), c("restaurant_name", "total_N", "overall_mean"))

setkey(restaurant_nonlocal_N, restaurant_name)
setkey(restaurant_local_N, restaurant_name)
setkey(restaurant_total_N, restaurant_name)

restaurant_all <- restaurant_nonlocal_N[restaurant_local_N[restaurant_total_N]] # joins

restaurant_all[ , c("proportion_local", "proportion_nonlocal") := .(local_N/total_N, nonlocal_N/total_N)] # calculate proportions

# remove NA function from here: 
# http://stackoverflow.com/questions/7235657/fastest-way-to-replace-nas-in-a-large-data-table
remove_NA_from_DT = function(DT) {
  for (i in names(DT))
    DT[is.na(get(i)),i:=0,with=FALSE]
}

remove_NA_from_DT(restaurant_all)
restaurant_all # check

# proportion for non_local & local, with minimum total_N of 200

setkey(restaurant_all, proportion_local)
tail(restaurant_all[total_N >= 200], 10) # local top 10
setkey(restaurant_all, proportion_nonlocal)
tail(restaurant_all[total_N >= 200], 10) # non-local top 10

# write csv

#write.csv(restaurant_all[ , .(restaurant_name, overall_mean, proportion_local, proportion_nonlocal)],
#          file="restaurant_proportion_local.csv",
#          row.names=FALSE)

################################
# Impact of changing radius
# Used in js map/radius visualization

#yelp
yelp_data_radius <- copy(yelp_data)
yelp_data_radius <- yelp_data_radius[ , .(user_rating, user_restaurant_distance)]

for (r in seq(10, 50, by=20)) {
  print(r)
  print(yelp_data_radius[user_restaurant_distance <= r, mean(user_rating)])
  print(yelp_data_radius[user_restaurant_distance <= r, .N])
  print(yelp_data_radius[user_restaurant_distance > r, mean(user_rating)])
  print("----")
}

r <- 1000
print(yelp_data_radius[user_restaurant_distance <= r, mean(user_rating)])
print(yelp_data_radius[user_restaurant_distance <= r, .N])
print(yelp_data_radius[user_restaurant_distance > r, mean(user_rating)])

# ta
tripadvisor_data_radius <- copy(tripadvisor_data)
tripadvisor_data_radius <- tripadvisor_data_radius[ , .(user_rating, user_restaurant_distance)]

for (r in seq(10, 50, by=20)) {
  print(r)
  print(tripadvisor_data_radius[user_restaurant_distance <= r, mean(user_rating)])
  print(tripadvisor_data_radius[user_restaurant_distance <= r, .N])
  print(tripadvisor_data_radius[user_restaurant_distance > r, mean(user_rating)])
  print("----")
}

r <- 1000
print(tripadvisor_data_radius[user_restaurant_distance <= r, mean(user_rating)])
print(tripadvisor_data_radius[user_restaurant_distance <= r, .N])
print(tripadvisor_data_radius[user_restaurant_distance > r, mean(user_rating)])


