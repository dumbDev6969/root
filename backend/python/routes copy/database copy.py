
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict
import json

# Import all CRUD functions from database_operations.py
from utils.databse_operations import (
    create_user, read_user, update_user, delete_user,
    create_employer, read_employer, update_employer, delete_employer,
    create_job, read_job, update_job, delete_job,
    create_qualification, read_qualification, update_qualification, delete_qualification,
    create_saved_job, read_saved_job, update_saved_job, delete_saved_job,
    create_submitted_resume, read_submitted_resume, update_submitted_resume, delete_submitted_resume,
    create_user_interest, read_user_interest, update_user_interest, delete_user_interest
)

router = APIRouter()

# Mapping tables to their respective CRUD functions
CRUD_MAP = {
    'users': {
        'create': create_user,
        'read': read_user,
        'update': update_user,
        'delete': delete_user
    },
    'employers': {
        'create': create_employer,
        'read': read_employer,
        'update': update_employer,
        'delete': delete_employer
    },
    'jobs': {
        'create': create_job,
        'read': read_job,
        'update': update_job,
        'delete': delete_job
    },
    'qualifications': {
        'create': create_qualification,
        'read': read_qualification,
        'update': update_qualification,
        'delete': delete_qualification
    },
    'saved_jobs': {
        'create': create_saved_job,
        'read': read_saved_job,
        'update': update_saved_job,
        'delete': delete_saved_job
    },
    'submitted_resume': {
        'create': create_submitted_resume,
        'read': read_submitted_resume,
        'update': update_submitted_resume,
        'delete': delete_submitted_resume
    },
    'user_interest': {
        'create': create_user_interest,
        'read': read_user_interest,
        'update': update_user_interest,
        'delete': delete_user_interest
    }
}

# Generic Create Model
class CreateRequest(BaseModel):
    table: str
    data: Dict[str, Any]

# Generic Read Model
class ReadRequest(BaseModel):
    table: str
    id: int

# Generic Update Model
class UpdateRequest(BaseModel):
    table: str
    id: int
    data: Dict[str, Any]

# Generic Delete Model
class DeleteRequest(BaseModel):
    table: str
    id: int

@router.post("/api/create")
async def create_record(request: CreateRequest):
    table = request.table.lower()
    data = request.data

    if table not in CRUD_MAP:
        raise HTTPException(status_code=400, detail=f"Invalid table name: {table}")

    try:
        create_func = CRUD_MAP[table]['create']
        
        # Dynamically unpack data based on the table
        response = create_func(**data)
        if response['success']:
            return {"message": response['message']}
        else:
            raise HTTPException(status_code=400, detail=response['message'])
    except TypeError as te:
        raise HTTPException(status_code=400, detail=f"Invalid data fields: {te}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/read")
async def read_record(table: str, id: int):
    table = table.lower()

    if table not in CRUD_MAP:
        raise HTTPException(status_code=400, detail=f"Invalid table name: {table}")

    try:
        read_func = CRUD_MAP[table]['read']
        response = read_func(id)
        if response['success']:
            # Parse the JSON string back to a dictionary
            data = json.loads(response['message'])
            return {"data": data}
        else:
            raise HTTPException(status_code=404, detail=response['message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/update")
async def update_record(request: UpdateRequest):
    table = request.table.lower()
    record_id = request.id
    data = request.data

    if table not in CRUD_MAP:
        raise HTTPException(status_code=400, detail=f"Invalid table name: {table}")

    try:
        update_func = CRUD_MAP[table]['update']
        response = update_func(record_id, **data)
        if response['success']:
            return {"message": response['message']}
        else:
            raise HTTPException(status_code=400, detail=response['message'])
    except TypeError as te:
        raise HTTPException(status_code=400, detail=f"Invalid data fields: {te}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/delete")
async def delete_record(request: DeleteRequest):
    table = request.table.lower()
    record_id = request.id

    if table not in CRUD_MAP:
        raise HTTPException(status_code=400, detail=f"Invalid table name: {table}")

    try:
        delete_func = CRUD_MAP[table]['delete']
        response = delete_func(record_id)
        if response['success']:
            return {"message": response['message']}
        else:
            raise HTTPException(status_code=404, detail=response['message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# c:\Users\jemca\OneDrive\Desktop\jobfinder\root\backend\python\routes\crud_routes.py
