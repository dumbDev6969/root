from fastapi import APIRouter, Request, HTTPException, Depends
from utils.logger import get_logger
from utils.security import validate_input
from utils.databse_operations import read_email_employers, read_email_user
from routes.database import serialize_data
from utils.password_manager import PasswordManager
import json
logger = get_logger(__name__)
router = APIRouter()
password_manager = PasswordManager()
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
        employers = read_email_employers(email)

        if users["success"]:
            try:
                if password_manager.verify_password(users['message']['password'], password):
                    # Remove password from response data
                    user_info = users['message'].copy()
                    user_info.pop('password', None)
                    return {
                        "message": "welcome user",
                        "personal_info": user_info
                    }
            except Exception as e:
                logger.error(f"Error verifying user password: {e}")
                raise HTTPException(status_code=500, detail="Error verifying credentials")
                
        if employers["success"]:
            try:
                if password_manager.verify_password(employers['message']['password'], password):
                    # Remove password from response data
                    employer_info = employers['message'].copy()
                    employer_info.pop('password', None)
                    return {
                        "message": "welcome employer",
                        "personal_info": employer_info
                    }
            except Exception as e:
                logger.error(f"Error verifying employer password: {e}")
                raise HTTPException(status_code=500, detail="Error verifying credentials")
        
        raise HTTPException(status_code=404, detail="User not found")
       
     

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

