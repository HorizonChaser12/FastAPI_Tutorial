from pydantic import BaseModel, model_validator, EmailStr
from typing import List, Dict, Optional

class Patient(BaseModel):
    
    name: str
    age: int
    weight: float
    married: Optional[bool] = None
    allergies: List[str]
    contact_details: Dict[str, str] 
    email: EmailStr
    
    # Field validators have their own limitations. They can only work upon one field and cant retain a field through another field. And here comes model_validator.
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Persons having age above 60 should have a emergency contact')
        return model
    
def insert_patient_data(patient: Patient):  
    print(patient.name)
    print(patient.age)
    print('Data Inserted')
    
patient_data = {'name':'Horizon', 'age':62, 'weight':76, 'allergies' : ['Pollen'],'contact_details':{'phone_no':'12345', 'emergency':'123456'}, 'email':'12345@hdfc.com'}

patient1 = Patient(**patient_data)  

insert_patient_data(patient1)