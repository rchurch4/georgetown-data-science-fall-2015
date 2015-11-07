# Script to remove extra underscore at end of some file names.

# This script is really for a one-time use. The bug that caused
# the extra underscore has been addressed in the data prep scripts.

# Source:
# Modeled this script after code at the following link: 
# http://stackoverflow.com/questions/225735/batch-renaming-of-files-in-a-directory

import glob, os

# Function to get rid of underscore at end of some file names. 
#
# @param dir The directory where data files are located. 
# @param pattern The pattern to locate faulty data file names. 
#
# @return Replaces the current file names with fixed file names (no underscore at end.)
def rename(dir, pattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        title_fixed = title[0:len(title)-1] # remove underscore
        os.rename(pathAndFilename, os.path.join(dir, title_fixed + ext))
        
# Run the function to change file names. 
rename(r'data', r'*_.csv')
