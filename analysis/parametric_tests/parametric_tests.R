################
# Parametric analyses
# Author: Ravi Makhija
#
# Description:
# Logistic regression and t-test. 
# 
# File Dependencies:
# 'data/tripadvisor_data.Rdata'
# 'data/yelp_data.Rdata'
#
# References
# 1) Set working directory to the file path of a script:
# http://stackoverflow.com/questions/13672720/r-command-for-setting-working-directory-to-source-file-location

require(data.table)
require(bit64)

################
# Set working directory to data directory.
# Makes use of location of this script to set data path relatively. 
################

path_to_this_script <- parent.frame(2)$ofile # must be sourced (rathern than run)
setwd(gsub("analysis/parametric_tests/parametric_tests.R", 
           "data", 
           path_to_this_script))
rm(path_to_this_script) # clean up

################
# Load in data
################

load("tripadvisor_data.Rdata")
load("yelp_data.Rdata")