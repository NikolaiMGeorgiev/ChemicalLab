from diary import Diary
from lab import Lab
from enum import Enum
import os
import re
from diaryform import init_diary_form
from chat.chat import Chat

class PageType(Enum):
    DIARY = 1
    LAB = 2
    DISTRIBUTORS = 3
    USER_INFO = 4


class Menu():
    def __init__(self, db, user):
        self.db = db
        self.user = user
        self.menu_texts = {
            "main": "Menu\n1. Diary logs\n2. Lab\n3. Vendors",
            "lab": "Lab\nSelect the number of an option:\n1. Experiment\n2. View lab history",
            "vendors": "Vendors:\n1. View chat history\n2. New chat",
            "login": "Please select an option:\n1. Login (as user)\n3. Login (as vendor)\n3. Register (as user)"
        }

    def init_menu(self):
        self.clear()
        if (self.user["type"] == "vendor"):
            self.vendor_handler()
            return
        print(self.menu_texts["main"])
        selected_page = self.get_valid_number(4, "Select page by index: ")
        page = PageType(int(selected_page))

        if page == PageType.DIARY:
            self.clear()
            self.diary_handler(Diary(self.user['id'], self.db))
        elif page == PageType.LAB:
            self.lab_handler()
        elif page == PageType.DISTRIBUTORS:
            self.distributors_handler()
        else:
            self.init_menu()

    def diary_handler(self, diary: Diary):
        print(diary.title)
        diary()
        command_raw = input('Enter command: ')
        self.clear()

        try:
            command, params = self.get_command(command_raw).values()
            if command == 's':
                sort_by = params[0]
                reversed_order = True if len(params) == 2 and params[1] == 'desc' else False
                if sort_by not in diary.header_map.keys() and sort_by != "date":
                    raise ValueError('Invalid command! Try agin.')
                # self.clear()
                diary.sort_logs(sort_by, reverse=reversed_order)
            elif command == 'n':
                form_data = init_diary_form()
                self.db.add_diary_log(self.user['id'], form_data.chemical.value, form_data.quantity.value, form_data.date.value)
                diary.populate_diary_logs()
            else:
                raise ValueError('Invalid command! Try agin.')
        except ValueError as e: 
            print(e)
        
        self.diary_handler(diary)

    def lab_handler(self):
        self.clear()
        options = {"muscle_mass": "Muscle mass", "body_fat" : "Body fat reduction", "energy": "Energy", "stength": "Strength"}
        options_text = "\n".join([str(index + 1) + ". " + list(options.values())[index] for index in range(len(options))])
        print(self.menu_texts["lab"])
        selected_option = self.get_valid_number(2, "Select option: ")
        
        print("Lab")
        self.clear()
        lab = Lab()
        if selected_option == 1:
            print("Choose the number of the option you wish to max out:")
            print(options_text)
            selected_option = self.get_valid_number(4, "Select option: ")

            print("Choose AT LEAST 4 chemicals to experiment with (separate with comma):")
            all_chems = ", ".join(lab.all_chem_names)
            print(f"(Possible choices: {all_chems})")
            selected_chems = input("Select chemicals: ")
            selected_chems = selected_chems.split(",")

            while not len(selected_chems) or len(list(filter(lambda x: x in lab.all_chem_names, selected_chems))) != len(selected_chems) or len(selected_chems) < 4:
                print('Invalid input! Try again:')
                selected_chems = input("Select chemicals: ")
                selected_chems = selected_chems.split(",")

            lab_result = lab.experiment(list(options.keys())[int(selected_option) - 1], selected_chems)

            self.clear()
            print("Result substance:")
            print("-".join(lab_result["substance"]))
            print("Substance properties:")
            print("\n".join([effect.replace("_", " ") + ": " + str(lab_result["properties"][effect]) + "%" for effect in lab_result["properties"].keys()]))
            self.db.add_lab_history_record(self.user["id"], "-".join(lab_result["substance"]), lab_result["properties"])
        elif selected_option == 2:
            lab_history = self.db.get_lab_history(self.user["id"])
            if not lab_history:
                print("No lab history")
            else:
                columns = lab.pos_eff_names + lab.neg_eff_names
                columns_width = {column: len(column) + 2 for column in columns}
                max_substance_length = max([len(substance) for substance in map(lambda row: row["substance"], lab_history)]) + 2
                substance_header = "substance" + " " * (max_substance_length - len("substance")) + "|"
                print(substance_header + "|".join([column.replace("_", " ") + " " * (columns_width[column] - len(column)) 
                                for column in columns 
                                if column != "substance"]))
                for row in lab_history:
                    row_text = row["substance"] + " " * (max_substance_length - len(row["substance"]))
                    for column in columns:
                        value = row[column]
                        row_text += "|" + str(value) + "%" + " " * (columns_width[column] - len(str(value)) - 1)
                    print(row_text)
        _ = input("Press any key to go back to the menu...")
        self.clear()
        self.lab_handler()

    def distributors_handler(self):
        self.clear()
        print(self.menu_texts["vendors"])
        selected_option = self.get_valid_number(2, "Select option: ")

        if selected_option == 1:
            pass
        else:
            chat = Chat(self.db, self.user["id"], "user")
            if chat.wait_for_vendor():
                self.clear()
                print("Joined chat with vendor")
                while True:
                    message = input("Enter message: ")
                    self.check_for_exit_command(message)
                    chat.send_message(message)
                    self.clear()
                    chat.print_messages()
                    chat.wait_for_response()
                    self.clear()
                    chat.print_messages()
            else:
                _ = input("Press any key to go back to the menu...")
                self.distributors_handler()

    def vendor_handler(self):
        chat = Chat(self.db, self.user["id"], "vendor")
        chat.create_chat()
        self.clear()
        print("Waiting for a user to join the chat...")
        chat.wait_for_user()
        print("A user entered the chat.")
        while True:
            chat.wait_for_response()
            self.clear()
            chat.print_messages()
            message = input("Enter message: ")
            self.check_for_exit_command(message)
            chat.send_message(message)
            self.clear()
            chat.print_messages()

    def get_user_data_input(self):
        print('Please provide your info:')
        user_data = {}
        user_keys = self.db.get_table_cols('users')
        for key in user_keys:
            print(f'Enter {key}:')
            if key == 'name':
                name = input()
                user_data['name'] = name
                while self.db.get_user(name):
                    print('Name already taken. Please choose another:')
                    name = input()
            else:
                user_data[key] = float(input()) if key != 'name' else input()

        self.db.add_user(user_data)
        return user_data

    def login_or_reg(self):
        print(self.menu_texts["login"])
        user = {}
        action = self.get_valid_number(3, "Enter option: ")
        if action == 1 or action == 2:
            print('Enter your name:')
            user_name = input()
            user = self.db.get_user(user_name) if action == 1 else self.db.get_vendor(user_name)
            if not user:
                self.clear()
                print('User not found')
                self.login_or_reg(action)
            user_data = {'id': user.id, 'name': user.name, 'type': 'user' if action == 1 else 'vendor'}
            self.user = user_data
            return user_data
        elif action == 3:
            user = self.get_user_data_input()
            print('User registered\nPlease log in.')
            return self.login_or_reg()
        self.clear()
        print('Invalid command! Try again.')
        self.login_or_reg()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_command(self, command_raw):
        self.check_for_exit_command(command_raw)
        line_fragments = re.search(r'/([a-zA-Z]+)\s*(.*)', command_raw)

        if not line_fragments:
            raise ValueError('Invalid command! Try again.')
        
        command = line_fragments.group(1)
        params = re.findall(r'\w+', line_fragments.group(2)) if len(line_fragments.groups()) > 1 else []
        return {'command': command, 'params': params}
        
    def get_valid_number(self, max_value, promt_text = ""):
        selected_number = input(promt_text)
        self.check_for_exit_command(selected_number)
        while not re.search(r'^[1-9]$', selected_number) or not int(selected_number) or int(selected_number) > max_value:
            self.check_for_exit_command(selected_number)
            print('Invalid option! Try again.')
            selected_number = input(promt_text)
        return int(selected_number)
    
    def check_for_exit_command(self, command_raw):
        if re.search(r'\s*/exit\s*', command_raw):
            exit()
        elif re.search(r'\s*/menu\s*', command_raw):
            self.clear()
            self.init_menu()