################
# json_to_csv_trip_advisor.py
# Version 3
# Python 2
#
# Description:
# This function takes as input the scraped restaurants from trip_advisor in
# json format, and outputs a csv file with the same information, 
# but organized so that each observation is a review. The script
# also encodes string inputs as UTF-8.  As a side note, for trip advisor, 
# the restaurant information is included in a separate json file, so the
# first part of this code creates a dictionary from that, and this gets
# pulled in while creating the observations of the output data set. 

import json
import csv

def json_to_csv_trip_advisor(input_file_paths, my_restaurant_location):
    # input: 
    #   input_file_paths
    #       takes the input file paths as a list of strings.
    #       these paths point to the scraped json trip_advisor files. 
    #   my_restaurant_location
    #       location of restaurants in current group of data sets
    # output: 
    #   One csv per json file is created. 
    # return
    #   None

    ################
    # Begin conversion
    ################
    
    ################
    # First bring in restaurant information.
    
    # All restaurant info is in Washington_DC_District_of_Columbia_basic_list.json. 
    with file('data/Washington_DC_District_of_Columbia_basic_list.json', 'r') as restaurant_list:
        restaurant_list_string = restaurant_list.read()
    # Convert data to a list.        
    restaurant_list_list = json.loads(restaurant_list_string) 
    restaurant_list_dict = dict()    
    
    for i, current_restaurant in enumerate(restaurant_list_list):
        #print type(current_restaurant[1])
        restaurant_list_dict[current_restaurant[1]] = [current_restaurant[0], current_restaurant[2], current_restaurant[3]]

    ################    
    # Now, focus on the reviews, which are included as separate data sets. 
    
    # Pull in the restaurant information while forming the observations. 
    for i, current_input_file_path in enumerate(input_file_paths):

        current_output_file_path = current_input_file_path.replace('.json', '.csv')
        
        # Read in scraped data from json input. 
        with file(current_input_file_path, 'r') as trip_advisor_input_file:
            trip_advisor_data_string = trip_advisor_input_file.read()

        # Convert data to a list.
        trip_advisor_restaurant_list = json.loads(trip_advisor_data_string)

        # Prepare list of observations to output.
        trip_advisor_observations_list = []

        # Prepare final header (but, will need to rename some input dictionary keys)
        trip_advisor_data_header = {'restaurant_name': None,
                                    'restaurant_location': my_restaurant_location,
                                    'restaurant_url': None,
                                    'restaurant_num_reviews': None,
                                    'restaurant_overall_rating': None,
                                    'user_review_title': None,
                                    'user_rating': None,
                                    'user_review_date': None,
                                    'user_name': None,
                                    'user_location': None,
                                    'user_num_reviews': None,                                                  
                                    'user_helpful_reviews': None,
                                    'user_review': None}
                                            
        # Loop through restaurants
        # Form each final observation and store in a list.
        # Loop through restaurants
        for i, current_restaurant in enumerate(trip_advisor_restaurant_list):
            # Loop through reviews
            for j, current_review in enumerate(current_restaurant[1]):       
                # Form current_observation
                current_observation = {'restaurant_name': current_restaurant[0],
                                       'restaurant_location': my_restaurant_location,
                                       'restaurant_url': restaurant_list_dict[current_restaurant[0]][0],
                                       'restaurant_num_reviews': restaurant_list_dict[current_restaurant[0]][1],
                                       'restaurant_overall_rating': restaurant_list_dict[current_restaurant[0]][2],                                       
                                       'user_review_title': current_review[0],
                                       'user_rating': current_review[1],
                                       'user_review_date': current_review[2],
                                       'user_name': current_review[3],
                                       'user_location': current_review[4],
                                       'user_num_reviews': current_review[5],                                                  
                                       'user_helpful_reviews': current_review[6],
                                       'user_review': current_review[7]} 

                trip_advisor_observations_list.append(current_observation)

                              
        # Encode to unicode and strip white space
        # The error handling is mainly for missing data here.
        # The data has to be encoded to unicode otherwie the
        # subsequent csv export fails. It has to be done for
        # one cell at a time since even if one attribute is 
        # missing for one row, the rest of the string
        # attributes for that row need to be encoded to
        # unicode. 
        # 
        # As a side note, this was not needed for Yelp, 
        # as no errors were thrown without it, perhaps because
        # of no missing data. 
        for i, current_review in enumerate(trip_advisor_observations_list):
            try:
                current_review['restaurant_name'] = current_review['restaurant_name'].encode('utf-8').strip()
            except:
                pass
            try:
                current_review['user_review_title'] = current_review['user_review_title'].encode('utf-8').strip()
            except:
                pass
            try:
                current_review['user_review_date'] = current_review['user_review_date'].encode('utf-8').strip()
            except:
                pass
            try:
                current_review['user_name'] = current_review['user_name'].encode('utf-8').strip()
            except:
                pass
            try:
                current_review['user_location'] = current_review['user_location'].encode('utf-8').strip()
            except:
                pass                
            try:
                current_review['user_review'] = current_review['user_review'].encode('utf-8').strip()
            except:
                pass   
            try:
                current_review['restaurant_url'] = current_review['restaurant_url'].encode('utf-8').strip()
            except:
                pass                   
                       
        # Write to a csv file. 
        with file(current_output_file_path, 'wb') as trip_advisor_output_file:
            trip_advisor_csv_ouput = csv.DictWriter(trip_advisor_output_file, trip_advisor_data_header.keys())
            trip_advisor_csv_ouput.writerow(dict(zip(trip_advisor_data_header.keys(), trip_advisor_data_header.keys()))) # write header
            for i, current_obs in enumerate(trip_advisor_observations_list):
                trip_advisor_csv_ouput.writerow(current_obs)
                
        print "Finished conversion for: ", current_output_file_path
            
    print 'All json to csv conversions done.\n'                        
                        
