




# this script needs a major update. it needs to take in
# the current lookup table, then find the unique cities
# in any new source data set, remove those that have already
# been geocoded, and then geocode the remaining ones. 
# then, it should append to the lookup csv output. 
#
# write now it just overwrites and checks everything from
# the source. 





# update_geocode_lookup_table
# Version 1
#
# Description:
# Script creates geocode lookup table for cities.
# This avoids the need to repeatedly ping the API
# every time we need the geocode for a city. It also
# help avoid the api ping time out, since only unique
# cities are pinged rather than all cities in the data
# set (e.g. less api calls).

import pandas as pd
import numpy as np
import os
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import time
import sys

################
# USER-DEFINED - Set Data File Paths
#
# Set the input data source and the output data
# files as a string. Relative or absolute path
# may be used. 
################

input_file_path = 'data/yelp_dc_2.csv'
output_file_path = 'data/geocode_lookup_table_1.csv' 
#       change output to geocode_lookup_table.csv
#       once script working well

################
# Update geocodes 
################

# Read in current geocode lookup table
old_geocode_lookup_table = pd.read_csv('data/geocode_lookup_table.csv')
# Read in input data source
new_data = pd.read_csv(input_file_path)

# Get the locations from old geocode table
old_data_locations = old_geocode_lookup_table.user_location
# Get the locations from input data source
new_data_locations = new_data.user_location.unique()
# Only keep locations that aren't in old lookup table
keep_new_locations = list(set(new_data_locations) - set(old_data_locations))
# Make data frame for new locations
keep_new_locations_df = pd.DataFrame({'user_location' : keep_new_locations})

# Heads up on size
num_items_to_geocode = len(keep_new_locations_df)
print 'items to geocode:', num_items_to_geocode

# Get geocodes for unique cities
for i in range(len(keep_new_locations_df)): 
    try:
        geolocator = Nominatim()
        current_geocode = geolocator.geocode(keep_new_locations_df.loc[i, 'user_location'], timeout=10)
        keep_new_locations_df.loc[i, 'user_latitude'] = current_geocode.latitude
        keep_new_locations_df.loc[i, 'user_longitude'] = current_geocode.longitude
        time.sleep(1.25)
            # at least 1 second delay - http://wiki.openstreetmap.org/wiki/Nominatim_usage_policy
    except: 
        # Note: Sometimes user_location is a few cities. I believe
        #       that is causing the occasional exception to be
        #       thrown. One possible solution to this would be to
        #       extract one city (use comma delimiter) and try
        #       geocoding again before moving on. 
        print i, 'exception thrown', sys.exc_info()
        continue
    print i, 'out of', num_items_to_geocode # to see progress

    
# Add in new results
combine_results_df = pd.concat([old_geocode_lookup_table, keep_new_locations_df])
    
# Write to csv
combine_results_df.to_csv(output_file_path, index=False)


