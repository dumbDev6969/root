from fastapi import FastAPI, Query
import requests
import feedparser

<<<<<<< HEAD

from utils.enoder import decode_string,encode_string
from utils.email_sender import send_email

import smtplib
server=smtplib.SMTP(host="smtp.gmail.com",port=587)



=======
>>>>>>> f34c7e8a538167fb1ee6f78cd7a942a3a77fa6c7
app = FastAPI()

class ResponseHandler:
    def __init__(self, count: int = 50, geo: str = 'all', industry: str = 'all', tag: str = 'all'):
        """
        Initialize the ResponseHandler.
        
        Args:
            count: Number of jobs to return. Defaults to 50.
            geo: Filter by geographic location. Defaults to 'all'.
            industry: Filter by industry. Defaults to 'all'.
            tag: Filter by tag. Defaults to 'all'.
        """
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

@app.get("/api/remote-jobs")
async def get_remote_jobs(
    count: int = Query(50, ge=1, le=50),
    geo: str = 'all',
    industry: str = 'all',
    tag: str = 'all'
):
    """
    Fetches remote jobs from the Jobicy API with specified filters.

    Args:
        count (int): Number of job listings to retrieve (default is 50, min is 1, max is 50).
        industry (str): Industry filter (default is 'all').
        tag (str): Tag filter (default is 'all').

    Returns:
        JSON response containing the list of job postings if the request is successful,
        otherwise a dictionary containing an error message.
    """
    #geo (str): Geographic region filter (default is 'all').
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
    """
    Retrieve a list of remote job postings from Jobicy as an RSS feed.

    Args:
        job_categories (str): Comma-separated list of job categories. Defaults to ''.
        job_types (str): Comma-separated list of job types. Defaults to ''.
        search_keywords (str): Keywords to search for. Defaults to ''.
        search_region (str): Region to search for. Defaults to ''.

    Returns:
        dict: A dictionary containing the list of RSS feed entries.
    """
    rss_url = 'https://jobicy.com/?feed=job_feed'
    rss_url += f"&job_categories={job_categories}&job_types={job_types}&search_keywords={search_keywords}&search_region={search_region}"
    
    rss_feed = feedparser.parse(rss_url)
    
    return {"entries": [entry for entry in rss_feed.entries]}

<<<<<<< HEAD
@app.post("/send_emial")
async def send_email(
    subject: str = '',
    body: str = '', 
    recipients: list = []
    
):

    """
    Sends an email with the specified subject and body to the given list of recipients.

    Args:
        subject (str): The subject of the email. Defaults to an empty string.
        body (str): The body content of the email. Defaults to an empty string.
        recipients (list): A list of recipient email addresses. Defaults to an empty list.

    Returns:
        json status
    """

    # subject = "daily update"
    # body = "This is your daily update"
    # sender = "jem_022190@binalatongan.edu.ph"  
    # recipients = ["jemcarlo46@gmail.com"", "recipient2@gmail.com"]

    try:
        sender=decode_string("kfn`1332:1Acjobmbupohbo/fev/qi")
        password = decode_string("t{ey!jcfi!uq{k!xnxq")
        
        send_email(subject, body, sender, recipients, password)

        return {"message": "Email sent successfully"}
    except:
        return {"error": "Failed to send email"}
   
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
=======

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
>>>>>>> f34c7e8a538167fb1ee6f78cd7a942a3a77fa6c7
