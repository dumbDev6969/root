from fastapi import APIRouter, Request, HTTPException
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/api/signup/jobseeker")
async def jobseeker(request: Request, crud):
    try:
        body = await request.json()
        table = body['table']
        data_to_insert = body['data']
    
        crud.create(table, **data_to_insert)
        return {"message": f"Record created in {table} table."}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/signup/recruter")
async def recruter(request: Request, crud):
    try:
        body = await request.json()
        table = body['table']
        data_to_insert = body['data']
    
        crud.create(table, **data_to_insert)
        return {"message": f"Record created in {table} table."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
