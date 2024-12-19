from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from utils.logger import get_logger
from utils.security import validate_input
from utils.databse_operations import get_all_records, create_user, create_employer
from utils.password_manager import PasswordManager
from utils.id_generator import generate_user_id
from datetime import datetime

logger = get_logger(__name__)
router = APIRouter()
password_manager = PasswordManager()

def serialize_data(data):
    if isinstance(data, dict):
        return {k: serialize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data

def records(table):
    try:
        response = get_all_records(table)
        if response['success']:
            data = serialize_data(response['message'])
            return data
        else:
            return HTTPException(status_code=404, detail=response['message'])
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.post("/api/signup/jobseeker")
async def jobseeker(request: Request):
    try:
        # Get and validate request data
        body = await request.json()
        data = body['data']
        logger.info(f"Raw data received: {data}")
        
        if 'password' not in data:
            raise HTTPException(status_code=400, detail="Password is required")
        
        # Generate unique user ID
        user_uuid = generate_user_id(prefix="USR")
        logger.info(f"Generated UUID for jobseeker: {user_uuid}")

        # Hash the password first to avoid unnecessary database operations if hashing fails
        try:
            hashed_password = password_manager.hash_password(data['password'])
            logger.info(f"Password hashed successfully")
        except Exception as e:
            logger.error(f"Error hashing password: {e}")
            raise HTTPException(status_code=500, detail=f"Error hashing password: {str(e)}")

        # Check for existing users with proper error handling
        # try:
        #     users = records("users")
        #     if not isinstance(users, list):
        #         raise HTTPException(status_code=500, detail="Error fetching user records")
                
        #     for i in users:
        #         if i["email"] == data["email"]:
        #             return {"message": "Email already exists"}

        #     employers = records("employers")
        #     if not isinstance(employers, list):
        #         raise HTTPException(status_code=500, detail="Error fetching employer records")
                
        #     for i in employers:
        #         if i["email"] == data["email"]:
        #             return {"message": "Email already exists"}
        # except Exception as e:
        #     logger.error(f"Error checking existing users: {e}")
        #     raise HTTPException(status_code=500, detail="Error validating user data")

        # Create user with the hashed password
        try:
            result = create_user(
                user_uuid=user_uuid,  # Add the UUID
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data['phone_number'],
                state=data['state'],
                municipality=data['municipality'],
                zip_code=data['zip_code'],
                email=data['email'],
                password=hashed_password,  # Use the hashed password
                city_or_province=data.get('city_or_province'),
                street=data.get('street')
            )
            
            if not result['success']:
                logger.error(f"Error creating user: {result['message']}")
                raise HTTPException(status_code=500, detail=result['message'])
                
            logger.info("User created successfully with hashed password and UUID")
            return {"message": "User created successfully", "user_uuid": user_uuid}
        except Exception as e:
            logger.error(f"Error during user creation: {e}")
            raise HTTPException(status_code=500, detail="Failed to create user")
        raise http_err
    except Exception as e:
        logger.error(f"Error during jobseeker signup: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/signup/recruter")
async def recruter(request: Request, _: None = Depends(validate_input)):
    try:
        # Get and validate request data
        body = await request.json()
        data = body['data']
        logger.info(f"Raw data received for recruiter: {data}")
        
        if 'password' not in data:
            raise HTTPException(status_code=400, detail="Password is required")

        # Generate unique employer ID
        employer_uuid = generate_user_id(prefix="EMP")
        logger.info(f"Generated UUID for employer: {employer_uuid}")

        # Hash the password first to avoid unnecessary database operations if hashing fails
        try:
            hashed_password = password_manager.hash_password(data['password'])
            logger.info("Password hashed successfully for recruiter")
        except Exception as e:
            logger.error(f"Error hashing password for recruiter: {e}")
            raise HTTPException(status_code=500, detail=f"Error hashing password: {str(e)}")

        # Check for existing users with proper error handling
        # try:
        #     users = records("users")
        #     if not isinstance(users, list):
        #         raise HTTPException(status_code=500, detail="Error fetching user records")
                
        #     for i in users:
        #         if i["email"] == data["email"]:
        #             return {"message": "Email already exists"}

        #     employers = records("employers")
        #     if not isinstance(employers, list):
        #         raise HTTPException(status_code=500, detail="Error fetching employer records")
                
        #     for i in employers:
        #         if i["email"] == data["email"]:
        #             return {"message": "Email already exists"}
        # except Exception as e:
        #     logger.error(f"Error checking existing users: {e}")
        #     raise HTTPException(status_code=500, detail="Error validating user data")

        # Create employer with hashed password
        try:
            result = create_employer(
                employer_uuid=employer_uuid,  # Add the UUID
                company_name=data['company_name'],
                phone_number=data['phone_number'],
                state=data['state'],
                zip_code=data['zip_code'],
                password=hashed_password,  # Use the hashed password
                email=data.get('email'),
                city_or_province=data.get('city_or_province'),
                street=data.get('street')
            )
            
            if not result['success']:
                logger.error(f"Error creating employer: {result['message']}")
                raise HTTPException(status_code=500, detail=result['message'])
                
            logger.info("Employer created successfully with hashed password and UUID")
            return {"message": "Employer created successfully", "employer_uuid": employer_uuid}
        except Exception as e:
            logger.error(f"Error during employer creation: {e}")
            raise HTTPException(status_code=500, detail="Failed to create employer")
            return {"message": "Employer created successfully"}
        except HTTPException as http_err:
            raise http_err
    except Exception as e:
        logger.error(f"Error during recruiter signup: {e}")
        raise HTTPException(status_code=500, detail=str(e))
