from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    allergies:List[str]
    contact_details:Dict[str,str]
    email: str
    
# Somtimes there is a requirement to validate your data on your custom business needs such as checking the domain of your email or some other things that cant be handled with custom datatypes. Here the field_validator comes into play.
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        
        valid_domains = ['hdfc.com','icici.com']
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value 
    
# Field validator works in 2 ways i.e. in After mode or in before mode. In after mode, the data which is given during the creation of the pydantic object is first type coerced adn after that the value is provided to the Field validator and in before mode, its given before the type coercion has happened.
# By default, the mode is set to after.
    @field_validator('age', mode='before')
    @classmethod
    def check_age(cls, value):
        if 18 <= value < 100:
            return value
        else:
            raise ValueError('Age should be between 18-100')
    
        
def insert_patient_data(patient: Patient):  
    print(patient.name)
    print(patient.age)
    print('Data Inserted')
    
patient_data = {'name':'Horizon', 'age':18, 'weight':76, 'allergies' : ['Pollen'],'contact_details':{'phone_no':'12345'}, 'email':'12345@hdfc.com'}

patient1 = Patient(**patient_data)  

insert_patient_data(patient1)