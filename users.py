import secrets
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response,status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List
from starlette.responses import RedirectResponse


router = APIRouter()

list_of_session_tokens: List[str]


VALID_CREDENTIALS = {"login": "trudnY",
                     "password": "PaC13Nt",}

security = HTTPBasic()

def user_must_be_logged_CHECK(credentials: HTTPBasicCredentials = Depends(security)): #session_token: str = Cookie(None)
    # #print(session_token)
    correct_username = secrets.compare_digest(credentials.username, VALID_CREDENTIALS["login"])
    correct_password = secrets.compare_digest(credentials.password, VALID_CREDENTIALS["password"])
    #print("credetians: ",f"{credentials.username}",f"{credentials.password}")

    #print(correct_username,correct_password)

    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised, login or password incorrect")



@router.post('/login', dependencies=[Depends(user_must_be_logged_CHECK)])
def login_user():
    #print('redirecting to...')
    return RedirectResponse("/welcome", status_code=301)#, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


