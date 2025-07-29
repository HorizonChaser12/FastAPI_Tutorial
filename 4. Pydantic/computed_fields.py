from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict, Optional

class Patient(BaseModel):
    
    name: str
    age: int
    weight: float
    height: float
    married: Optional[bool] = None
    allergies: List[str]
    contact_details: Dict[str, str] 
    email: EmailStr
    
    # Sometimes there is a requirement that can be fullfilled by the fields we  have without asking the user to compute it by itself. Here computed_fields come into play.
    @computed_field
    @property
    # the function name should be called as it is from the particular methods which are implementing it as that becomes the field name too.
    def BMI(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
def insert_patient_data(patient: Patient):  
    print(patient.name)
    print(patient.age)
    print('BMI', patient.BMI)
    print('Data Inserted')
    
patient_data = {'name':'Horizon', 'age':62, 'weight':76,'height':1.23, 'allergies' : ['Pollen'],'contact_details':{'phone_no':'12345', 'emergency':'123456'}, 'email':'12345@hdfc.com'}

patient1 = Patient(**patient_data)  

insert_patient_data(patient1)