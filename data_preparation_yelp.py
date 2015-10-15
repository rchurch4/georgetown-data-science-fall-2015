# data_preparation_yelp.py
# Version 1
#
# Description:
# This script takes json files generated from
# scraping yelp as an input, and in the end 
# delivers csvs that add features in and also
# do some data cleaning. Along the way,
# one more csv per json is created before the
# features are added. And, the geocode lookup
# table is also updated with any new locations
# in the input data files.  
# 
# How to run
# From the shell:
#   1) Navigate to root of github folder.
#      The reason for maintaining this structure is because
#      this script depends on data files that are located in
#      './data'. Also, this script imports some custom
#      functions that are in './data_preparation/yelp/lib'.
#   2) python data_preparation/yelp/data_preparation_yelp.py
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
#   json_to_csv_yelp.py
#   update_geocode_lookup_table.py
#   clean_and_feature_generation_yelp.py
#
# File Dependencies:
#   geocode_lookup_table.csv
#   Files specified below in variable: 
#       input_data_path

import os
import sys
sys.path.insert(0, './data_preparation_lib') # from github folder root
from json_to_csv_yelp import json_to_csv_yelp
from update_geocode_lookup_table import update_geocode_lookup_table
from clean_and_feature_generation_yelp import clean_and_feature_generation_yelp
from change_extension_to_csv import change_extension_to_csv

################
# Set Data File Paths (USER-DEFINED)
# 
# Details: 
# input_file_paths should be given as a list of strings.
# output_file_paths will be created automatically, changing
# .json extension to .csv extension, and appending 
# '_cleaned_features' for the final output files. 
# 
# There is also an optional section to dynamically generate
# file names, if they are structured as 'root_#_ending'.
# 
# Example 1:
# # Manually specify input_file_paths
# input_file_paths = ['data/yelp_dc_1.json', 'data/yelp_dc_2.json']
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
'''
make_input_file_paths = []
start_num = 10 # user-defined
end_num = 19 # user-defined
for i in range(start_num, end_num + 1):
    path_root = 'data/yelp_dc_' # user-defined
    path_ending = '.csv' # user-defined
    current_path = path_root + str(i) + path_ending
    make_input_file_paths.append(current_path)
'''
####    
# Mandatory - Set paths
input_file_paths = ['data/yelp_nsh_20.json']


################
# Proceed with user prompt, then data preparation sequence
################

# Warn user about possibly overwriting csvs.
# Uses a loop to ensure valid input.
current_user_prompt = "This script will overwrite any csv files with the same name. Therefore, you should make sure that input_file_path is correct in the script before running. Do you want to proceed with running the script? (Y/N): "
while True:
    user_proceed_response = raw_input(current_user_prompt)
    if user_proceed_response.lower() != 'y' and user_proceed_response.lower() != 'n':
        print '\nPlease enter "Y" for Yes and "N" for No. No other responses will be accepted. \n'
        current_user_prompt = "Do you want to proceed with running the script? (Y/N): "
    elif user_proceed_response.lower() == 'n':
        print 'Aborting data preparation sequence.'
        break
    elif user_proceed_response.lower() == 'y':
        
        print '\nStarting data preparation sequence. \n'

        # json to csv conversion
        json_to_csv_yelp(input_file_paths)
        
        # update geocode lookup table
        input_file_paths_csv = change_extension_to_csv(input_file_paths)
        update_geocode_lookup_table(input_file_paths_csv)
        
        # add features and do some data cleaning
        clean_and_feature_generation_yelp(input_file_paths_csv)

        break # exit user prompt loop
