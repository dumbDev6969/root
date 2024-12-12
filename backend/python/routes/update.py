from fastapi import FastAPI, Query, HTTPException, Request
from pydantic import BaseModel, EmailStr, validator
from utils.enoder import decode_string
from utils.email_sender import my_send_email
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator


class DataModel(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    state: str
    city_or_province: Optional[str]
    municipality: Optional[str]
    zip_code: str
    street: Optional[str]
    email: str
    password: str
    created_at: Optional[str]
    updated_at: Optional[str]

class UpdateRequest(BaseModel):
    table: str
    id: int
    data: DataModel


def run(app,crud):
    @app.put("/api/update")
    async def update_record(request: UpdateRequest):
        try:
            print(request.data)
            crud.update(request.table, request.id, **request.data)
            return {"message": f"Record updated in {request.table} table."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))