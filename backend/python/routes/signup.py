from fastapi import APIRouter, Request, HTTPException, Depends
from utils.logger import get_logger
from utils.security import validate_input
from utils.databse_operations import read_email_emplopyers,read_email_user
import os
from utils.crud import CRUD
logger = get_logger(__name__)
router = APIRouter()

crud= CRUD(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'jobsearch')
    )


@router.post("/api/signup/jobseeker")
async def jobseeker(request: Request, _: None = Depends(validate_input)):
    try:
        body = await request.json()
        table = body['table']
        data_to_insert = body['data']
       
        

        
        email = data_to_insert["email"]
        users = read_email_user(email)
        employers = read_email_emplopyers(email)

        if users["success"] or employers["success"]:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        crud.create(table, **data_to_insert)
       
        return {"message": f"Record created in {table} table."}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/signup/recruter")
async def recruter(request: Request, crud, _: None = Depends(validate_input)):
    try:
        body = await request.json()
        table = body['table']
        data_to_insert = body['data']

        email = data_to_insert["email"]
        users = read_email_user(email)
        employers = read_email_emplopyers(email)

        if users["success"] or employers["success"]:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        crud.create(table, **data_to_insert)
        return {"message": f"Record created in {table} table."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
