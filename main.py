from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def loadData():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data    

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
def sort_patients(sort_by:  str = Query(..., description='This si used to sort the patient data from the DB based on height, weight and BMI'), order_by:str=Query('asc,desc', description='Sort in asc or desc order')):
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