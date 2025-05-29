import pickle
from pydantic import BaseModel

class User(BaseModel):
    
    username: str
    password: str
    active: bool = True
    restrictions: bool = True

class Database():
    def __init__(self) -> None:
        pass

    def read(self, filename: str = 'database.txt') -> dict:
        try:
            with open(file=filename, mode='rb+') as file:
                database = pickle.load(file)
                return database
        except FileNotFoundError:
            return {}

    def add_user(self, user_data: User, filename: str = 'database.txt'):
        db = self.read()
        
        if db.get(user_data.username):
            raise Exception('Пользователь с таким именем уже существует')
        
        db[user_data.username] = user_data

        with open(file=filename, mode='wb+') as file:
            pickle.dump(db, file)
        
    def find_user(self, username: str) -> User:
        db = self.read()

        if user:= db.get(username):
            return user    
        raise Exception('Пользователь не найден')
    
    def change_password(self, username: str, new_password: str, filename: str = 'database.txt'):
        db = self.read()

        db[username].password = new_password

        with open(file=filename, mode='wb+') as file:
            pickle.dump(db, file)
    
    def change_active_user(self, username: str, active: bool, filename: str = 'database.txt'):
        db = self.read()

        db[username].active = active

        with open(file=filename, mode='wb+') as file:
            pickle.dump(db, file)

    def change_restriction_user(self, username: str, restrictions: bool, filename: str = 'database.txt'):
        db = self.read()

        db[username].restrictions = restrictions

        with open(file=filename, mode='wb+') as file:
            pickle.dump(db, file)    
    
    def drop(self, filename: str = 'database.txt'):
        db = self.read()

        db.clear()

        with open(file=filename, mode='wb+') as file:
            pickle.dump(db, file)
    
        
