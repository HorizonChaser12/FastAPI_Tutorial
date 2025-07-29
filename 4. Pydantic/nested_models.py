from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Annotated

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