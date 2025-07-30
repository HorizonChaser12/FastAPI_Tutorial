from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()

class Patient(BaseModel):
    # The ... in the field shows that it is required.
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
         
class PatientUpdate(BaseModel):
    # id is not repeated here because it is a part of the Patient model.
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    
    
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

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update:PatientUpdate):
    data = loadData()
    if patient_id not in data:
         raise HTTPException(status_code=404, detail='Patient ID not found.')
    
    # This is used to load all the value of the key which was provided to us in the function parameter
    existing_patient_info = data[patient_id]
    
    # We are storing the update info that the client has given to use into a variable. We are coverting it from a pydantic object to a python dictionary with the unset value to true so that the fields which aren't given should not be in the dictionary with null values.
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    # Here are looping through the updated data we have to update the things in the existing data.
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    
    # This has a issue in it, the problem is that if we update weight and height then we need to recalculate the BMI and verdict too, as it is not updated by itself. 
    # data[patient_id] = existing_patient_info
    
    # This is how you create a pydantic object. But there is still a issue over here, i.e. we have a missing required field i.e id field.
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)
    
    # as we dont need the id tag in the other pydantic class we made, so we will exclude it.
    existing_patient_info = patient_pydantic_object.model_dump(exclude='id')
    
    # Add this dict to data
    data[patient_id] = existing_patient_info
    
    # save data
    saveData(data)
    
    return JSONResponse(status_code=200, content='Patient Updated')


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = loadData()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient is not found')
    
    del data[patient_id]
    
    saveData(data)
    
    return JSONResponse(status_code=200, content='Patient deleted')