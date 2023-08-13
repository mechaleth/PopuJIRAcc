from pydantic import BaseModel
from typing import Dict, Tuple, List, Optional
import enum


class AuthData(BaseModel):
    id: int
    user_name: str



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
    _user_data: Dict[int, AccountData] = {}
    _user_role_data: Dict[int, Roles] = {}
    _user_auth_data: Dict[str, AuthData] = {}
    _account_auth_max_id: int = 0
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(UserStorage, cls).__new__(cls)
        return cls.__instance

    def _insert_user(self, user_name: str, user_role_id) -> InsertStatus:
        self._account_auth_max_id += 1
        self._user_auth_data[user_name] = AuthData(id=self._account_auth_max_id,
                                                   user_name=user_name)
        user_data_new_id = max(self._user_data)+1
        self._user_data[user_data_new_id] = AccountData(id=user_data_new_id,
                                                        auth_id=self._account_auth_max_id,
                                                        role_id=user_role_id)
        return InsertStatus.Inserted

    def _update_user(self, user_name: str, user_role_id):
        auth_id = self._user_auth_data[user_name].id
        for acc_id, acc_data in self._user_data.items():
            if acc_data.auth_id == auth_id:
                self._user_data[acc_id] = AccountData(id=acc_id,
                                                      auth_id=auth_id,
                                                      role_id=user_role_id)
                break

    def update_users_data(self, auth_data: AuthData, role: Roles):
        if role.id >= max(self._user_role_data):  # aka max(id)
            self._user_role_data[max(self._user_role_data)+1] = role
        if auth_data.user_name not in self._user_auth_data.keys():
            self._insert_user(auth_data.user_name, role.id)
        else:
            self._update_user(auth_data.user_name, role.id)

    def remove_user_data(self, auth_data: AuthData):
        auth_id = self._user_auth_data[auth_data.user_name].id
        self._user_auth_data.pop(auth_data.user_name)
        account_id = None
        for acc_id, acc_data in self._user_data.items():
            if acc_data.auth_id == auth_id:
                account_id = acc_data.auth_id
                break
        self._user_data.pop(account_id)

    def drop_role(self, role: Roles):
        # Ждём обновления ролей и пользователей
        self._user_role_data.pop(role.id)
        account_id_list = [acc_id for acc_id, acc_data in self._user_data.items() if acc_data.role_id == role.id]
        for _id in account_id_list:
            self._user_data.pop(_id)

