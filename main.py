from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

app = FastAPI()

app.counter = 0





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
@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

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
    surename: str

class patient_simple_response(BaseModel):
    id: int
    patient: patient

# patients_counter = 0
patients = []

@app.post('/patient', response_model=patient_simple_response)
def patient_simple_poster(patient_rq: patient):
    global patients_counter
    # patients_counter += 1
    patients.append(patient_simple_response(id=len(patients), patient=patient_rq))
    return patient_simple_response(id=(len(patients)-1), patient=patient_rq)

# Zadanie 4
@app.get('/patient/{number}')
def patient_simple_getter(number: int):
    # global patients_counter
    global patients
    # number -= 1 # 0 is the first index of patients list (not 1) - thats why we need to downgrade the number by 1
    if number < len(patients) and number >= 0:
        return patients[number].patient
    raise HTTPException(status_code=204, detail="No content")




