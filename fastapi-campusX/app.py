from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
import json

from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional


app = FastAPI()

class Patient(BaseModel):
   id: Annotated[str, Field(..., description='Id of the patinent', examples=['P001'])]
   name: Annotated[str, Field(..., description='name of the patinent')]
   city: Annotated[str, Field(..., description='City where the patient is living')]
   age: Annotated[int, Field(..., gt=0, lt= 120, description='Age of the patinent')]
   gender: Annotated[Literal['male', 'female', 'Others'], Field(..., description='Gender of the patinent')]
   height: Annotated[float, Field(...,gt=0,  description='height of the patinent')]
   weight: Annotated[float, Field(..., gt=0, description='weight of the patinent')]       
   
   
   @computed_field
   @property
   def bmi(self) -> float:
      bmi = round(self.weight / (self.height**2), 2 )
      return bmi
   
   @computed_field
   @property
   def verdict(self) -> str:
      if self.bmi < 18.5:
         return 'Underweight'
      elif self.bmi < 25:
         return 'Normal'
      elif self.bmi < 30:
         return 'Overweight'
      else:
         return 'Obese'


class PatientUpdate(BaseModel):
   name: Annotated[Optional[str], Field(default=None)]
   city: Annotated[Optional[str], Field(default=None)]
   age: Annotated[Optional[int], Field(default=None, gt = 0)]
   gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
   height: Annotated[Optional[float], Field(default=None, gt=0)]
   weight: Annotated[Optional[float], Field(default=None, gt=0)]



def load_data():
   with open("patients.json", "r") as f:
      data = json.load(f) 
   return data 

def save_data(data):
   with open("patients.json", "w") as f:
      json.dump(data,f) 
   

@app.get("/")
def hello():
   return {"message":"Patient Managements System FastAPI"} 

@app.get("/about")
def about():
   return {"about": "A fastapi backend for patient management systems"}


@app.get("/view")
def view_data():
   
   data = load_data()
   return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(..., description='ID of the patients in DB', example = 'Example: P001')):
   ## Load all the data
   data = load_data()
   
   if patient_id in data:
      return data[patient_id]
   raise HTTPException(status_code=404, detail = 'Patient not found')


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort based on bmi, weight and height'), order: str = Query('asc', description='Sort in asc or desc order')):
   valid_fields = ['height', 'weight', 'bmi']
   
   if sort_by not in valid_fields:
      raise HTTPException(status_code=400, detail=f'Invalid filed. Select between these {valid_fields}')
   
   if order not in ['asc', 'desc']:
      raise HTTPException(status_code=400, detail=f'Invalid filed. Select between these asc, desc')
   
   data  = load_data()
   

   sort_order = True if order=='desc' else False

   sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

   return sorted_data
   
   
   
   
@app.post('/create')
def create_patient(patient: Patient):
   ## Load the existing data
   
   data = load_data()
   
   ## Check of the patient exist
   if patient.id in data:
      raise HTTPException(status_code=400, detail='Patient already exist')
   
   ## add new patient
   data[patient.id] = patient.model_dump(exclude=['id'])
   
   ## save into json file
   save_data(data)
   
   return JSONResponse(status_code = 201, content= {'message': 'patient created sucessfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
   
   data = load_data()
   
   if patient_id not in data:
      raise HTTPException(status_code=400, detail= 'Patient not found')
   
   existing_patient_info = data[patient_id]
   
   update_patient_info = patient_update.model_dump(exclude_unset=True)
   
   for key, value in update_patient_info.items():
      existing_patient_info[key] = value
   
   existing_patient_info['id'] = patient_id
   patient_pydantic_obj = Patient(**existing_patient_info)
   existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')
   
   # add this dict to data
   data[patient_id] = existing_patient_info

    # save data
   save_data(data)

   return JSONResponse(status_code=200, content={'message':'patient updated'})
   

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
   data  = load_data()
   
   if patient_id not in data:
      raise HTTPException(status_code=404, detail= 'patient not found')
   del data[patient_id]
   
   save_data(data)
   return JSONResponse(status_code=200, content = {'message': 'Patient Sucessfully deleted'})      