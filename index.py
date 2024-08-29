from database import DB
from menu import Menu

db = DB()
menu = Menu(db, None)
user = menu.login_or_reg()
if user: 
    menu.init_menu()
