import secrets
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Set
from starlette.responses import RedirectResponse

from hashlib import sha256


router = APIRouter()

set_of_session_tokens: Set[str] = set()


VALID_CREDENTIALS = {"login": "trudnY",
                     "password": "PaC13Nt",}

security = HTTPBasic()

def user_must_be_logged_CHECK(credentials: HTTPBasicCredentials = Depends(security)): #session_token: str = Cookie(None)
    # #print(session_token)
    SECRET_KEY = '5fc649c49b48aeb497e75fedb8ff583b4278a5a147a938c8b6bd5d7409d39499'
    correct_username = secrets.compare_digest(credentials.username, VALID_CREDENTIALS["login"])
    correct_password = secrets.compare_digest(credentials.password, VALID_CREDENTIALS["password"])
    #print("credetians: ",f"{credentials.username}",f"{credentials.password}")

    #print(correct_username,correct_password)

    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised, login or password incorrect")

    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{SECRET_KEY}", encoding='utf-8')).hexdigest()
    # print(f'sesssion_token = {session_token}') #26.04
    return session_token

def check_existing_session_token(token: str)  -> str:
    # print(f'token  z funkcji= {token}') # 26.04

    # print(f'lista dostepnych tokenow= {set_of_session_tokens}') #26.04
    if token not in set_of_session_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised, jest lipa z ciasteczkami")
    return token


@router.post('/login')
def login_user(response: Response, session_token: str = Depends(user_must_be_logged_CHECK)):
    #print('redirecting to...')
    response.set_cookie(key='session_token', value=session_token)
    response.headers["Location"] = "/welcome"
    response.status_code = status.HTTP_301_MOVED_PERMANENTLY

    set_of_session_tokens.add(session_token)
    #return RedirectResponse("/welcome", status_code=301)#, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@router.post('/logout')
def logout(response: Response, session_token: str = Cookie(None)):
    if session_token not in set_of_session_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Lipa z autoryzacją ciasteczkami",
            headers={"WWW-Authenticate": "Basic"},
        )
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/"
    set_of_session_tokens.remove(session_token)

    # token = check_existing_session_token(request.cookies.get('session_token'))
    # set_of_session_tokens.remove(token)
    # return RedirectResponse("/", status_code=status.HTTP_301_MOVED_PERMANENTLY)