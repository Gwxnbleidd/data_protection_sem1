from app.utils.database import User, Database
from app.GUI.main_window import login_window


database = Database()

admin = User(username='admin', password='')
try:
    database.add_user(admin)
except Exception as e:
    pass

if __name__ == '__main__':
    login_window('mainloop')
