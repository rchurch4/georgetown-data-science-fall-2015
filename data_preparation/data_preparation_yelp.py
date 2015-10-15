# data_preparation_yelp.py
# Version 1
#
# Description:
# This script takes json files generated from
# scraping yelp as an input, and in the end 
# delivers csvs that add features in and also
# do some data cleaning. 
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
#   clean_and_feature_generation_yelp_multiple.py
#
# File Dependencies:
#   geocode_lookup_table.csv
#   Files specified in variable: input_data_path


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
input_file_paths = ['data/yelp_dc_1.json', 'data/yelp_dc_2.json']

################
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
        print 'Starting data preparation sequence.'

        # json to csv conversion
        
        # update geocode lookup table
        
        # add features and do some data cleaning

        break # exit user prompt loop
