################
# Association Rules
# Author: Ravi Makhija
#
# Description:
# 
# File Dependencies:
#   'data/tripadvisor_data.Rdata'
#   'data/yelp_data.Rdata'
#
# References
#   1) 

require("arules")
require("arulesViz")

# Create a categorical variable using binning:
#   Rating 1 or 2 -> low
#   Rating 3 -> medium
#   rating 4 or 5 -> high

# Reference Links:

# https://cran.r-project.org/web/packages/arules/index.html
# https://cran.r-project.org/web/packages/arules/vignettes/arules.pdf
# https://cran.r-project.org/web/packages/arules/arules.pdf
# https://cran.r-project.org/web/packages/arulesViz/index.html
# https://cran.r-project.org/web/packages/arulesViz/vignettes/arulesViz.pdf
# http://www.rdatamining.com/examples/association-rules
