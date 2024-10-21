import PySimpleGUI as sg
import os
import json

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, 'contactsdata.json')
if not os.path.exists(file_path):
    with open(file_path, 'w') as f: f.write('[]')

def adding_contact(firstname, secondname, number, ):
    new_contact = {
        'firstname': f'{firstname}',
        'secondname': f'{secondname}',
        'number': f'{number}'
    }
    with open(file_path, 'r+') as fp:
        file_content = json.load(fp)
        file_content.append(new_contact)
        fp.seek(0)
        json.dump(file_content, fp, indent=4)

def review_adding_inputs(firstname, secondname, number):
    if not all ([firstname, secondname, number]):
        return 'Please fill everything out'
    if not number.isdigit():
        return 'You cant use letters for Number'
    with open(file_path, 'r') as fp:
        contacts = json.load(fp)
        for contact in contacts:
            contact_numbers = contact.get('number')
            if number == contact_numbers:
                return 'This Number is already in your Contacts'
    return ''

def removing_contact(contacts, index, fp):
    del contacts[index]
    fp.seek(0)  
    fp.truncate()
    json.dump(contacts, fp, indent=4)

def review_remove_input(contact_to_remove, contacts_list):
    index = -1
    if contact_to_remove == '':
        return 'Please write a Name/Number'
    with open(file_path, 'r+') as fp:
        contacts = json.load(fp)
        for contact in contacts:
            index += 1
            firstname = contact.get('firstname')
            secondname = contact.get('secondname')
            number = contact.get('number')
            if contact_to_remove in (firstname, secondname, number):
                removing_contact(contacts, index, fp)
                contacts_list.removeq(firstname)
                return '', contacts_list
        else:
            return 'No Contacts found'
        
def update_contact_information(values, window):
    selected_contact = ''.join(values['-CONTACTS-'])
    with open(file_path, 'r') as fp:
        contacts = json.load(fp)
        for contact in contacts:
            if selected_contact == contact['firstname']:
                window['-FIRSTNAME_DISPLAY-'].update(value=contact['firstname'])
                window['-SECONDNAME_DISPLAY-'].update(value=contact['secondname'])
                window['-NUMBER_DISPLAY-'].update(value=contact['number'])
                break