# Ravi Makhija
# update_geocode_lookup_table.py
# Version 4
# Python 2
#
# Description:
# This function updates the geocode lookup table to include
# any locations in the input data sources. . 
# 
# References:
#   geopy documentation: 
#       https://pypi.python.org/pypi/geopy

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import time
import sys

def update_geocode_lookup_table(input_file_paths):
    # input: 
    #   input_file_paths
    #       takes the input file paths as a list of string objects.
    #       these paths point to csv files created from
    #       the originally scraped json files. 
    # output: 
    #       An updated geocode lookup table.     
    #       geocode_lookup_table.csv
    # return
    #       None

    # Set file paths

    old_lookup_table_path = 'data/geocode_lookup_table.csv'
    output_file_path = 'data/geocode_lookup_table.csv' 
    #       note that this overwrites the old lookup table by default.
    #       optional backup feature? 

    ################
    # Update geocodes 
    ################

    # Grab all locations from all input_file_paths.
    all_input_locations = pd.Series()
    for i, current_input_file_name in enumerate(input_file_paths):
        #print i+1, current_input_file_name
        current_input_file = pd.read_csv(current_input_file_name, header = 0)
        all_input_locations = pd.concat([all_input_locations, current_input_file.user_location])

        # Keep only unique input locations. 
        unique_input_locations = all_input_locations.unique()
        # Remove any unique input locations for which we
        # already have the geocode in old_lookup_table. 
        old_lookup_table = pd.read_csv(old_lookup_table_path, header=0)
        old_lookup_table_locations = old_lookup_table.user_location
        unique_input_locations_to_add = list(set(unique_input_locations) - set(old_lookup_table_locations))
        # Heads up on number of items to geocode
        num_items_to_geocode = len(unique_input_locations_to_add)
        print 'starting geocoding for:', current_input_file_name
        print 'items to geocode:', num_items_to_geocode

        # Set up df for unique_input_locations_to_add
        new_only_lookup_table = pd.DataFrame({'user_location':unique_input_locations_to_add})
        # Geocode time!
        for i in range(len(new_only_lookup_table)):
            try:
                geolocator = Nominatim()
                current_geocode = geolocator.geocode(new_only_lookup_table.loc[i, 'user_location'], timeout=10)
                new_only_lookup_table.loc[i, 'user_latitude'] = current_geocode.latitude
                new_only_lookup_table.loc[i, 'user_longitude'] = current_geocode.longitude
                time.sleep(1.25)
                    # at least 1 second delay - http://wiki.openstreetmap.org/wiki/Nominatim_usage_policy
            except: 
                # Note: Sometimes user_location is a few cities. I believe
                #       that is causing the occasional exception to be
                #       thrown. One possible solution to this would be to
                #       extract one city (use comma delimiter) and try
                #       geocoding again before moving on. Will try this
                #       in phase 2 of the project, since it's a matter of
                #       cleanliness of the input location data. 
                print i, 'exception thrown', sys.exc_info()
                continue
            print i+1, 'out of', num_items_to_geocode # to see progress    

        # Combine with old geocode table
        combined_lookup_table = pd.concat([old_lookup_table, new_only_lookup_table])
        # Write to csv
        combined_lookup_table.to_csv(output_file_path, index=False)
        print "geocode lookup table update complete for,", current_input_file_name