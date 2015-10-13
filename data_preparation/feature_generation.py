# feature_generation
# Version 1
#
# Description:
# Script to generate extra features. 
#
# Issues:
# Need to figure out at which point and how data will be
# merged. 

import pandas as pd
import numpy as np
import os
from geopy.geocoders import Nominatim
import time

# Load data in as a Pandas DataFrame.
d = pd.read_csv('data/yelp_dc_pilot_2.csv')
#print d.head()

################
# Some data cleaning
################

# Clean up address formatting

# Coerce user_num_reviews to a float

################
# Feature generating main methods
# 
# Note: Some of the feature generation scrip takes time
# to run (e.g. grabbing geocodes), that is why this script
# has been made modular by allowing one to specify which 
# main methods (e.g. which features) to run in the end. 
################

def make_restaurant_geocode():
    # Generates: 
    #   restaurant_latitude
    #   restaurant_longitude

    # Get geocodes for DC and Nashville
    geolocator = Nominatim()
    dc_geocode = geolocator.geocode("Washington, DC")
    nashville_geocode = geolocator.geocode("Nashville, TN")
    # Assign geocode based on restaurant_location
    for i in range(len(d)):
        # Restaurant geocode
        if d.loc[i, 'restaurant_location'] == "Washington, DC":
            d.loc[i, 'restaurant_latitude'] = dc_geocode.latitude
            d.loc[i, 'restaurant_longitude'] = dc_geocode.longitude
        elif d.loc[i, 'restaurant_location'] == "Nashville, TN":
            d.loc[i, 'restaurant_latitude'] = nashville_geocode.latitude
            d.loc[i, 'restaurant_longitude'] = nashville_geocode.longitude

def make_user_geocode():
    # Generate: 
    #   user_latitude, 
    #   user_longitude

    for i in range(10): # need to set this to len(d) later
        geolocator = Nominatim()
        current_user_geocode = geolocator.geocode(d.loc[i, 'user_location'])
        d.loc[i, 'user_latitude'] = current_user_geocode.latitude
        d.loc[i, 'user_longitude'] = current_user_geocode.longitude
        time.sleep(0.5) # wait since there is one api call per iteration


################
# Run main methods
################

make_restaurant_geocode()
make_user_geocode()

################
# Check out results
################

print d.head(10)
print '----'
print d.tail(10)

   
'''
# Checks        
# print d.dtypes
'''