# concatenate geocode lookup tables, keep unique rows

import pandas as pd
import numpy as np

table1 = pd.read_csv('data/geocode_lookup_table_1.csv', header=0)
table2 = pd.read_csv('data/geocode_lookup_table_2.csv', header=0)
table3 = pd.read_csv('data/geocode_lookup_table_3.csv', header=0)

all_tables = pd.concat([table1, table2, table3])
all_tables_unique = all_tables.drop_duplicates() # unique rows, not cities

# why  don't these match?
# print len(all_tables_unique)
# print len(all_tables_unique.user_location.unique())

all_tables_unique.to_csv('data/geocode_lookup_table_concat.csv', index = False)
