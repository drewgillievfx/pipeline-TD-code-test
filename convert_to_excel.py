"""
    convert_to_excel.py
    Start Date: 20230125
    Version: 1.0
    Written by: Drew Gillie

    This code is written for the purpose of completing a coding challenge for
    Laika for the Media Systems Pipeline Technical Director Position

    ##########################################################################
    Challenge #1

    Write a script that exports the data in a Python dictionary to Microsoft 
    Excel in spreadsheet format. The dictionary is the result of a database 
    query and is provided to you in pickle file called test_data.pkl. The 
    spreadsheet should include columns for:
        - Task Name, 
        - Set Part Name, 
        - Parent Build Name, 
        - Start Date, and 
        - End Date. 
    The data should be sorted by earliest Start Date first. 
    
    If a Due Date has already passed, shade the entire row red in Excel.

    You'll need to install and use an external Python library to handle the 
    Excel import. We use `openpyxl` for this at Laika.

    The database returns unfriendly key names for some fields. We map these 
    keys to the above listed human-readable fields in the following way:
        - Task Name = `content`
        - Set Part = `entity`
        - Parent Build = `sg_parent_build`
        - Start Date = `start_date`
        - End Date = `due_date`
    ##########################################################################


    This program will convert data from a pickle file into an excel file.
    Only relevant data is brought over and sorted from earliest date
    
    Overall thought process:
        1. Load the data from pickle
        2. Sort data by date
        3. Create an excel file
        4. Add headers
        5. Bring data in, sorted by date
        6. Highlight past dates in red

"""
import pickle
from openpyxl import Workbook
from openpyxl.utils import column_index_from_string
from openpyxl.utils import get_column_letter

print ("Start\n") # only for testing purposes

##############################################################################
# 1. Unpickle file and place into a dict

imported_data = "test_data.pkl"

unpickled_data = open(imported_data, "rb")
data = pickle.load(unpickled_data)
# print(data) # [works]

##############################################################################
# 2. Sort data by earliest start date

sorted_data = sorted(data, key=lambda  x: x['start_date'])
# print(sorted_data) # [works]

# get size of dict - may or may not be useful later
dict_size = len(sorted_data)
# print("size of dict = {}\n".format(dict_size))

# create a list of names to denote the different rows from the sorted data
number_of_rows = []

# create name of rows based on the size of the sorted data
for i in range(0,dict_size): # start at 2 because row number 2
    # name and row number
    name_part = "data_starting_row_"
    number_part = i + 2

    # final name should look like "data_starting_row_4"
    list_of_dict_name = name_part + str(number_part)

    # add name to the number_of_rows list
    number_of_rows.append(list_of_dict_name)

# create a list of dicts associated with row numbers on the sheet
individual_row_dict = []
for i in range(0,dict_size): # start at 0 to index at 0th element in list
    # print row name
    # print("\n\n{}".format(number_of_rows[i]))

    # create a new dict for each row
    individual_row_dict.append(dict(sorted_data[i]))

    # print the dict
    # print("    {}\n".format(individual_row_dict[i]))

# print(number_of_rows)
"""
    For purposes of grabbing data from this portion of the code to use later 
    in the code, here is what will be needed:
    
    name of dict: 
        number_of_rows[i]
        print("\n\n{}".format(number_of_rows[i]))
    dict data:
        individual_row_dict[i]
        print("    {}\n".format(individual_row_dict[i]))
"""


##############################################################################
# 3. Create an excel file

wb = Workbook()

# add worksheet
ws = wb.active 

# change title
ws.title = "Formatted"

# I may want to do a check to see if file exists ###

##############################################################################
# 4. Add data to excel file

# Add the column headers and corresponding keys
column_names = ["Task", "Set Part", "Parent Build", "Start Date", "End Date"]
corresponding_keys = ["content", "entity", "sg_parent_build", "start_date", 
                    "due_date"]
# print (column_names)
# print (corresponding_keys)

