# data_cleanliness_score_yelp.py
# Version 1
#
# Description:
# Script to check cleanliness of data. Assigns a score
# out of 100%. 	
#
# File Dependencies:
#   

import pandas as pd
import numpy as np

# Make score data frame index from features. 
score_index = [
'restaurant_name',
'restaurant_location',
'restaurant_overall_rating',
'restaurant_num_reviews',
'restaurant_url',
'restaurant_phone',
'restaurant_address',
'user_name',
'user_rating',
'user_review',
'user_location',
'user_num_reviews',
'user_review_date',
'restaurant_latitude',
'restaurant_longitude',
'user_latitude',
'user_longitude',
'user_restaurant_distance',
'user_is_local',    
'user_review_length',    
'mean_restaurant_rating_yelp',
'mean_restaurant_rating_yelp_local',
'mean_restaurant_rating_yelp_local'
]

score_categories = [
'missing_values', # proportion of values DON'T have missing values (importance not too high)
'realistic_values', # proportion of values that are realistic (importance high)
'correct_data_type', # ensure column is the correct data type
'outliers', # 1 - (proportion of values that are outliers)
'sufficient_sample_size' # ensure some minimum number of observations are available for analysis
]

# Create score dataframe
score_df = pd.DataFrame(np.NaN, index = score_index, columns=score_categories)

print score_df
#print len(score_df)



