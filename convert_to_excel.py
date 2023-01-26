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
from datetime import datetime
from openpyxl.styles import Font
from openpyxl.styles import Alignment
from openpyxl.styles import PatternFill

print ("Start\n") # only for testing purposes

##############################################################################
# Variables, lists, etc
column_names = ["Task", "Set Part", "Parent Build", "Start Date", "End Date"]
corresponding_keys = ["content", "entity", "sg_parent_build", "start_date", 
                    "due_date"]

imported_data = "test_data.pkl"
workbook_title = "converted_data.xlsx"
worksheet_title = "Formatted"


##############################################################################
# 1. Unpickle file and place into a list

# convert pickled data into a list
unpickled_data = open(imported_data, "rb")
data = pickle.load(unpickled_data)
# print(data) # [works] this is a list, not a dict

# check type
# t = type(data)
# print("type = {}\n".format(t))

##############################################################################
# 2. Sort data by earliest start date

# find size - how many lists are inside this list 
list_size = len(data)
print("size of list = {}\n".format(list_size))

sorted_data = sorted(data, key=lambda  x: x['start_date'])
# print(sorted_data) # [works]

##############################################################################
# 3. Create an excel file

wb = Workbook()
ws = wb.active # add worksheet
ws.title = worksheet_title # change title

##############################################################################
# 4. Add data to excel file

# Some data needs to be fixed before it goes into excel
def remove_brackets(input):
    return str(input).strip("[]")

def remove_quote(input):
    return str(input).strip(" '' ")

# FUNCTION - TITLE --> EXCEL to pass column headers from list to excel 
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
    # print("Testing sorted_data_to_rows function\n")

    # print dict 
    # print("dict: {}\n".format(input_data))
    """
        Note: if the data changes then this need to be updated. 
        Possibly a different function to handle the sections needed. 
    """
    columns =['A', 'B', 'C', 'D', 'E']
    rows =['1', '2', '3', '4', '5']
    key_value = find_specific_key_values(input_data)

    # columns = i rows = j
    # for j in range(2, (dict_size + 2)):
    # for i, row in enumerate(rows):
    for i, row in enumerate(range(2, (dict_size+2))):
        for j, col in enumerate(columns):

            print(f'Rows: {row}, Value: {col}')

            starting_row = 2
            cell_value = col
            # ws.cell((starting_row+i), (j+1), cell_value)
            ws[col + str(row)] = key_value[i][j]
            # ws[columns[i] + str(j)] = key_value[i]

   
# sorted_data_to_rows(sorted_data)
# 

# FUNCTION to catch None
def catch_key(catch_list):
    # input data is a list that contains a list, key, and second key
    data_list = catch_list[0]
    key_catch = catch_list[1]

    if len(catch_list) == 3:
        nested_catch = catch_list[2]
        if key_catch in data_list:
            if data_list[key_catch] is not None:
                if nested_catch in data_list[key_catch]:
                    return data_list[key_catch][nested_catch]
                else:
                    return "Not available"
            else:
                return "Not available"
        else:
            return "Not available"
    else:
        if key_catch in data_list:
            return data_list[key_catch]
        else:
            return "Not available"

# FUNCTION to find specific key-values
def get_data_from_lists(input_data):
    for i in range(0,list_size):
        inner_data = input_data[i]

        print("Sublist: {}".format(i+1))

        # TASK 
        task_list = [inner_data, 'content']
        content = catch_key(task_list)
        if content == "Not Available":
            continue
        print("{} = {}".format(column_names[0], content))
        ws.cell(row = i + 2, column=1).value = content

        # SET PART
        set_part_list = [inner_data, 'entity', 'code']
        entity_code = catch_key(set_part_list)
        if entity_code == "Not Available":
            continue
        
        code_no_bracket = remove_brackets(entity_code)
        code_no_quote = remove_quote(code_no_bracket)
        print("{} = {}".format(column_names[1], code_no_quote))
        ws.cell(row = i + 2, column=2).value = code_no_quote


        # PARENT BUILD 
        parent_list = [inner_data, 'sg_parent_build', 'code']
        sg_parent_build_code = catch_key(parent_list)
        if sg_parent_build_code == "Not Available":
            sg_parent_build_code = "Not Available"
            continue

        sg_parent = remove_brackets(sg_parent_build_code)
        print("{} = {}".format(column_names[2], sg_parent))
        ws.cell(row = i + 2, column=3).value = sg_parent
        
        # START DATE
        start_list = [inner_data, 'start_date']
        start_date = catch_key(start_list)
        if start_date == "Not Available":
            continue

        print("{} = {}".format(column_names[3], start_date))
        ws.cell(row = i + 2, column=4).value = start_date

        # END DATE 
        end_list = [inner_data, 'due_date']
        due_date = catch_key(end_list)
        if due_date == "Not Available":
            continue

        print("{} = {}\n".format(column_names[4], due_date))
        ws.cell(row = i + 2, column=5).value = due_date

        print("=====================\n") # visual element for debugging

