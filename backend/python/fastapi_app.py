from fastapi import FastAPI, HTTPException
from typing import Dict
import json
import requests
import logging
from bs4 import BeautifulSoup
import json

with open("jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)  # Use json.load() instead of json.loads()

app = FastAPI()

class JobScraper:
    """A class to scrape job listings from JobStreet Philippines."""
    
    def __init__(self, base_url: str = "https://ph.jobstreet.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def extract_job(self, job_id: str) -> Dict:
        url = f"{self.base_url}/job/{job_id}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            script_tags = soup.find_all('script', attrs={'data-rh': 'true', 'type': 'application/ld+json'})
           
            if len(script_tags) > 1 and script_tags[1].contents:
                return json.loads(script_tags[1].contents[0])
            else:
                return {'error': 'Job listing not found or no longer available'}
                
        except Exception as e:
            self.logger.error(f"Error extracting job {job_id}: {str(e)}")
            return {'error': f'Failed to extract job: {str(e)}'}

@app.get("/extract_job/{job_id}")
async def extract_job(job_id: str):
    scraper = JobScraper()
    result = scraper.extract_job(job_id)
    
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    
    return result

@app.get("/jobs")
async def read_jobs():
    jobz = []
    for job in jobs:
        try:
            job = json.loads(job)
            results = job["results"]["results"]["jobs"]
            jobz.extend(results)
        except:
            pass
    return jobz


   
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
