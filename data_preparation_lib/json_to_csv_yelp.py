################
# json_to_csv_yelp.py
# Version 4
# Python 2
#
# Description:
# This function takes as input the scraped restaurants from yelp in
# json format, and outputs a csv file with the same information, 
# but organized so that each observation is a review. The script
# also encodes string inputs as UTF-8.  
# This function is used in data_preparation_trip_advisor.py. 
################

import json
import csv

def json_to_csv_yelp(input_file_paths, my_restaurant_location):
    # input: 
    #   input_file_paths
    #       takes the input file paths as a list of string objects.
    #       these paths point to the scraped json yelp files. 
    #   my_restaurant_location
    #       for current input data sets, either DC or Nashville    
    # output: 
    #   One csv per json file is created. 
    # return
    #   None

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
                            'restaurant_location': my_restaurant_location,
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
                                       'restaurant_location': my_restaurant_location,
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
                
        print "Finished conversion for: ", current_output_file_path
        
    print 'All json to csv conversions done.\n'

