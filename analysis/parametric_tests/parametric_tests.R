#### Parametric tests

#### References
# 1) Set working directory to the file path of a script:
# http://stackoverflow.com/questions/13672720/r-command-for-setting-working-directory-to-source-file-location

#### Set working directory
#### Makes use of location of this script to set data path relatively. 

path_to_script <- parent.frame(2)$ofile
setwd(gsub("analysis/parametric_tests/parametric_tests.R", 
           "data", 
           path_to_script))

#### Read in the data

# Yelp

test <- read.csv(file="yelp_dc_1_cleaned_features.csv", header=TRUE)

# Trip Advisor


