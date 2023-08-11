from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional

import hashlib
import jwt

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#todo add to safe component (database)
AUTHSECRET = "BlaBlaBla"

class TaskData(BaseModel):
    pass

def verify(token):
    try:
        decoded = jwt.decode(token, AUTHSECRET, algorithms=['HS256'])
        return decoded
    except (Exception) as error:
        #print(error) #todo logs!
        return None#{"success": False}


@app.post("/add_task", response_class=RedirectResponse)
def add_task(body: TaskData, header: Optional[str] = Header(None)):
    if not verify(header["access_token"]):
        return RedirectResponse(header['redirect_url'],
                                status_code=status.HTTP_302_FOUND,
                                headers={"x-error": "Invalid credentials"}) #todo bad request
    #todo add task to database from task_tracker_base

#todo others need to test

#@app.post("/reassign", response_class=RedirectResponse)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)