### Based implementation for a task

# ## Type validation, issue in python so we need pydantic for it so we get type and data validation


# def insert_patient_data(name, age):
#     print(name)
#     print(age)
#     print('Inserted into the databased')
    
    
# insert_patient_data('nitish', 'thirty')   

# ## Basic fix but it wont give any error (weak approch)

# def insert_patient_data2(name: str, age: int):
#     print(name)
#     print(age)
#     print('Inserted into the databased')
    
    
# insert_patient_data2('nitish', 'thirty')  




## Implementation with pydantic

# from pydantic import BaseModel

# class Patient(BaseModel):
#     name: str
#     age: int

# def insert_patient_data(patient: Patient):
#     print(patient.age)
#     print(patient.name)
#     print('Updated')

# def update_patient_data(patient: Patient):
#     print(patient.age)
#     print(patient.name)
#     print('Updated')

# patients_info = {'name': 'nitish', 'age': 30}    
# patient1 = Patient(**patients_info)

# update_patient_data(patient1)




from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the Patient', description='Give the name of the Patient')]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=100)
    weight: Annotated[float, Field(gt = 0, strict=True)]
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[list[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]
    
def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@gmail.com', 'linkedin_url':'http://linkedin.com/1322', 'age': '30', 'weight': 75.2,'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)