# FUNCTION to pass column headers from dict to excel 
def title_names_to_excel(input_names):
    column_index = 0 # setting counter iter for stringed loop

    for name in input_names:
        # print(name)

        column_index += 1

        column_letter = get_column_letter(column_index)
        # column_index = column_index_from_string(name)
    
        ws.cell(row=1, column=column_index, value=name)
        # print(column_letter)
title_names_to_excel(column_names)

def remove_brackets(input):
    return str(input).strip("[]")

def remove_quote(input):
    return str(input).strip(" '' ")

# FUNCTION to check the column and return category as value
def check_column_letter_set_data(letter):
    try:
        if letter == 'A':
            value = "content" # Task Name
        elif letter == 'B':
            value = "entity-code" # Part Name
        elif letter == 'C':
            value = "sg_parent_build-code" # Parent Build Name
        elif letter == 'D':
            value = "start_date" # Start Date
        elif letter == 'E':
            value = "due_date" # End Date
        else:
            raise ValueError("There are no columns for this data.")
    except ValueError as e:
        print("An error occured: ", e)
        value = None
    print(value)
    return value 
# check_column_letter_set_data("k") # returns error as expected

# FUNCTION to catch None
def catch_key(input_dict, key_catch, nested_key):
    if input_dict.get(key_catch) is not None:
        if nested_key is not None:
            if nested_key in input_dict.get(key_catch):
                return input_dict[key_catch][nested_key]
            else: 
                return None
        else: 
            return input_dict.get(key_catch)
    else:
        print("Very sneaky data!")
        value = "Not available"
        return input_dict.get(value)
        # return None

# FUNCTION to find specific key-values
def find_specific_key_values(input_dict):
    # create a list
    matching_values =[]
    
    # add values from specific keys to list
    # Task Name
    task_name = catch_key(input_dict, "content", None)
    matching_values.append(task_name) 
    
    # Set Part Name
    # remove brackets from data point
    set_part = remove_brackets(catch_key(input_dict, "entity", "code")) 
    matching_values.append(set_part) 
    
    # Parent Build
    p_build = catch_key(input_dict, "sg_parent_build", "code")
    parent_build = remove_quote(p_build)
    matching_values.append(parent_build) 
    
    # Start Date
    start_date = catch_key(input_dict, "start_date", None)
    matching_values.append(start_date) 
    
    # End Date
    due_date = catch_key(input_dict, "due_date", None)
    matching_values.append(due_date) 
    
    # print("values : {}\n".format(matching_values))
    return matching_values 

# FUNCTION to pass the sorted data from dict to excel
def sorted_data_to_rows(input_data):
    print("Testing sorted_data_to_rows function\n")

    # print dict 
    print("dict: {}\n".format(input_data))

    columns =['A', 'B', 'C', 'D', 'E']
    # for i in range(0, 5):
    for j, value in enumerate(columns):
        for i, value in enumerate(columns):
            print(f'Column: {i + 1}, Value: {value}')
            ws.cell((j+1), (i+1), value)

    
    # if row_number < len(input_data):
            # key_value = find_specific_key_values(input_data[row_number])
    # else:
        # print("Index out of range.")
        # row_number = row_number + 1
        # key_value = find_specific_key_values(input_data[row_number])


    # for i, row in enumerate(input_data):
    #     key_value = find_specific_key_values(row)
    #     for j, cell in enumerate(columns):
    #         cell_pos = cell + str(row_number + i)
    #         ws[cell_pos] = key_value[j]
    #         print(cell_pos)
    
    # ws.cell(2, 2, key_value[1])
   
sorted_data_to_rows(individual_row_dict)

# for i in range(2,(dict_size + 2)):
#     print("row:{}".format(i))
#     # place all data into excel , start at row 2
#     current_row = i
#     sorted_data_to_rows(individual_row_dict,current_row)

##############################################################################
# 5. Format data

##############################################################################
wb.save('converted_data.xlsx')
print ("\nFinished") # only for testing purposes
