from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

import hashlib

from starlette.responses import HTMLResponse


class AutorizeUserBody(BaseModel):
    pass

class UserAutentificationForm(BaseModel):
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
    email = form_data.username
    password = form_data.password
    print("login")
    #    user = query_user(email)
    #    if not user:
    # you can return any response or error of your choice
    #        raise InvalidCredentialsException
    #    elif password != user['password']:
    #        raise InvalidCredentialsException

    #    token = manager.create_access_token(data={'sub': email})
    #    response = RedirectResponse(url="/protected",status_code=status.HTTP_302_FOUND)
    #    manager.set_cookie(response, token)
    #    return response
    pass #todo login user
    #todo post_autorization_code() here if all right

def post_autorization_code(user_id):
    #todo requests.post to service
    pass

def check_app():
    pass #aka


@app.post("/client")
async def client(body: ServiceBaseClass):
    # verify the token 
    # TO do after we create first credentials

    # get the client_id and secret from the client application
    client_secret_input = body.client_secret
    autorization_code = body.autorization_code      

    # the client secret in the database is "hashed" with a one-way hash
    hash_object = hashlib.sha1(bytes(client_secret_input, 'utf-8'))
    hashed_client_secret = hash_object.hexdigest()

    # make a call to the model to authenticate
    createResponse = check_app(body.user_id, hashed_client_secret, autorization_code)
    return Response(status_code=status.HTTP_200_OK)


@app.post("/signin")
async def create_user(body: UserData):
    pass
    #todo add to database + explore servers



#final request
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = {}#fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = {}#UserInDB(**user_dict)
    hashed_password = form_data.password#fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": "aaaaa", "token_type": "bearer"} #???? Нужно же ответить 200

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
