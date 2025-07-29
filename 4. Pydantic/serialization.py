from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Annotated

# Serialization is used to help export pydantic models as python dictionaries or JSON.
class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    
    name: str
    age: int = Field(ge=18, lt=100)
    weight:  float
    married: Optional[bool] = None
    allergies: List[str]
    contact_details: Dict[str,str]
    address : Address
def insert_patient_data(patient: Patient):  
    print(patient.name)
    print(patient.age)
    print(patient.address)
    print('Data Inserted')
    
Address_data = {'city':'Bhubaneswar', 'state':'Odisha', 'pin': '751002'}

address1 = Address(**Address_data)    
     
patient_data = {'name':'Horizon', 'age':18, 'weight':76, 'allergies' : ['Pollen'],'contact_details':{'phone_no':'12345'},'address':address1}

patient1 = Patient(**patient_data)  

insert_patient_data(patient1)

# This is used to export the model to Python Dictionaries
# Other functions are there like limiting the no. of fields by using include, exclude, etc.
temp = patient1.model_dump()
print(temp)
print(type(temp))

# This will export the model in JSON format
temp2= patient1.model_dump_json()
print(temp2)
print(type(temp2))