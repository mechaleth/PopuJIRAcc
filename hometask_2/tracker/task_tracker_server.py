from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional

import hashlib
import jwt
from starlette.responses import Response

AUTHSECRET = "SecureNoAzazaza"

class SecretHolder:
    _secret_key = ""

    @classmethod
    def set_secretkey(cls, secret_key):
        cls._secret_key = secret_key

    @classmethod
    def get_secretkey(cls) -> str:
        return cls._secret_key

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_decor(method):
    async def wrapper(req: Request):
        if not verify(req.headers.get("access_token")):
            return RedirectResponse(url="http://localhost:8000/login",  # todo вынести в параметры
                                    status_code=status.HTTP_302_FOUND,
                                    headers={"x-error": "Invalid credentials"})
        await method(req)
    return wrapper


class UpdateKey(BaseModel):
    service_key: jwt.JWT

class TaskData(BaseModel):
    aaa: str

def verify(token):
    try:
        decoded = jwt.JWT.decode(token,
                                 SecretHolder.get_secretkey(),
                                 algorithms='HS256')
        return decoded
    except (Exception) as error:
        #print(error) #todo logs!
        return None#{"success": False}

@app.post("/update_key")
async def update_secret_key(req: UpdateKey):
    decoded = jwt.JWT.decode(req.service_key, AUTHSECRET, algorithms=['HS256'])
    SecretHolder.set_secretkey(decoded["service_key"])
    return Response(status_code=status.HTTP_200_OK)


@app.post("/add_task", response_class=RedirectResponse)
@verify_decor
async def add_task(req: Request):
    print("aaaaa")

    #todo add task to database from task_tracker_base

#todo others need to test

#@app.post("/reassign", response_class=RedirectResponse)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)