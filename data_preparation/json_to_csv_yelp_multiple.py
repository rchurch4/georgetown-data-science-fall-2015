################
# json_to_csv_yelp.py
# Version 3
# Python 2
#
# Description:
# This script takes as input the scraped restaurants from yelp in
# json format, and outputs a csv file with the same information, 
# but organized so that each observation is a review. The script
# also encodes string inputs as UTF-8.  
#
# Input Details:
# List of json input files, each structured as a list of dictionaries, where
# each dictionary is associated with one restaurant. 
#
# Output Details:
# csv where each row represents a unique user review
#
# File Dependencies:
#   input_file_path (user-defined)
#
################

import json
import csv

################
# Set Data File Paths (USER-DEFINED)
# 
# Details: 
# input_file_paths should be given as a list of strings.
# output_file_paths will be created automatically, changing
# .json extension to .csv extension. 
# There is also an optional section to dynamically generate
# file names, if they are structured as 'root_#_ending'.
# 
# Example: input_file_paths = ['data/yelp_dc_1.json', 'data/yelp_dc_2.json']
################

####
# Optional - dynamically generate input file paths
'''
make_input_file_paths = []
start_num = 0 # user-defined
end_num = 13 # user-defined
for i in range(start_num, end_num + 1):
    path_root = 'data/yelp_nsh_' # user-defined
    path_ending = '.json' # user-defined
    current_path = path_root + str(i) + path_ending
    make_input_file_paths.append(current_path)
'''
####    
# Mandatory - Set paths
input_file_paths = make_input_file_paths # user defined

################
# Issue User Warning
################

current_user_prompt = "This script will overwrite any csv files with the same name. Therefore, you should make sure that input_file_path is correct in the script before running. Do you want to proceed with running the script? (Y/N): "
while True:

    user_proceed_response = raw_input(current_user_prompt)
    if user_proceed_response.lower() != 'y' and user_proceed_response.lower() != 'n':
        print '\nPlease enter "Y" for Yes and "N" for No. No other responses will be accepted. \n'
        current_user_prompt = "Do you want to proceed with running the script? (Y/N): "
    elif user_proceed_response.lower() == 'n':
        print 'Aborting json to csv conversion.'
        break
    elif user_proceed_response.lower() == 'y':
        print 'Starting json to csv conversion.'
    
    ################
    # Begin conversion
    ################
    
        for i, current_input_file_path in enumerate(input_file_paths):

            current_output_file_path = current_input_file_path.replace('.json', '.csv')

            # Read in scraped data from json input. 
            with file(current_input_file_path, 'r') as yelp_input_file:
                yelp_data_string = yelp_input_file.read()

            # Convert data to a list.
            yelp_restaurant_list = json.loads(yelp_data_string)

            # Prepare list of observations to output.
            yelp_observations_list = []

            # Prepare final header (but, will need to rename some input dictionary keys)
            yelp_data_header = {'restaurant_name': None,
                                'restaurant_location': 'Washington, DC',
                                'restaurant_overall_rating': None,
                                'restaurant_num_reviews': None,
                                'restaurant_url': None,
                                'restaurant_phone': None,
                                'restaurant_address': None,                    
                                'user_name': None,                               
                                'user_rating': None,
                                'user_review': None,
                                'user_location': None,
                                'user_num_reviews': None,
                                'user_review_date': None}

            # Form each final observation and store in a list.
            # Loop through restaurants
            for i, current_restaurant in enumerate(yelp_restaurant_list):
                # Loop through reviews
                for j, current_review in enumerate(current_restaurant['reviews']):
                    # Form current_observation
                    current_observation = {'restaurant_name': current_restaurant['name'].encode('utf-8').strip(),
                                           'restaurant_location': 'Washington, DC',
                                           'restaurant_overall_rating': current_restaurant['rating'],
                                           'restaurant_num_reviews': current_restaurant['num_reviews'],
                                           'restaurant_url': current_restaurant['url'].strip(),
                                           'restaurant_phone': current_restaurant['phone'],
                                           'restaurant_address': current_restaurant['address'].encode('utf-8').strip(),
                                           'user_name': current_review['name'].encode('utf-8').strip(),                               
                                           'user_rating': current_review['rating'],
                                           'user_review': current_review['review'].encode('utf-8').strip(),
                                           'user_location': current_review['location'].encode('utf-8').strip(),
                                           'user_num_reviews': current_review['exp'].encode('utf-8').strip(),
                                           'user_review_date': current_review['date'].encode('utf-8').strip()}
                    yelp_observations_list.append(current_observation)
                    
            # Write to a csv file. 
            with file(current_output_file_path, 'wb') as yelp_output_file:
                yelp_csv_ouput = csv.DictWriter(yelp_output_file, yelp_data_header.keys())
                yelp_csv_ouput.writerow(dict(zip(yelp_data_header.keys(), yelp_data_header.keys()))) # write header
                for i, current_obs in enumerate(yelp_observations_list):
                    yelp_csv_ouput.writerow(current_obs)
                    
            print "Finished conversion for:", current_output_file_path

        break # exit while loop after all conversions are done