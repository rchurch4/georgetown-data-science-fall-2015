# data_cleanliness_score_yelp.py
# Version 1
#
# Description:
# Script to check cleanliness of data. Assigns a score
# out of 100%. 	
#
# File Dependencies:
#   

# List of yelp features:
#   restaurant_name
#   restaurant_location
#   restaurant_overall_rating
#   restaurant_num_reviews
#   restaurant_url
#   restaurant_phone
#   restaurant_address
#   user_name
#   user_rating
#   user_review
#   user_location
#   user_num_reviews
#   user_review_date

# List of Nominatim (geocode) features:
#   restaurant_latitude
#   restaurant_longitude
#   user_latitude
#   user_longitude   

# List of extra features:
#   user_restaurant_distance   
#   user_is_local    
#   user_review_length    
#   mean_restaurant_rating_yelp
#   mean_restaurant_rating_yelp_local
#   mean_restaurant_rating_yelp_local








''' Ideas:
# Description:
# 

# Things to Check:

# Check for reasonable values for numerical variables. 

# Check for reasonable values for categorical variables. (e.g. region should be local or non-local)

# Count missing values for each variable. 

# Look for outliers. 

# Trailing white spaces. 



###### idea: score each column in different categories, then take a weighted average based on importance of each column. 

# "column health"

# anohter idea: can assign a score based on sample_size for a desired type of analysis.
'''