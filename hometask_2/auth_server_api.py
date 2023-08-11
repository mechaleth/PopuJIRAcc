from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

import hashlib

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


@app.post("/autorize_user")
async def autorize_user(body: AutorizeUserBody):
    pass #todo redirect user

@app.post("/autentificate_user")
async def autentificate(body: UserAutentificationForm):
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
    return {'success': createResponse}


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
