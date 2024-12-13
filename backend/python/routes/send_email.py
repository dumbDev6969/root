from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from utils.email_sender import my_send_email
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()  # loads the environment variables from the .env file

sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')

router = APIRouter()

class HandleEmailRequest(BaseModel):
    subject: str
    body: str
    recipients: List[EmailStr]

@router.post("/sendemail")
async def send_email(request: HandleEmailRequest):
    try:
        my_send_email(
            subject=request.subject,
            body=request.body,
            sender=sender_email,
            recipients=request.recipients,
            password=sender_password
        )
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
