from pydantic import BaseModel
from typing import Dict, List, Optional
import enum
import auth_logic


class AuthData(BaseModel):
    id: int
    user_name: str
    password: str
    shape: str
    length: float
    thin: float



class Roles(BaseModel):
    id: int
    role: str


class AccountData(BaseModel):
    id: int
    auth_id: int  # AuthData
    role_id: int  # Roles


InsertStatus = enum.Enum('InsertStatus', {'Inserted': 1,
                                          'UserExists': 2,
                                          'UnexistingRole': 3})


class UserStorage:
    _user_data: List[AccountData] = {}
    _user_role_data: List[Roles] = {}
    _user_auth_data: Dict[str, AuthData] = {}
    _account_auth_max_id: int = 0
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(UserStorage, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        pass

    def insert_user(self, user_name: str, user_password, user_role_id, shape: str, length: float, thin: float) -> InsertStatus:
        if user_name in self._user_auth_data.keys():
            return InsertStatus.UserExists
        if user_role_id >= len(self._user_role_data): #aka max(id)
            return InsertStatus.UnexistingRole
        self._account_auth_max_id += 1
        self._user_auth_data[user_name] = AuthData(id=self._account_auth_max_id,
                                                   user_name=user_name,
                                                   user_password=
                                                   auth_logic.code_password(user_password, shape, length, thin),
                                                   thin=thin,
                                                   shape=shape,
                                                   length=length)
        self._user_data.append(AccountData(id=len(self._user_data),
                                           auth_id=self._account_auth_max_id,
                                           role_id=user_role_id))
        return InsertStatus.Inserted

    def check_username(self, username):
        return username in self._user_auth_data.keys()

    def check_user_role(self, role_id):
        return role_id in tuple(x.id for x in self._user_role_data)

    def get_users_password(self, user_name: str) -> Optional[str]:
        return self._user_auth_data.get(user_name, None)

    def get_user_role(self, user_name):
        return self._user_auth_data[user_name]["role_id"]


fake_db = UserStorage()
