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
""" Variables to change for different type of data sheets. """
column_names = ['Task', 'Set Part', 'Parent Build', 'Start Date', 'End Date']

##############################################################################
""" 1. Defining the data class. """

class CapturedData:
    def __init__(self, object_name, task_name, set_part,
                 parent_build, start_date,
                 end_date):

        self.object_name = object_name
        self.task_name = task_name
        self.set_part = set_part
        self.parent_build = parent_build
        self.start_date = start_date
        self.end_date = end_date

    def print_status(self):
        print(F'object_name = {self.object_name}')
        print(F'task_name = {self.task_name}')
        print(F'set_part = {self.set_part}')
        print(F'parent_build = {self.parent_build}')
        print(F'start_date = {self.start_date}')
        print(F'end_date = {self.end_date}')
        

    
    def set_start_date(self, date_string):
        date_format = "%Y-%m-%d"
        self.start_date = datetime.strptime(date_string, date_format)

    def set_end_date(self, date_string):
        date_format = "%Y-%m-%d"
        self.end_date = datetime.strptime(date_string, date_format)

##############################################################################
""" 2. Create an excel file. """


def set_cell_value(worksheet, row, col, value):
    cell = worksheet.cell(row=row, column=col)
    converted_value = ''.join(value)
    cell.value = converted_value


def create_excel_file(data_file_name):
    wb = Workbook()  # Create a workbook.
    ws = wb.active  # Add worksheet.
    ws.title = 'Formatted'  # Change title.

    # Pass titles from column_names list to excel.
    for i in range(1,(len(column_names)+1)):
        title = str(column_names[i-1])

        set_cell_value(ws, 1, i, title)

    # Create file name and save file.
    output_file = (data_file_name + '_converted_data.xlsx')
    wb.save(output_file)
    

##############################################################################
##############################################################################

if __name__ == '__main__':
    print('\nStarting Script\n')  # Only for testing purposes--------------.
    a = CapturedData('a1', 'build', 'roof', 'horace', '2016-12-05', '2017-1-23')
    a.print_status()
    
    # Input file when script is run through command line
    input_file = sys.argv[1]  # 'test_data.pkl'
    create_excel_file(input_file)

    # Unpickle, sort, and set up excel file.
    # process_data(input_file)

    # Select data in excel and format it.
    # format_data()
    
    print('\nFinished Processing')  # Only for testing purposes----------.
