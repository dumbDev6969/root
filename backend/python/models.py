from pydantic import BaseModel, validator
import re

class Srecruter(BaseModel):
    phone_number: str

    @validator('phone_number')
    def validate_phone_number(cls, v: str) -> str:
        if not re.match(r'^\+?1?\d{9,15}$', v):
            raise ValueError("Invalid phone number format")
        return v

class SignupRecruter(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str

class CreateRequest(BaseModel):
    table: str
    data: dict
