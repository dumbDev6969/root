from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from utils.logger import get_logger
from utils.crud import CRUD
from utils.database import db
from utils.security import validate_input
from utils.databse_operations import get_all_records
from datetime import datetime

crud = CRUD(db)
logger = get_logger(__name__)
router = APIRouter()



def serialize_data(data):
    if isinstance(data, dict):
        return {k: serialize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data

# Corrected import state


def records(table):
    try:
        response = get_all_records(table)
        if response['success']:
            data = serialize_data(response['message'])
            return data
        else:
            return HTTPException(status_code=404, detail=response['message'])
    except Exception as e:
        return  HTTPException(status_code=500, detail=str(e))


@router.post("/api/signup/jobseeker")
async def jobseeker(request: Request):
    try:
        body = await request.json()
        table = "users"  # Fixed table name as per user's request
        data_to_insert = body['data']

        users = records("users")
        for i in users:
            if i["email"] ==  data_to_insert["email"]:
                  return {"message": f"email alread exixst"} 
            
        emplyoers = records("employers")
        for i in emplyoers:
            if i["email"] ==  data_to_insert["email"]:
                  return {"message": f"email alread exixst"} 

        crud.create(table, data_to_insert)  # Pass data_to_insert as a single argument
        return {"message": f"Record created in {table} table."}
    except HTTPException as http_err:
        # If it is a validation HTTPException, re-raise it
        raise http_err
    except Exception as e:
        logger.error(f"Error during employer signup: {e}")
        return str(e)

@router.post("/api/signup/recruter")
async def recruter(request: Request, _: None = Depends(validate_input)):
    try:
        body = await request.json()
        table = "employers"  # Fixed table name as per user's request
        data_to_insert = body['data']
        r = records(table)
        users = records("users")
        for i in users:
            if i["email"] ==  data_to_insert["email"]:
                return {"message": f"email alread exixst"} 
            
        emplyoers = records("employers")
        for i in emplyoers:
                if i["email"] ==  data_to_insert["email"]:
                    return {"message": f"email alread exixst"} 
        crud.create(table, data_to_insert)  # Pass data_to_insert as a single argument
        return {"message": f"Record created in {table} table."}
    except HTTPException as http_err:
        # If it is a validation HTTPException, re-raise it
        raise http_err
    except Exception as e:
        logger.error(f"Error during employer signup: {e}")
        return str(e)