get_data_from_lists(sorted_data)



##############################################################################
# 5. Format data

# if date has passed, shade entire row red
# select row - fill it with red
def fill_row(selected_row):
    # select row
    row_cells = ws[selected_row]

    # select color red
    fill_color = PatternFill(start_color="FFC7CE", 
                            end_color="FFC7CE", fill_type = "solid")
    font_change = Font(name='Arial', size=12, color='8B0000')

    # set the fill color of the cells in the row
    for cell in row_cells:
        cell.fill = fill_color
        cell.font = font_change

# check date
def date_to_check_from_excel():
    for dates in range(2,(list_size+2)):
        # get date from excel
        date_to_get_checked = ws.cell(row =dates, column=5).value
        
        listed_date = datetime.strptime(date_to_get_checked, "%Y-%m-%d")

        # get current date
        current_date = datetime.now()
        # print(current_date)
        # print(listed_date)
        if listed_date < current_date:
            # print("This date has already passed.")
            fill_row(dates)
        else:
            continue
            # print("This date has not yet passed.")

date_to_check_from_excel()


# format title / header info
def format_title():
    # Set the Title font
    title_font = Font(name='Arial', size=20, color='ffffff')

    # Set Title fill
    title_fill = PatternFill(start_color='000000', end_color='000000', fill_type='solid')

    # Iterate through column_names
    for i, title in enumerate(column_names):
        # Get the column letter
        column_letter = get_column_letter(i + 1)
        column_number = column_letter + '1'

        # Apply the formatting
        # ws[column_number].alignment = title_alignment
        ws[column_number].font = title_font
        ws[column_number].fill = title_fill

format_title()

# center align data
def center_align_cells(worksheet):
    for row in worksheet.iter_rows():
        for cell in row:
            cell.alignment = Alignment(horizontal='center')
center_align_cells(ws)

# right align data for column A
def right_align_column_a():
    for row in ws.iter_rows(min_row=1, max_col=1):
        for cell in row:
            if cell.row != 1:
                cell.alignment = Alignment(horizontal='right', vertical='center')
right_align_column_a()

# size each column based on max cell length
def autofit_columns(column_number):
    # Initialize max_size
    max_size = 0

    # Iterate through cells in the column
    for cell in ws[column_number]:
        # Get the length of the cell value and font size
        length = len(str(cell.value))
        font_size = cell.font.size

        # Update max_size if the current length + font size is greater than max_size
        max_size = max(max_size, length + font_size)

    average_size = 15
    new_column_size = ((average_size + max_size) / 2) - 2
    ws.column_dimensions[column_number].width = new_column_size

    print(max_size)

columns = ["A", "B", "C", "D", "E"]
for column in columns:
    autofit_columns(column)

# check unavailable data
def check_unavailable_data():
    # for info in range(2,(list_size+2)):
        # get date from excel
        # not_available_check = ws.cell(row =info, column=info).value
        
    font_change = Font(name='Arial', size=12, color='8B0000', 
                        bold=True, italic=True)

    for row in ws.iter_rows():
        for cell in row:
            if cell.value == "Not available":
                # Apply the formatting
                cell.font = font_change


check_unavailable_data()






##############################################################################
wb.save(workbook_title)
print ("\nFinished") # only for testing purposes
