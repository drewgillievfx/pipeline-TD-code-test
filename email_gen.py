#!/usr/bin/env python
import cPickle as pickle

def getItemString(item):
    if item['content'] == 'design':
        task_name = "Design/Concept"
    elif item['content'] == 'first build':
        task_name = "First Build"
    item_string = 'Task Date Change\n'
    item_string += 'Task Name: %s\n' % task_name
    item_string += 'Link: %s\n' % item['entity']['code'][0]
    item_string += 'Parent Build: %s\n' % item['sg_parent_build']['code'] if item['sg_parent_build'] else ''
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

    print email_body

if __name__ == '__main__':
    main()
