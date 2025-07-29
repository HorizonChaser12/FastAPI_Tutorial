from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Annotated
# There are many custom datatype you can push into variable such as Emailstr, AnyUrl ,etc from Pydantic.

# Here we are inherting the pydantic's Base Model to implement it.
class Patient(BaseModel):
    
    # You can pass metadata, default value and other parameters by using a combination of Annotated and Field modules.
    name: Annotated[str, Field(default="Horizon",max_length=50, description="Enter the name of the person within 50 chars", examples=['Hello','World'], min_length=5)]
    
    # We can also implement custom data validation, such as checking whether the minimum age should be 18 or anything by using the Field module.
    age: int = Field(ge=18, lt=100)
    # We can add more datatype validation in nested items using the module Typing
    weight:  float
    
    # If we dont provide all the fields while calling a method then it will throw error and every field is marked as required by default. We can make a field optional by importing Optional from the typing module and then incoporating the variable's data type with the below syntax. 
    married: Optional[bool] = None
    
    # The reason we aren't using the usual list() is beacuse we are actually checking the data type of the items that list contains rather than checking the data type of the variable.
    allergies: List[str]
    
    # The same goes over here, we are checking what is the type of the variable and what data does the Dictionary holds inside it.
    contact_details: Dict[str,str]
    
        
#Before hand we used to just implement what parameters do we need when calling this method but to use pydantic we will ask for a object that is inherting the pydantic baseModel to implement data validation. 
# def insert_patient_data(name, age):    
def insert_patient_data(patient: Patient):  
    print(patient.name)
    print(patient.age)
    print('Data Inserted')
    
patient_data = {'name':'Horizon', 'age':18, 'weight':76, 'allergies' : ['Pollen'],'contact_details':{'phone_no':'12345'}}

# Here we have actually converted out data into a packed variable
patient1 = Patient(**patient_data)  

# As we have now changed the type of parameter needed for our function, we will also be providing the same kind of data to the user and check if the data validation works or no.
insert_patient_data(patient1)