from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd
from schema.user_input import UserInput

# Import the model
with open('models/model.pkl','rb') as f:
    model = pickle.load(f)

# Initialize FastAPI
app = FastAPI()

    
# To get some info in the deafult page when accessing the API.
@app.get('/')
def home():
    return {'Message': 'This API is being used to predict premiums for particular persons.'}
    
# To showcase about the model as well version lables of the software and other things.
@app.get('/health')
def health_check():
    if model == None:
        return {'Error':'The model is not loaded.'}
    else:
        return {'status':'Model has loaded.'}
    

        
# API Endpoints
@app.post('/predict')
def predict_premium(data: UserInput):
    # To create proper informat format, we will be using pandas such that each row's data can be send fully  to the model as the model is also trained on dataframe.
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])
    
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    class_names = model.classes_
    
    response = {
        "response": {
            "predicted_category": prediction,
            "confidence": float(max(probabilities)),
            "class_probabilities": {
                class_name: float(prob) 
                for class_name, prob in zip(class_names, probabilities)
            }
        }
    }
    
    return JSONResponse(status_code=200, content=response)