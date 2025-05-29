import json
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    active: bool = True
    restrictions: bool = True


class Database():
    def __init__(self, filename='temp_database.txt') -> None:
        self._filename = filename

    def read(self) -> dict[str, User]:
        try:
            with open(file=self._filename, mode='r') as file:
                database = json.load(file)
                return database
        except FileNotFoundError:
            return {}

    def add_user(self, user_data: User):
        db = self.read()

        if db.get(user_data.username):
            raise Exception('Пользователь с таким именем уже существует')

        db[user_data.username] = user_data.model_dump()

        with open(file=self._filename, mode='w') as file:
            json.dump(db, file, indent=4)

    def find_user(self, username: str) -> User:
        db = self.read()

        if user_data := db.get(username):
            return User(**user_data)
        raise Exception('Пользователь не найден')

    def change_password(self, username: str, new_password: str):
        db = self.read()

        db[username]['password'] = new_password

        with open(file=self._filename, mode='w') as file:
            json.dump(db, file, indent=4)

    def change_active_user(self, username: str, active: bool):
        db = self.read()

        db[username]['active'] = active

        with open(file=self._filename, mode='w') as file:
            json.dump(db, file, indent=4)

    def change_restriction_user(self, username: str, restrictions: bool):
        db = self.read()

        db[username]['restrictions'] = restrictions

        with open(file=self._filename, mode='w') as file:
            json.dump(db, file, indent=4)

    def drop(self):
        db = self.read()

        db.clear()

        with open(file=self._filename, mode='w') as file:
            json.dump(db, file, indent=4)
