# from fastapi import FastAPI, HTTPException, Request
# from pydantic import BaseModel

# class ContactForm(BaseModel):
#     first_name: str
#     last_name: str
#     email : str
#     message: str

# def run(app, my_send_email):
#     @app.post("/contact_sendmail")
#     async def contact_form_submission(request: Request):
#         try:
#             data = await request.json()
#             form = ContactForm(**data)
#             print("Form data: ", form)
#             print("contact: ", data)
#             return "asdsad"
#             sender_email = "joblits.co@gmail.com"
#             password = "xvuh racq cbue fskh"
#             subject = "New Contact Form Submission"
#             body = "saa"
#             recipients = ["jemcarlo46@gmail.com"]

#             # Call the provided my_send_email function
#             my_send_email(
#                 subject=subject,
#                 body=body,
#                 sender=sender_email,
#                 recipients=recipients,
#                 password=password
#             )
#             print("sendingggggggg")
#             return {"message": "Email sent successfully"}
#         except HTTPException as e:
#             print("errorrrr")
#             return {"message": str(e.detail)}
#         except Exception as e:
#             return {"message": str(e)}

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, EmailStr
from utils.email_sender import my_send_email  # Ensure correct import

class ContactForm(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    message: str

def run(app: FastAPI):
    @app.post("/contact_sendmail")
    async def contact_form_submission(form: ContactForm):
        try:
            print("Form data:", form)
            
            sender_email = "joblits.co@gmail.com"
            password = "xvuh racq cbue fskh"  # Consider using environment variables for security
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