# feature_generation
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

# Set up lookup dataframe with unique cities
d = pd.read_csv('data/yelp_dc_pilot_2.csv')
geocode_lookup_table = pd.DataFrame(d.user_location.unique())
geocode_lookup_table.columns = ['user_location'] # rename column

# Get geocodes for unique cities
for i in range(len(geocode_lookup_table)): 
    try:
        geolocator = Nominatim()
        current_geocode = geolocator.geocode(geocode_lookup_table.loc[i, 'user_location'], timeout=10)
        geocode_lookup_table.loc[i, 'user_latitude'] = current_geocode.latitude
        geocode_lookup_table.loc[i, 'user_longitude'] = current_geocode.longitude
    except:
        print i, 'exception thrown', sys.exc_info()
        continue
    print i # to see progress

# Write to csv
geocode_lookup_table.to_csv('data/geocode_lookup_table.csv', index=False)


