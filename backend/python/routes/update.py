from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

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

@router.put("/api/update")
async def update_record(request: UpdateRequest, crud):
    try:
        crud.update(request.table, request.id, **request.data.dict())
        return {"message": f"Record updated in {request.table} table."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
