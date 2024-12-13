from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
from utils.email_sender import my_send_email  # Ensure correct import
import os
from dotenv import load_dotenv

load_dotenv()  # loads the environment variables from the .env file



router = APIRouter()

class ContactForm(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    message: str

@router.post("/contact_sendmail")
async def contact_form_submission(form: ContactForm):
    try:
        sender_email = os.getenv('SENDER_EMAIL')
        password = os.getenv('SENDER_PASSWORD')
        subject = "New Contact Form Submission"
        body = f"""
        You have a new contact form submission:

        First Name: {form.first_name}
        Last Name: {form.last_name}
        Email: {form.email}
        Message: {form.message}
        """
        recipients = ["jemcarlo46@gmail.com"]

        # Call the provided my_send_email function
        my_send_email(
            subject=subject,
            body=body,
            sender=sender_email,
            recipients=recipients,
            password=password
        )
        print("Email sent successfully")
        return {"message": "Email sent successfully"}
    except HTTPException as e:
        print("HTTPException:", e)
        raise e  # Let FastAPI handle the exception
    except Exception as e:
        print("Exception:", e)
        raise HTTPException(status_code=500, detail=str(e))
