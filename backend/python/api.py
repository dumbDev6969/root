from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from utils.crud import CRUD
from routes import geo, signup, send_email, jobs, update, query_and_delete

crud = CRUD(
    host='localhost',
    user='root',
    password='',
    database='jobsearch'
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Srecruter(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=255)
    phone_number: str = Field(..., min_length=10, max_length=20)
    state: str = Field(..., min_length=1, max_length=50)
    city_or_province: Optional[str] = Field(None, max_length=50)
    municipality: Optional[str] = Field(None, max_length=50)
    zip_code: str = Field(..., min_length=5, max_length=10)
    street_number: Optional[str] = Field(None, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    created_at: Optional[str]
    updated_at: Optional[str]

    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not v.isdigit():
            raise ValueError('Phone number must contain only digits')
        return v

class SignupRecruter(BaseModel):
    table: str
    data: Srecruter

class CreateRequest(BaseModel):
    table: str
    data: dict

modules_to_run = [
    (jobs, [app]),
    (geo, [app]),
    (signup, [app, crud]),
    (send_email, [app]),
    (update, [app, crud]),
    (query_and_delete, [app, crud]),
]

for module, args in modules_to_run:
    module.run(*args)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=11352,
        reload=True
    )
