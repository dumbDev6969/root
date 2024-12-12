from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
import requests
import feedparser
from utils.crud import CRUD
from utils.enoder import decode_string
from utils.email_sender import my_send_email
from pydantic import BaseModel, EmailStr, field_validator
from routes import geo,signup,send_email

crud = CRUD(host='localhost', user='root', password='', database='jobsearch')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Srecruter(BaseModel):
    company_name: str
    phone_number: str
    state: str
    city_or_province: Optional[str]
    municipality: Optional[str]
    zip_code: str
    street_number: Optional[str]
    email: str
    password: str
    created_at: Optional[str]
    updated_at: Optional[str]

class DataModel(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    state: str
    city_or_province: Optional[str]
    municipality: Optional[str]
    zip_code: str
    street: Optional[str]
    email: str
    password: str
    created_at: Optional[str]
    updated_at: Optional[str]

class SignupRecruter(BaseModel):
    table: str
    data: Srecruter

class CreateRequest(BaseModel):
    table: str
    data: dict

class UpdateRequest(BaseModel):
    table: str
    id: int
    data: DataModel

class HandleEmailRequest(BaseModel):
    subject: str
    body: str
    recipients: List[EmailStr]

    @field_validator('recipients')
    def validate_recipients(cls, v):
        if not v:
            raise ValueError('Recipients list cannot be empty')
        return v

@app.get("/api/remote-jobs")
async def get_remote_jobs(
    count: int = Query(50, ge=1, le=50),
    geo: str = 'all',
    industry: str = 'all',
    tag: str = 'all'
):
    params = ResponseHandler(count=count, geo=geo, industry=industry, tag=tag).to_params()
    response = requests.get('https://jobicy.com/api/v2/remote-jobs', params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve jobs"}

@app.get("/rss/remote-jobs")
async def get_remote_jobs_rss(
    job_categories: str = '',
    job_types: str = '',
    search_keywords: str = '',
    search_region: str = ''
):
    rss_url = 'https://jobicy.com/?feed=job_feed'
    rss_url += f"&job_categories={job_categories}&job_types={job_types}&search_keywords={search_keywords}&search_region={search_region}"
    
    rss_feed = feedparser.parse(rss_url)
    
    return {"entries": [entry for entry in rss_feed.entries]}


@app.put("/api/update")
async def update_record(request: UpdateRequest):
    try:
        print(request.data)
        crud.update(request.table, request.id, **request.data)
        return {"message": f"Record updated in {request.table} table."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

geo.run(app)
signup.run(app,crud)
send_email.run(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",  # Use "module_name:app_variable"
        host="127.0.0.1", 
        port=11352, 
        reload=True
    )