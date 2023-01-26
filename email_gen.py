#!/usr/bin/env python
import pickle

def getItemString(item):
    if item['content'] == 'design':
        task_name = "Design/Concept"
    elif item['content'] == 'first build':
        task_name = "First Build"
    item_string = 'Task Date Change\n'
    item_string += 'Task Name: %s\n' % task_name
    item_string += 'Link: %s\n' % item['entity']['code'][0]
     
    if item['sg_parent_build']:
        item_string += 'Parent Build: %s\n' % item['sg_parent_build']['code']
    else:
         'Not available'
    item_string += 'Start: %s\n' % item['start_date']
    item_string += 'End: %s\n' % item['due_date']
    return item_string

def main():
    with open('test_data.pkl', 'rb') as f:
        data = pickle.load(f)

    email_body = ''
    for item in data:
        item_string = getItemString(item)
        email_body += '%s\n' % item_string

    print (email_body)

if __name__ == '__main__':
    main()

# Comments on solving this
"""
    1. Folding the functions we have a simple code structure
        import pickle
        getItemString - with an input item
        main function
        main test
    2. Working parts
        import
        main test
    3. Lets look at the main function
        opening 'test_data.pkl' and unpickling checks out
        potential issue line 21: email_body = ''
        definite issue line 26: print email_body
            should be print(email_body)
    4. Lets look at the getItemString function
        potentially line 12: with the if statement
            I will move it down a line to fit within Pep 8
            This is a simpler line that could be all on one line, 
            but to keep in the same style, I will change it
    5. Didnt catch on first inspection
        this probably was not the problem
        but cPickle does not work in Python3
        changed to pickle
"""