# data_preparation_trip_advisor.py
# Version 1
#
# Description:
# This script takes json files generated from
# scraping TRIP ADVISOR as an input, and in the end 
# delivers csvs that add features in and also
# do some data cleaning. Along the way,
# one more csv per json is created before the
# features are added. And, the geocode lookup
# table is also updated with any new locations
# in the input data files. Please also note that
# the city for the input data has to be defined
# by the user at run time (there will be a user
# prompt).
# 
# How to run:
# From the shell:
#   python data_preparation_trip_advisor.py
#
# Data preparation is done in three steps:
#   1) Converts json to csv, making each row of the
#      csv a unique review with restaurant info merged
#      in. 
#   2) Updates geocode lookup table with any new
#      geocodes required. 
#   3) Adds extra features to the data set and does
#      some data cleaning along the way. 
#
# Script Dependencies:
#   data_preparation_lib/json_to_csv_trip_advisor.py
#   data_preparation_lib/update_geocode_lookup_table.py
#   data_preparation_lib/clean_and_feature_generation_trip_advisor.py
#
# File Dependencies:
#   data/geocode_lookup_table.csv
#   data/Washington_DC_District_of_Columbia_basic_list.json
#   Files specified below in variable: 
#       input_data_path

import os
import sys
sys.path.insert(0, './data_preparation_lib') # from github folder root
from json_to_csv_trip_advisor import json_to_csv_trip_advisor
from update_geocode_lookup_table import update_geocode_lookup_table
from clean_and_feature_generation_trip_advisor import clean_and_feature_generation_trip_advisor
from change_extension_to_csv import change_extension_to_csv

################
# Set Data File Paths (USER-DEFINED)
# 
# Details: 
# input_file_paths should be given as a list of strings.
# 
# There is also an optional section to dynamically generate
# file names, if they are structured as 'root_#_ending'.
# 
# Example 1:
# # Manually specify input_file_paths
# input_file_paths = ['data/Washington_DC_District_of_Columbia_review_list0.json']
# 
# Example 2:
# # Dynamically generate input_file_paths
# make_input_file_paths = []
# start_num = 1 # user-defined
# end_num = 19 # user-defined
# for i in range(start_num, end_num + 1):
#     path_root = 'data/yelp_dc_' # user-defined
#     path_ending = '.csv' # user-defined
#     current_path = path_root + str(i) + path_ending
#     make_input_file_paths.append(current_path)
# input_file_paths = make_input_file_paths # user-defined
################

####
# Optional - dynamically generate input file paths

make_input_file_paths = []
start_num = 0 # user-defined
end_num = 0 # user-defined
for i in range(start_num, end_num + 1):
    path_root = 'data/Washington_DC_District_of_Columbia_review_list' # user-defined
    path_ending = '.json' # user-defined
    current_path = path_root + str(i) + path_ending
    make_input_file_paths.append(current_path)

####    
# Mandatory - Set paths
#input_file_paths = ['data/Washington_DC_District_of_Columbia_review_list40.json']
input_file_paths = make_input_file_paths

################
# Proceed with user prompt, then data preparation sequence
################

# Warn user about possibly overwriting csvs.
# Uses a loop to ensure valid input.
current_user_prompt = "\nThis script will overwrite any csv files with the same name. Therefore, you should make sure that input_file_paths is correct in the script before running. \n\nTo proceed, type either 'DC' or 'Nashville' depending on your input data. Otherwise, type 'q' to abort: "
while True:
    user_proceed_response = raw_input(current_user_prompt)
    if user_proceed_response.lower() != 'dc' and user_proceed_response.lower() != 'nashville' and user_proceed_response.lower() != 'q':
        current_user_prompt = '\nPlease enter one of "DC", "Nashville", or "q": '
    elif user_proceed_response.lower() == 'q':
        print 'Aborting data preparation sequence.'
        break
    elif user_proceed_response.lower() == 'dc' or user_proceed_response.lower() == 'nashville':
        if user_proceed_response.lower() == 'dc':
            my_restaurant_location = 'Washington, DC'
        elif user_proceed_response.lower() == 'nashville':
            my_restaurant_location = 'Nashville, TN'
        
        print '\nStarting data preparation sequence. \n'

        # json to csv conversion
        json_to_csv_trip_advisor(input_file_paths, my_restaurant_location)
        
        # update geocode lookup table
        input_file_paths_csv = change_extension_to_csv(input_file_paths)
        update_geocode_lookup_table(input_file_paths_csv)
        
        # add features and do some data cleaning
        clean_and_feature_generation_trip_advisor(input_file_paths_csv)

        break # exit user prompt loop
