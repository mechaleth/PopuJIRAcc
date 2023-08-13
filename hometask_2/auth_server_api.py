from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

import hashlib

import jwt

from starlette.responses import HTMLResponse

import fake_auth_db
import auth_logic



class UserAutentificationForm(BaseModel):
    name: str
    role_id: int
    shape: str
    length: float
    thin: float

class ServiceBaseClass(BaseModel):
    autorization_code: str
    user_id: str
    client_secret: str
    
class UserData(UserAutentificationForm):
    user_id: str

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/autorize_user", response_class=HTMLResponse)
async def autorize_user():
    return """
    <!DOCTYPE html>
    <html>
       <body>
          <form method="POST"  action="/login">
             <label for="username">Username:</label><br>
             <input type="text" id="username" name="username" value="johndoe@mail.com"><br>
             <label for="password">Password:</label><br>
             <input type="password" id="password" name="password" value="hunter2"><br><br>
             <input type="submit" value="Submit">
          </form>
       </body>
    </html>
    """

@app.post("/autorize_user")
async def autentificate(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password
    print("login")
    if fake_auth_db.fake_db.get_users_password(username) is None:
        return Response(f"User {username} not exists", status_code=status.HTTP_404_NOT_FOUND)
    if  auth_logic.code_password(password) != fake_auth_db.fake_db.get_users_password(username):
        return Response(f"Uncorrect {username} credentials", status_code=status.HTTP_404_NOT_FOUND)
    secret = auth_logic.generate_authsecret()
    encoded_jwt = jwt.JWT.encode({"username": username,
                                  "role": fake_auth_db.fake_db.get_user_role()},
                                 secret,
                                 algorithm='HS256')
    auth_logic.post_services_authsecret(secret)
    return Response(headers={"access_token": encoded_jwt}, status_code=status.HTTP_200_OK)

@app.post("/signin")
async def create_user(body: UserAutentificationForm):
    username = body.username
    password = body.password
    role = body.role_id
    if not fake_auth_db.fake_db.check_user_role(role):
        return Response(headers={"whats_up": f"Uncorrect user role"},
                        status_code=status.HTTP_404)
    if not fake_auth_db.fake_db.check_username(username):
        return Response(headers={"whats_up": f"User {username} already exists"},
                        status_code=status.HTTP_404_NOT_FOUND)
    fake_auth_db.fake_db.insert_user(username, auth_logic.code_password(password),
                                     role, thin=body.thin,
                                     shape=body.shape, length=body.length)
    return Response(status_code=status.HTTP_200_OK)

@app.post("/update_key")
async def update_keys():
    auth_logic.post_services_authsecret(auth_logic.generate_authsecret())
    return Response(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    import uvicorn
    auth_logic.post_services_authsecret(auth_logic.generate_authsecret())
    uvicorn.run(app, host="0.0.0.0", port=8000)
