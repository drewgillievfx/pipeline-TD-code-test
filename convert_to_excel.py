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

##############################################################################
# 5. Format data
def title_names_to_excel(input_names):
    for name in input_names:
        print(name)

title_names_to_excel(column_names)
##############################################################################
wb.save('converted_data.xlsx')
print ("\nFinished") # only for testing purposes
