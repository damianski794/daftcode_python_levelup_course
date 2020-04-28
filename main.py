from fastapi import Cookie, Depends, FastAPI, HTTPException, Response, status
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from typing import Dict

from pydantic import BaseModel
#from .routers import users #todo przerobic zeby odwolywac sie do tego usera z folderu .routers
import users #todo przerzucic to do folderu .routers (czytaj powyzej)
import sqlite3_file


app = FastAPI()
app.include_router(users.router)
app.include_router(sqlite3_file.router)
app.counter = 0
templates = Jinja2Templates(directory="templates")



class HelloNameResp(BaseModel):
    message: str

@app.get('/hello/{name}', response_model=HelloNameResp)
def hello_name(name: str):
    return HelloNameResp(message=f"Hello {name}")

@app.get('/counter')
def counter():
    app.counter += 1
    # return str(app.counter)
    return {"value": app.counter}

# ------------------------------------------------
# PROBA POST

class moj_request(BaseModel):
    first_key = "czyzby kluczyk"

class struktura_zwracana(BaseModel):
    received: dict
    constant_data = "python jest super"

@app.post('/dej/mi/cos', response_model=struktura_zwracana)
def receive_something(rq: moj_request):
    return struktura_zwracana(received=rq)

# ---------------------
# ZADANIE DOMOWE SERIA 1

# zadanie 1
# @app.get('/')
# def hello_world():
#     return {"message": "Hello World during the coronavirus pandemic!"}

#zadanie 2
@app.get('/method')
def GETmethod():
    return {"method": "GET"}

@app.post('/method')
def POSTmethod():
    return {"method": "POST"}

@app.put('/method')
def PUTmethod():
    return {"method": "PUT"}

@app.delete('/method')
def DELETEmethod():
    return {"method": "DELETE"}

# zadanie 3

class patient(BaseModel):
    name: str
    surname: str

class patient_simple_response(BaseModel):
    id: int
    patient: patient

patients: Dict[str, patient] = {}

# zakomentowane 26.04
# @app.post('/patient', response_model=patient_simple_response, dependencies = [Depends(users.check_if_session_exists)])
# def patient_simple_poster(patient_rq: patient):
#     global patients_counter
#     patients.append(patient_simple_response(id=len(patients), patient=patient_rq))
#     return patient_simple_response(id=(len(patients)-1), patient=patient_rq)

# Zadanie 4
@app.get('/patient/{number}')
def patient_simple_getter(number: int):
    global patients
    if number < len(patients) and number >= 0:
        return patients.get(str(number)) #.patient
    raise HTTPException(status_code=204, detail="No content")


# ------------------------------
# WYKLAD 3
from fastapi import Request

@app.get('/', response_model=HelloNameResp) # wyklad 3 zad. 1 ##@app.get('/welcome', response_model=HelloNameResp)
def greet_user(request: Request):
    #print(request)
    return HelloNameResp(message='Hello user')


@app.get('/welcome')
def welcome_user(request: Request, cookie: str = Depends(users.check_if_session_exists)):
    if cookie not in users.set_of_session_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised, jest lipa z ciasteczkiem")
    return templates.TemplateResponse("item.html", {"request": request, "user": "trudnY"})


@app.post('/patient', response_model=patient)
def add_new_patient(name: str, surname: str, response: Response, token: str = Depends(users.check_if_session_exists)):
    patient_ = patient(name=name, surname=surname)
    id_ = app.counter
    patients.update({id_: {"name": patient_.name,
                           "surname": patient_.surname}})

    response.status_code = status.HTTP_301_MOVED_PERMANENTLY
    response.headers["Location"] = f"/patient/{id_}"
    # print('---------------')
    # print(f"patients= {patients}")
    # print('---------------')

    app.counter += 1

    return patient_

@app.get('/patient', dependencies = [Depends(users.check_if_session_exists)])
def get_all_patients():
    # print(patients)
    return patients

@app.delete('/patient/{id}', dependencies = [Depends(users.check_if_session_exists)])
def remove_patient(response: Response ,id: int):
    # print('patients przed usuwaniem', patients)
    if id in patients.keys():
        # print(f'id={id} jest w patients keys')
        patients.pop(id, None)
        response.status_code = status.HTTP_204_NO_CONTENT

    # print('patients po usuwaniu', patients)




