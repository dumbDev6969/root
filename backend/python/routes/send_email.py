from fastapi import FastAPI, Query, HTTPException, Request
from pydantic import BaseModel, EmailStr, validator
from utils.enoder import decode_string
from utils.email_sender import my_send_email
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator
import os
from dotenv import load_dotenv

load_dotenv()  # loads the environment variables from the .env file

sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')

class HandleEmailRequest(BaseModel):
    subject: str
    body: str
    recipients: List[EmailStr]

    @field_validator('recipients')
    def validate_recipients(cls, v):
        if not v:
            raise ValueError('Recipients list cannot be empty')
        return v

def run(app):
    @app.post("/sendemail")
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