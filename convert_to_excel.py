"""
    convert_to_excel.py
    Start Date: 20230125
    Version: 1.1
    Written by: Drew Gillie

    This code is written for the purpose of completing a coding challenge for
    Laika for the Media Systems Pipeline Technical Director Position

    Version changelog:
        1.0 Original submitted code.
        1.1 Modify to run and process rather than script base

    1.1 Notes: Oh! Right, I'm writing this in python, not MEL. I can run main.

    ##########################################################################
    Challenge #1

    Write a script that exports the data in a Python dictionary to Microsoft
    Excel in spreadsheet format. The dictionary is the result of a database
    query and is provided to you in pickle file called'test_data.pkl The
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

    Overall thought process
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
import sys

##############################################################################
# 5. Format data
""" This section of code is dedicated to reformatting the data on excel. """


def fill_row(selected_row):  # Give a row number to fill in red.
    row_cells = ws[selected_row]  # Select row from input.

    # Select the color red.
    fill_color = PatternFill(start_color='FFC7CE',
                             end_color='FFC7CE', fill_type='solid')
    font_change = Font(name='Arial', size=12, color='8B0000')

    # Set the fill color of all of the cells in the row.
    for cell in row_cells:
        cell.fill = fill_color
        cell.font = font_change


def date_to_check_from_excel():  # checks date, colors row red.
    for dates in range(2, (list_size+2)):
        # Get date from excel.
        date_to_get_checked = ws.cell(row=dates, column=5).value
        listed_date = datetime.strptime(date_to_get_checked, '%Y-%m-%d')

        # Get current date.
        current_date = datetime.now()
        # print(current_date)  # Only for testing purposes---.
        # print(listed_date)  # Only for testing purposes---.
        if listed_date < current_date:
            # print('This date has already passed.')  # Testing purposes---.
            fill_row(dates)
        else:
            # print('This date has not yet passed.')  # Testing purposes---.
            continue


def format_title():  # Format the titles / headers.
    # Set the Title font.
    title_font = Font(name='Arial', size=20, color='ffffff')

    # Set Title fill.
    title_fill = PatternFill(start_color='000000', end_color='000000',
                             fill_type='solid')

    # Iterate through column_names.
    for i, title in enumerate(column_names):
        column_letter = get_column_letter(i + 1)  # Get the column letter.
        column_number = column_letter + '1'

        # Apply the formatting.
        ws[column_number].font = title_font
        ws[column_number].fill = title_fill


def center_align_cells(worksheet):  # Alaign data to center.
    for row in worksheet.iter_rows():
        for cell in row:
            cell.alignment = Alignment(horizontal='center')


def right_align_column_a():  # Aligns first column data to right.
    for row in ws.iter_rows(min_row=1, max_col=1):
        for cell in row:
            if cell.row != 1:
                cell.alignment = Alignment(horizontal='right',
                                           vertical='center')


def autofit_columns(column_number):  # Adjust column width based on max cell.
    max_size = 0  # Initialize the max size.

    # Iterate through cells in the column.
    for cell in ws[column_number]:
        # Get the length of the cell value and font size.
        length = len(str(cell.value))
        font_size = cell.font.size
        max_size = max(max_size, length + font_size)

    average_size = 15  # Guess and check to see how it looks.
    new_column_size = ((average_size + max_size) / 2) - 2

    # print(max_size)  # Only for testing purposes---.
    ws.column_dimensions[column_number].width = new_column_size


def check_unavailable_data():  # Search for data with no entry point.
    # Set the destination font change.
    font_change = Font(name='Arial', size=12, color='8B0000',
                       bold=True, italic=True)

    """
    Search all of the data to find 'Not available'.
    This strange error is documented, but all instances of 'Not available'
    must be a lower case 'a'.

    When 'Not available' is found, set the font change.
    """
    for row in ws.iter_rows():
        for cell in row:
            if cell.value == 'Not available':
                # Apply the formatting.
                cell.font = font_change

def format_data():
    format_title()
    center_align_cells(ws)
    right_align_column_a()

    columns = ['A', 'B', 'C', 'D', 'E']
    for column in columns:
        autofit_columns(column)

    check_unavailable_data()
##############################################################################

class CapturedData:
    def __init__(self, object_name, task_name, set_part,
                 parent_build, start_date: None,
                 end_date: None):

        self.object_name = object_name
        self.task_name = task_name
        self.set_part = set_part
        self.parent_build = parent_build
        self.start_date = start_date
        self.end_date = end_date

    def set_start_date(self, date):
        self.start_date = date
    
    def set_start_date(self, date_string):
        date_format = "%Y-%m-%d"
        self.start_date = datetime.strptime(date_string, date_format)


data_entry_1 = CapturedData("task1", "set1", "build1")
data_entry_1.set_start_date("2021-01-01")
print(data_entry_1.start_date)




    



##############################################################################
##############################################################################
""" section of code to delete when ready """


column_names = ['Task', 'Set Part', 'Parent Build', 'Start Date', 'End Date']
corresponding_keys = ['content', 'entity', 'sg_parent_build',
                    'start_date', 'due_date']



##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################


def remove_brackets(input):
    return str(input).strip('[]')


def remove_quote(input):
    return str(input).strip(" '' ")




def check_column_letter_set_data(letter):  # check column and return value
    try:
        if letter == 'A':
            value = 'content'  # Task Name.
        elif letter == 'B':
            value = 'entity-code'  # Part Name.
        elif letter == 'C':
            value = 'sg_parent_build-code'  # Parent Build Name.
        elif letter == 'D':
            value = 'start_date'  # Start Date.
        elif letter == 'E':
            value = 'due_date'  # End Date.
        else:
            raise ValueError('There are no columns for this data.')
    except ValueError as e:
        print('An error occured: ', e)
        value = None
    # print(value)  # Only for testing purposes---.
    return value


def find_specific_key_values(input_dict):  # Find specific key-values.
    matching_values = []  # Create a list for values from keys.

    # Add values from specific keys to list.

    # 1. Task Name.
    task_name = catch_key(input_dict, 'content', None)
    matching_values.append(task_name)

    # 2. Set Part Name.
    # Need to remove brackets from  this data point.
    set_part = remove_brackets(catch_key(input_dict, 'entity', 'code'))
    matching_values.append(set_part)

    # 3. Parent Build.
    p_build = catch_key(input_dict, 'sg_parent_build', 'code')
    parent_build = remove_quote(p_build)
    matching_values.append(parent_build)

    # 4. Start Date.
    start_date = catch_key(input_dict, 'start_date', None)
    matching_values.append(start_date)

    # 5. End Date.
    due_date = catch_key(input_dict, 'due_date', None)
    matching_values.append(due_date)

    # print('values : {}\n'.format(matching_values))  # Testing purposes---.
    return matching_values






##############################################################################
""" 1. Unpickle and sort data by earliest start date, place in list. """

def get_value(input_data, key_code):  # Find specific key-values.
    """
    This is the main data conversion function.

    The goal is to find the requested data that should be on the
    spreadsheet.

    When an object is created, it will set object traits to the value it 
    should be.  This function retreives the value for the associated key.

    Some pieces of data may need to be corrected, this is done by removing
    brackts "[]" and single quotes around text " '' ".
    """

    switcher = {
        'task_name': ('content', None),
        'set_part': ('entity', 'code'),
        'parent_build': ('sg_parent_build', 'code'),
        'start_date': ('start_date', None),
        'due_date': ('due_date', None)
    }
    if key_code not in switcher:
        return 'Invalid Key (key_code'

    # Find the corresponding key-value pair
    key_values = switcher.get(key_code) # Get the key-cade value

    # if the pair has a nested list, get the nested value
    if key_values[1] is not None:
        returned_key = input_data[key_values[0]][key_values[1]]
    else:  # get the normal value
        returned_key = input_data[key_values[0]]
    # Some data may not exist, 
    if returned_key is None:
        returned_key = 'Not available'

    # Fix formatting issues with data, check for [] and '.
    bracket = ('[' + returned_key + ']')
    quote = ("'" + returned_key + "'")

    if returned_key == bracket:
        returned_key = remove_brackets(returned_key)
    if returned_key == quote:
        returned_key = remove_quote(returned_key)

    return returned_key


def create_new_data_objects(data_in):
    # Convert pickled data into a list.
    unpickled_data = open(data_in, 'rb')
    data = pickle.load(unpickled_data)

    # Sort data by start date now
    sorted_data = sorted(data, key=lambda x: x['start_date'])

    # Find size - how many lists are inside this list.
    list_size = len(sorted_data)
    print('Size of list = {}\n'.format(list_size))

    # List of objects created from data
    captured_data_list = []
    for i in range(0, list_size):
        object_name = ('object_' + i)
        captured_data_list.append(CapturedData(object_name))

    for objects in captured_data_list:
        """
        For each object, set specific_data to list index
        The List index is which data entry point in the larger list.  Then set
        the object attribute to the key:value pair
        """
        specific_data = sorted_data[objects]
        objects.task_name = get_value(specific_data, 'task_name')
        objects.set_part = get_value(specific_data, 'set_part')
        objects.parent_build = get_value(specific_data, 'parent_build')
        objects.start_date = get_value(specific_data, 'start_date')
        objects.end_date = get_value(specific_data, 'due_date')
        
        ws.cell(row=i+2, column=1).value = content



##############################################################################
""" 2. Create an excel file. """


def create_excel_file(data_file_name):
    wb = Workbook()  # Create a workbook.
    ws = wb.active  # Add worksheet.
    ws.title = 'Formatted'  # Change title.


##############################################################################
""" 3. Add data to excel file after fixing some data. """

"""
This section of code is all about taking the input data from the .pkl
file and converting it into simple lists.  The lists will then be added to
excel.  Some issues will arise as some of the input data may return None.
"""

def title_names_to_excel(input_names):  # Pass titles from list to excel.
    column_index = 0  # Setting counter iter for stringed loop.

    for name in input_names:
        # print(name)  # Only for testing purposes---.
        column_index += 1
        column_letter = get_column_letter(column_index)
        # column_index = column_index_from_string(name)
        ws.cell(row=1, column=column_index, value=name)


def add_data_to_excel_file(data, data_file_name):
    column_names = []  # Find names for titles that match requirements
    title_names_to_excel(column_names)
    get_data_from_lists(sorted_data)



##############################################################################
"""
Main function to process data with script. 

An input file needs to be processed and automated so it creates and fills a 
worksheet in excel.
"""

def process_data(file_to_process):
    hidden_data = unpickle_and_sort_data(file_to_process)
    
    # Create an excel file using the file name of the data to be processed.
    create_excel_file(file_to_process)
    add_data_to_excel_file(hidden_data, file_to_process)
    
    

##############################################################################
##############################################################################

if __name__ == '__main__':
    print('Starting Script\n')  # Only for testing purposes---.

    # Input file when script is run through command line
    input_file = sys.argv[1]  # 'test_data.pkl'
    output_file = (input_file + '_converted_data.xlsx')

    # Unpickle, sort, and set up excel file
    process_data(input_file)

    wb.save(output_file)
    print('\nFinished Processing')  # only for testing purposes

"""
Basic command line template:

python3 this_script.py data_to_process.pkl

Note: 
Include full path

python3 /convert_to_excel.py  /test_data.pkl 

"""