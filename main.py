from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()

class Patient(BaseModel):
    
    id: Annotated[str,Field(..., description='ID of the patient', examples=['P001'])]  
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='Place where the patient is living')]
    age: Annotated[int, Field(gt=0,lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in Kgs')]


@computed_field
@property
def bmi(self) -> float:
     bmi = round(self.weight/(self.height**2),2)
     return bmi
 
@computed_field
@property
def verdict(self) -> str:
    if self.bmi < 18.5: 
        return 'Underweight'
    elif self.bmi < 25:
        return 'Normal'
    elif self.bmi < 30:
        return 'Normal'
    else:
        return 'Obese' 

def loadData():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data   

def saveData(data):
    with open('patients.JSON','w') as f:
        json.dump(data,f)
         

# This is a default endpoint
@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

# These are called endpoints
@app.get("/about")
def about():
    return {"message":"This is why I love learning, so many things to learn."}

#Using /docs in the opened link will open an interactive version of all the endpoints you have created. 

# Used to load data from a local file
@app.get("/view")
def view():
    data = loadData()
    return data

# This is a example on how to use path params and how to use Path()
@app.get("/patient/{patient_id}")
def getPatient(patient_id:str=Path(..., description="ID of the patient in the DB", example='P001')):
    data = loadData()
    
    if patient_id in data:
        return data[patient_id]
# This is how you use a HTTPException rather than returning a JSON file which would often mean that the status code has comepleted successfully but actually the data is not found.
    else:
        raise HTTPException(status_code=404, detail='Patient not found.')
    
@app.get("/sort") 
def sort_patients(sort_by:  str = Query(..., description='This is used to sort the patient data from the DB based on height, weight and BMI'), order_by:str=Query('asc,desc', description='Sort in asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid field select from {valid_fields}')
    
    valid_sorts = ['asc','desc']
    if order_by not in valid_sorts:
        raise HTTPException(status_code=400, detail='Invalid sort method, please choose asc or desc.')
    
    data = loadData()
    sort_order = False if order_by=='asc' else True
    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by,0), reverse =sort_order)
    
    return sorted_data  

@app.post('/create')
def create_patient(patient:Patient):
    # load existing Data
    data  = loadData()
    
    # check if the data is already present in the existing data
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists.')
    # If no existing data, then add the record to the existing database i.e to our JSON File.
    # The exisitng data variable in which we loaded our database's data is a python dictionary while as the data we want to insert into is a pydantic object, so we need to convert the pydantic object to dictionary.
    # We are excluding id because that is the key to our dictionary in our db.
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    # Save the data into the db
    saveData(data)
    
    # Give a response back to the client that the action has been completed
    
    return JSONResponse(status_code=201, content={'message':'patient created'})
     