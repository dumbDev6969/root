from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
import requests
import feedparser
from utils.crud import CRUD
from utils.enoder import decode_string
from utils.email_sender import my_send_email
from pydantic import BaseModel, EmailStr, field_validator
from routes import geo,signup,send_email,jobs,update

crud = CRUD(host='localhost', user='root', password='', database='jobsearch')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Srecruter(BaseModel):
    company_name: str
    phone_number: str
    state: str
    city_or_province: Optional[str]
    municipality: Optional[str]
    zip_code: str
    street_number: Optional[str]
    email: str
    password: str
    created_at: Optional[str]
    updated_at: Optional[str]



class SignupRecruter(BaseModel):
    table: str
    data: Srecruter

class CreateRequest(BaseModel):
    table: str
    data: dict


    
jobs.run(app)
geo.run(app)
signup.run(app,crud)
send_email.run(app)
update.run(app,crud)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",  # Use "module_name:app_variable"
        host="127.0.0.1", 
        port=11352, 
        reload=True
    )