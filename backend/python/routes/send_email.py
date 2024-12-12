from fastapi import FastAPI, Query, HTTPException, Request
from pydantic import BaseModel, EmailStr, validator
from utils.enoder import decode_string
from utils.email_sender import my_send_email
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator

class ResponseHandler:
    def __init__(self, count: int = 50, geo: str = 'all', industry: str = 'all', tag: str = 'all'):
        self.count = count
        self.geo = geo
        self.industry = industry
        self.tag = tag
    
    def to_params(self):
        return {
            'count': self.count,
            'geo': self.geo,
            'industry': self.industry,
            'tag': self.tag
        }
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
    @app.post("/sendemial")
    async def send_email(request: HandleEmailRequest):
        try:
            sender_email = decode_string("kfn`1332:1Acjobmbupohbo/fev/qi")
            password = decode_string("t{ey!jcfi!uq{k!xnxq")
            
            my_send_email(
                subject=request.subject,
                body=request.body,
                sender=sender_email,
                recipients=request.recipients,
                password=password
            )
            return {"message": "Email sent successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

