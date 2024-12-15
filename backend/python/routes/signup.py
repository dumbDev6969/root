from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.crud import CRUD
from utils.database import db  # Import the existing Database instance
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

# Initialize CRUD with the existing Database instance
crud = CRUD(db)

class SignupData(BaseModel):
    username: str
    email: str
    password: str

@router.post("/signup")
async def signup(data: SignupData):
    try:
        # Check if user already exists
        existing_user = crud.read("users", {"email": data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Create new user
        new_user = {
            "username": data.username,
            "email": data.email,
            "password": data.password  # Note: In a real application, you should hash the password
        }
        user_id = crud.create("users", new_user)

        return {"message": "User created successfully", "user_id": user_id}
    except Exception as e:
        logger.error(f"Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
