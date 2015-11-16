# clustering.py
# cluster yelp and TA data
# 
# Rob Churchill
#
# NOTE: IN ORDER TO GET ANY VISUALIZATIONS OUT OF THIS SCRIPT,
#       YOU MUST PUT THIS IN AN IPYTHON NOTEBOOK OR SOMETHING SIMILAR
#
# NOTE: I learned to do this in my data science class last semester. If you are looking for plagiarism things, you will almost certainly find similar clustering code. 
# I did not copy it, I learned this specific way of doing it, and referred to my previous assignments when doing it for this project. If you would like to see my previous
# assignments, I will provide you them on request. Otherwise, I don't think that it's worth adding a lot of extra files for the sole sake of showing that I haven't plagiarized.

import scipy as sp 
import numpy as np
import math
from sklearn.cluster import KMeans
import scipy.cluster.hierarchy as hr
from sklearn.cluster import DBSCAN
import csv
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

folder = 'data/'
file_names = ['yelp_data.csv', 'trip_advisor_data.csv']

yelp_dataset = list()
#change the index of file_names in this line to 0 if you want to cluster yelp, 1 if you want to cluster trip advisor
with open(folder+file_names[1], 'r') as f:
	reader = csv.reader(f)
	for line in reader:
		yelp_dataset.append(line)

# remove headers
yelp_dataset.remove(yelp_dataset[0])

# throw out the fields we don't need so that we have enough memory to cluster such a large dataset
new_yelp_ds = []
for y in yelp_dataset:
	local = 0
	if y[19] == "TRUE":
		local = 1
	
	if y[19]  in ["FALSE", "TRUE"]:	
		for l in range(0, len(y)):
			if y[l] == "NA":
				y[l] = 0
		if int(y[11]) > 99:
			# mean_rating, distance
			y = [float(y[21]), math.log(float(y[18])+1), math.log(int(y[6])+1)]
			new_yelp_ds.append(y)

# this condensed dataset is now our working dataset
yelp_dataset = np.array(new_yelp_ds)
print len(yelp_dataset)

#print np.amax(yelp_dataset[:,1])

# start kmeans. try it with 1...11 clusters to see which is best. for both, it was two.
error = np.zeros(11)
error[0] = 0
for k in range(1,11):
	kmeans = KMeans(n_clusters=k)
	kmeans.fit_predict(yelp_dataset)
	centroids = kmeans.cluster_centers_
	labels = kmeans.labels_
	error[k] = kmeans.inertia_

plt.plot(range(1,len(error)),error[1:])
plt.xlabel('Number of clusters')
plt.ylabel('Error')

# run kmeans on the optimal k
kmeans = KMeans(n_clusters=2, n_init=15)
kmeans.fit_predict(yelp_dataset)
centroids = kmeans.cluster_centers_
labels = kmeans.labels_
error = kmeans.inertia_

print labels
print error

# make it pretty and plot it. kmeans told us literally nothing about this dataset.
colors = []
for l in labels:
    if l == 0:
        colors.append('r')
    elif l== 1:
        colors.append('b')
    elif l == 2:
        colors.append('g')
    elif l == 3:
        colors.append('c')
    else:
        colors.append('m')
plt.scatter(yelp_dataset[:,1], yelp_dataset[:,2], c=colors, s=8, lw=0)

# set up dbscan, set the eps based on the website
# for yelp, use 0.25. For trip advisor use 0.5
dbscan = DBSCAN(eps = 0.5)

# run dbscan on the data
dbscan.fit_predict(yelp_dataset)
labels = dbscan.labels_
print labels


# make it pretty and plot it. dbscan highlights some major grouping of reviews in the data,
# especially the local and non-local groups.
colors = []
for l in labels:
    if l == 0:
        colors.append('r')
    elif l== 1:
        colors.append('b')
    elif l == 2:
        colors.append('g')
    elif l == 3:
        colors.append('c')
    elif l == 4:
        colors.append('y')
    else:
        colors.append('m')

plt.scatter(yelp_dataset[:,1], yelp_dataset[:,2], c=colors, s=8, lw=0)

# hierarchical clustering is a very memory consuming algorithm, so we can only take a small subset of the dataset
# we randomly permute and take the first 1000.
permutation = np.random.permutation(yelp_dataset)
small_ds = permutation[:1000]

# run the algorithm on our data
Z = hr.linkage(small_ds, method='complete', metric='euclidean')

print Z.shape, small_ds.shape

# plot the dendrogram to see how the clusters were created.
fig = plt.figure(figsize=(10,10))
T = hr.dendrogram(Z,color_threshold=0.4, leaf_font_size=1)

fig.show()

# cluster our data and get the labels for plotting.
labels = hr.fcluster(Z, t=7, depth=8)
#print labels

# make it pretty and plot it. heirarchical clustering, like kmeans, showed us nothing interesting.
colors = []
for l in labels:
    if l == 0:
        colors.append('r')
    elif l== 1:
        colors.append('b')
    elif l == 2:
        colors.append('r')
    elif l == 3:
        colors.append('c')
    elif l == 4:
        colors.append('y')
    else:
        colors.append('m')

plt.scatter(yelp_dataset[:,1], yelp_dataset[:,2], c=colors, s=8, lw=0)