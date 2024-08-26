import os
from datetime import datetime
from database import DB, Users
from user import User
from diary import Diary
from menu import init_menu, login_or_reg

# user_data = {
#     "name": "User2", "age": 25, "weight": 78.5, "height": 185, "bodyfat": 12.2
# }
# user_keys = ['name', 'age', 'weight', 'height', 'bodyfat']
# current_datetime = datetime.now()
# formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
# log_data = [
#     {"user_id":2, "chemical": "Cl", "quantity": 2.5, "date": formatted_datetime},
#     {"user_id":2, "chemical": "Ka", "quantity": 1.5, "date": formatted_datetime}
# ]
# user = User(name="User2", age=25, weight=78.5, height=185, bodyfat=12.2)

db = DB()
user = login_or_reg()
os.system('cls' if os.name == 'nt' else 'clear')
if user: 
    print(f'Welcome, {user["name"]}')
    init_menu(user)
