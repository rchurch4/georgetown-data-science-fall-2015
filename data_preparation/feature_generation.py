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

# Load data in as a Pandas DataFrame.
d = pd.read_csv('data/yelp_dc_pilot_2.csv')
#print os.listdir(os.getcwd())
print d.head()

# Create restaurant_latitude
# Create restaurant_longitude

geolocator = Nominatim()
dc_geocode = geolocator.geocode("Washington, DC")
print dc_geocode.latitude
print dc_geocode.longitude

def set_restaurant_geocode(restaurant_location):
    if restaurant_location == "Washington, DC":
        restaurant_latitude = dc_geocode.latitude
        restaurant_longitude = dc_geocode.longitude
        
        
        
        

