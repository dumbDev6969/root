from fastapi import APIRouter, Request, HTTPException, Depends
from utils.logger import get_logger
from utils.security import validate_input
from utils.databse_operations import read_email_emplopyers,read_email_user
from routes.database import serialize_data
import json
logger = get_logger(__name__)
router = APIRouter()
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError

class LoginRequest(BaseModel):
    email: str
    password: str

    

@router.post("/login")
async def login(form: LoginRequest, _: None = Depends(validate_input)):
    try:
        email = form.email
        password = form.password
        
        users = read_email_user(email)
        employers = read_email_emplopyers(email)

        if users["success"]:
            if users['message']['password'] == password:
                return {
                    "message": "welcome user",
                    "personal_info": users['message']
                }
        if employers["success"]:
            if employers['message']['password'] == password:
                return {
                    "message": "welcome employer",
                    "personal_info": employers['message']
                }
        
        raise HTTPException(status_code=404, detail="User not found")
       
     

        return {"message": f"llogging in"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

