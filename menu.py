from diary import Diary
from lab import Lab
from enum import Enum
from datetime import datetime
from database import DB
import os
import re
from diaryform import init_diary_form

class PageType(Enum):
    DIARY = 1
    LAB = 2
    DISTRIBUTORS = 3
    USER_INFO = 4

# log_data = [
#     {"user_id":2, "chemical": "Cl", "quantity": 2.5, "date": formatted_datetime},
#     {"user_id":2, "chemical": "Ka", "quantity": 1.5, "date": formatted_datetime}
# ]

db = DB()

def init_menu(user):
    print(f'1. Diary logs\n2.Lab\n3.Distributors\n4.User info\nSelect page by index:')
    selected_page = input()
    if not re.search(r'^[1-9]$', selected_page) or int(selected_page) > 4:
        print('Invalid command')
        return

    page = PageType(int(selected_page))
    if page == PageType.DIARY:
        controller = Diary(user['id'], db)
        controller_handler = diary_handler
        command_raw = "/p"
    elif page == PageType.LAB:
        controller = None
        controller_handler = lab_handler
        command_raw = "/p"
    # elif page == '3':
    #     pass
    # elif page == '4':
    #     pass
    else:
        print('Invalid command2')
        return

    os.system('cls' if os.name == 'nt' else 'clear')

    while not re.search(r'\s*exit\s*', command_raw) and not re.search(r'\s*menu\s*', command_raw):
        try:
            section_handler(controller, controller_handler, command_raw, user)
            command_raw = input('Enter command: ')
        except ValueError as e: 
            print(e)
            return
        except Exception as e:
            print('An error occurred')
            print(e)
            break

    if re.search(r'\s*menu\s*', command_raw):
        os.system('cls' if os.name == 'nt' else 'clear')
        init_menu()

def section_handler(controller, controller_handler, command_raw, user):
    os.system('cls' if os.name == 'nt' else 'clear')
    fragments = command_handler(command_raw)
    controller_handler(fragments['command'].strip(), fragments['params'], controller, user)

def command_handler(command_raw):
    line_fragments = re.search(r'/([a-zA-Z])\s*(.*)', command_raw)

    if not line_fragments:
        raise ValueError('Invalid command3')
    
    command = line_fragments.group(1)
    params = re.findall(r'\w+', line_fragments.group(2)) if len(line_fragments.groups()) > 1 else []
    return {'command': command, 'params': params}

def diary_handler(command, params, diary: Diary, user):
    
    if command in ['s', 'p']:
        print(diary.title)

    if command == 's':
        sort_by = params[0]
        reversed_order = len(params) == 2 and params[1] == 'desc'
        if sort_by not in diary.header_map.keys() and sort_by != diary.vertical_header:
            raise ValueError('Invalid command4')
        return diary.sort_logs(sort_by, reverse=reversed_order)
    elif command == 'n':
        form_data = init_diary_form()
        db.add_diary_log(user['id'], form_data.chemical.value, form_data.quantity.value, form_data.date.value)
        return diary.populate_diary_logs()
    elif command == 'p':
        return diary()
    
    raise ValueError('Invalid command5')

def lab_handler(command, params, lab, user):
    options = {"muscle_mass": "Muscle mass", "body_fat" : "Body fat reduction", "energy": "Energy", "stength": "Strength"}
    options_text = "\n".join([str(index + 1) + ". " + list(options.values())[index] for index in range(len(options))])
    print("Lab")
    print("Choose the number of the option you wish to max out:")
    print(options_text)
    selected_option = input()

    while not selected_option or int(selected_option) > 4:
        print('Invalid otpion! Try again:')
        selected_option = input()

    lab = Lab()
    print("Choose the chemicals to experiment with (separate with comma):")
    all_chems = ", ".join(lab.all_chem_names)
    print(f"(Possible choices: {all_chems})")
    selected_chems = input()

    while not selected_chems or not len(selected_chems):
        print('Invalid input! Try again:')
        selected_chems = input()

    selected_chems = selected_chems.split(",")
    # TODO fix issue with odd number of parameter
    lab_result = lab.experiment(list(options.keys())[int(selected_option)], selected_chems)
    print(lab_result)

def get_user_data_input():
    print('Please provide your info:')
    user_data = {}
    user_keys = db.get_table_cols('users')
    for key in user_keys:
        print(f'Enter {key}:')
        if key == 'name':
            name = input()
            user_data['name'] = name
            while db.get_user(name):
                print('Name already taken. Please choose another:')
                name = input()
        else:
            user_data[key] = float(input()) if key != 'name' else input()

    db.add_user(user_data)
    return user_data

def login_or_reg(action = None):
    print('Please select an option:\n1. Login\n2. Register')
    user = {}
    if (not action):
        action = input()
    if action == '1':
        print('Enter your name:')
        user_name = input()
        user = db.get_user(user_name)
        if not user:
            return print('User not found')
        return {'id': user.id, 'name': user.name}
    elif action == '2':
        user = get_user_data_input()
        print('User registered\nPlease log in:')
        return login_or_reg('1')
    return print('Invalid command')