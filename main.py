import PySimpleGUI as sg
import contactsmanager as cm
import os
import json

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, 'contactsdata.json')
if not os.path.exists(file_path):
    with open(file_path, 'w') as f: f.write('[]')
    
contacts_list = []
with open(file_path, 'r') as fp:
    contacts = json.load(fp)
    for contact in contacts:
        name = contact.get('firstname')
        contacts_list.append(name)


def add_contact_gui():
    layout = [[sg.Text('First Name', size=(10, 1)), sg.InputText('', key='-FIRSTNAME-', size=(20,1)),],
            [sg.Text('Second Name', size=(10, 1)), sg.InputText('', key='-SECONDNAME-', size=(20,1))],
            [sg.Text('Number', size=(10, 1)), sg.InputText('', key='-NUMBER-', size=(20,1))],
            [sg.Text('', key='-ADDING_ERROR-')],
            [sg.Button('Add Contact', key='-ADDING_ADD-'), sg.Button('Exit', key='-ADDING_EXIT-')]]
    window = sg.Window('Add Contact', layout, modal=True)

    while True:
        event, values = window.read()   
        if event in (None, '-ADDING_EXIT-'):
            break
        if event == '-ADDING_ADD-':
            firstname = values['-FIRSTNAME-']
            secondname = values['-SECONDNAME-']
            number = values['-NUMBER-']
            error_message = cm.review_adding_inputs(firstname, secondname, number)
            if error_message != '':
                window['-ADDING_ERROR-'].update(value=error_message)
                continue
            cm.adding_contact(firstname, secondname, number)
            break
    window.close()
    return firstname

def remove_contact_gui(contacts_list):
    layout = [[sg.Text('Enter Name or Number')],
            [sg.InputText('', key='-CONTACT_TO_REMOVE-', size=(15, 1))],
            [sg.Text('', key='-REMOVE_ERROR-')],
            [sg.Button('Remove Contact', key='-REMOVING_REMOVE-'), sg.Button('Exit', key='-REMOVING_EXIT-')]]
    window = sg.Window('Remove Contact', layout, modal=True)

    while True:
        event, values = window.read()
        if event in (None, '-REMOVING_EXIT-'):
            break
        if event == '-REMOVING_REMOVE-':
            contact_to_remove = values['-CONTACT_TO_REMOVE-']
            error_message, contacts_list = cm.review_remove_input(contact_to_remove, contacts_list)
            if error_message != '':
                window['-REMOVE_ERROR-'].update(value=error_message)
            else:
                break
    window.close()

def main_gui():
    main_col1 = sg.Column([[sg.Frame('Contact Information', [[sg.Text(),  sg.Column([[sg.Text('First Name:')],
                            [sg.Text('', key='-FIRSTNAME_DISPLAY-')],
                            [sg.Text('Second Name:')],
                            [sg.Text('', key='-SECONDNAME_DISPLAY-')],      
                            [sg.Text('Number:')],
                            [sg.Text('', key='-NUMBER_DISPLAY-')]], size=(200, 270))]])]])

    main_col2 = sg.Column([[sg.Frame('Contacts', [[sg.Column([[sg.Listbox(contacts_list, key='-CONTACTS-',size=(20,20))]],size=(100,270))]])]])

    main_col3 = sg.Column([
        [sg.Frame('Actions',[[sg.Button('add', key='-MAIN_ADD-', size=(9,1)),
                            sg.Button('remove', key='-MAIN_REMOVE-', size=(9,1)),
                            sg.Button('exit', key='-MAIN_EXIT-', size=(9, 1))]])]])
    
    layout = [[main_col1, main_col2],
              [main_col3]]
    window = sg.Window('Contactbook', layout)

    while True:
        event, values = window.read(timeout=1000)
        if event in (None, '-MAIN_EXIT-'):
            break
        if event == '-MAIN_ADD-':
            firstname = add_contact_gui()
            contacts_list.append(firstname)
            window['-CONTACTS-'].update(values=contacts_list)
        if event == '-MAIN_REMOVE-':
            remove_contact_gui(contacts_list)
            window['-CONTACTS-'].update(values=contacts_list)
        cm.update_contact_information(values, window)
        
    window.close()

main_gui()