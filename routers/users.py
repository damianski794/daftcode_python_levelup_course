from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List

router = APIRouter()

list_of_session_tokens: List[str]


VALID_CREDENTIALS = {"login": "trudnY",
                     "password": "PaC13Nt",}

def user_must_be_logged_CHECK(session_token: str=Depends(Cookie())):
    print(session_token)

@router.get('/login', dependencies=[user_must_be_logged_CHECK])
def login_user():
    pass



