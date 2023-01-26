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

print('Start\n')  # Only for testing purposes---.

##############################################################################
""" Variables, lists, etc. """


column_names = ['Task', 'Set Part', 'Parent Build', 'Start Date', 'End Date']
corresponding_keys = ['content', 'entity', 'sg_parent_build',
                      'start_date', 'due_date']

imported_data = 'test_data.pkl'
workbook_title = 'converted_data.xlsx'
worksheet_title = 'Formatted'


##############################################################################
""" 1. Unpickle file and place into a list. """

# Convert pickled data into a list.
unpickled_data = open(imported_data, 'rb')
data = pickle.load(unpickled_data)
# print(data)  # [works] This is a list, not a dict.

# Check type of the converted data.
# t = type(data)  # Only for testing purposes---.
# print('type = {}\n'.format(t))  # Only for testing purposes---.

##############################################################################
""" 2. Sort data by earliest start date. """

# Find size - how many lists are inside this list.
list_size = len(data)
print('Size of list = {}\n'.format(list_size))

sorted_data = sorted(data, key=lambda x: x['start_date'])
# print(sorted_data) # [works].  # Only for testing purposes---.

##############################################################################
""" 3. Create an excel file. """

wb = Workbook()
ws = wb.active  # Add worksheet.
ws.title = worksheet_title  # Change title.

##############################################################################
""" 4. Add data to excel file after fixing some data. """

"""
This section of code is all about taking the input data from the .pkl
file and converting it into simple lists.  The lists will then be added to
excel.  Some issues will arise as some of the input data may return None.
"""


def remove_brackets(input):
    return str(input).strip('[]')


def remove_quote(input):
    return str(input).strip(" '' ")


def title_names_to_excel(input_names):  # Pass titles from list to excel.
    column_index = 0  # Setting counter iter for stringed loop.

    for name in input_names:
        # print(name)  # Only for testing purposes---.
        column_index += 1
        column_letter = get_column_letter(column_index)
        # column_index = column_index_from_string(name)
        ws.cell(row=1, column=column_index, value=name)


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


# def sorted_data_to_rows(input_data):  # pass sorted data from dict to excel
#     # print('Testing sorted_data_to_rows function\n') # Testing purposes---.
#     # print('dict: {}\n'.format(input_data))
#     """
#     Note: if the data changes then this need to be updated.
#     Possibly a different function to handle this is needed.
#     """

#     columns = ['A', 'B', 'C', 'D', 'E']
#     rows = ['1', '2', '3', '4', '5']

#     key_value = find_specific_key_values(input_data)

#     for i, row in enumerate(range(2, (dict_size+2))):
#         for j, col in enumerate(columns):
#             print(f'Rows: {row}, Value: {col}')
#             starting_row = 2
#             cell_value = col
#             ws[col + str(row)] = key_value[i][j]


def catch_key(catch_list):  # Catch None error and return 'Not acailable'.
    """
    Input data = [list, key, nested key].

    The list that is passed into this function contains 3 items.  The first
    two variables are on each item that passes through, however the
    third nested key variable only comes in with a few pieces of data.

    Therefore, if it exists, run the case where all three are tested.
    The thing being tested in this function is if a piece of data from
    the .pkl file did not have an entry.  If no entry, then return a
    phrase 'Not available' in order to keep the code running and note
    this on the excel worksheet.
    """
    data_list = catch_list[0]
    key_catch = catch_list[1]

    if len(catch_list) == 3:
        nested_catch = catch_list[2]
        if key_catch in data_list:
            if data_list[key_catch] is not None:
                if nested_catch in data_list[key_catch]:
                    return data_list[key_catch][nested_catch]
                else:
                    return 'Not available'
            else:
                return 'Not available'
        else:
            return 'Not available'
    else:
        if key_catch in data_list:
            return data_list[key_catch]
        else:
            return 'Not available'


def get_data_from_lists(input_data):  # Find specific key-values.
    """
    This is the main data conversion function.

    The goal is to find the requested data that should be on the
    spreadsheet.

    First, this function creates a variable that contains 2-3 data points.
    The input data, key used to find information, and a nested key, if data
    is inside a list inside of the list (i.e. a nested list).  This data
    gets sent to the catch_key function to make sure there actually is data.

    When sent back, it will print the data to the terminal, then add to excel.

    Some pieces of data may need to be corrected, this is done by removing
    brackts "[]" and single quotes around text " '' ".

    This is done for each list in the larger list converted from the .pkl
    file.  This will look like this:
    [
        [list 0]
        [list 1]
        [etc.]
    ]
    """
    for i in range(0, list_size):
        inner_data = input_data[i]
        print('Sublist: {}'.format(i+1))  # Testing purposes---.

        # TASK ----------------------------------.
        task_list = [inner_data, 'content']
        content = catch_key(task_list)

        if content == 'Not Available':
            continue

        print('{} = {}'.format(column_names[0], content))
        ws.cell(row=i+2, column=1).value = content

        # SET PART ----------------------------------.
        set_part_list = [inner_data, 'entity', 'code']
        entity_code = catch_key(set_part_list)

        if entity_code == 'Not Available':
            continue

        code_no_bracket = remove_brackets(entity_code)
        code_no_quote = remove_quote(code_no_bracket)

        print('{} = {}'.format(column_names[1], code_no_quote))
        ws.cell(row=i + 2, column=2).value = code_no_quote

        # PARENT BUILD  ----------------------------------.
        parent_list = [inner_data, 'sg_parent_build', 'code']
        sg_parent_build_code = catch_key(parent_list)

        if sg_parent_build_code == 'Not Available':
            sg_parent_build_code = 'Not Available'
            continue

        sg_parent = remove_brackets(sg_parent_build_code)

        print('{} = {}'.format(column_names[2], sg_parent))
        ws.cell(row=i+2, column=3).value = sg_parent

        # START DATE ----------------------------------.
        start_list = [inner_data, 'start_date']
        start_date = catch_key(start_list)

        if start_date == 'Not Available':
            continue

        print('{} = {}'.format(column_names[3], start_date))
        ws.cell(row=i+2, column=4).value = start_date

        # END DATE ----------------------------------.
        end_list = [inner_data, 'due_date']
        due_date = catch_key(end_list)
        if due_date == 'Not Available':
            continue

        print('{} = {}\n'.format(column_names[4], due_date))
        ws.cell(row=i+2, column=5).value = due_date

        print('=====================\n')  # Visual element for debugging.


def send_data_to_excel():  # FINAL FUNCTION
    # check_column_letter_set_data('k') # returns error as expected
    title_names_to_excel(column_names)
    get_data_from_lists(sorted_data)


send_data_to_excel()
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


def format_data_on_excel():
    date_to_check_from_excel()
    format_title()
    center_align_cells(ws)
    right_align_column_a()

    columns = ['A', 'B', 'C', 'D', 'E']
    for column in columns:
        autofit_columns(column)

    check_unavailable_data()


format_data_on_excel()


##############################################################################
wb.save(workbook_title)
print('\nFinished')  # only for testing purposes
