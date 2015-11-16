# Creates graph of restaurant reviews for yelp or trip advisor.
# writes graph to gml file for use in gephi
#
# Rob Churchill
#
# NOTE: I learned to do this in my data science class last semester. If you are looking for plagiarism things, you will almost certainly find similar clustering code. 
# I did not copy it, I learned this specific way of doing it, and referred to my previous assignments when doing it for this project. If you would like to see my previous
# assignments, I will provide you them on request. Otherwise, I don't think that it's worth adding a lot of extra files for the sole sake of showing that I haven't plagiarized.

import networkx as nx
import numpy as np
import scipy as sp
import csv

folder = 'data/'
file_names = ['yelp_data.csv', 'trip_advisor_data.csv']
# EDIT this line to change which website you make the graph for. True=yelp, False=TripAdvisor
yelp = False

yelp_dataset = list()
file_name = file_names[1]
if yelp == True:
    file_name = file_names[0]
# reads in appropriate file given yelp boolean variable
with open(folder+file_name, 'r') as f:
	reader = csv.reader(f)
	for line in reader:
		yelp_dataset.append(line)

# removes headers
yelp_dataset.remove(yelp_dataset[0])
print len(yelp_dataset)

# create the graph
G = nx.Graph()

for y in yelp_dataset:
    # add the nodes if they don't already exist
    G.add_node(y[4], type='restaurant')
    G.add_node(y[13], type='reviewer')
    # add the edge between the reviewer and restaurant, weight is in different position in each file.
    if yelp == True:
        G.add_edge(y[13], y[4], weight=float(y[2]))
    else:
        G.add_edge(y[13], y[4], weight=float(y[1]))
    
print nx.number_of_nodes(G)
print nx.number_of_edges(G)

# write graph to gml file.
nx.write_gml(G, 'ta_graph.gml')