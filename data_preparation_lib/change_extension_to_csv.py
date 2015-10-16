# change_extension_to_csv.py
# Version 4
#
# Description:
# A function to convert the list of json file paths to
# the corresponding list of csv file paths. 

def change_extension_to_csv(input_file_paths):
    # input
    #   json file paths as list of string objects
    # return
    #   corresponding csv file paths as list of string objects
    
    input_file_paths_csv = []
    for current_input_file_path in input_file_paths:
        current_csv = current_input_file_path.replace('.json','.csv')
        input_file_paths_csv.append(current_csv)
    return input_file_paths_csv