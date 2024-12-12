import requests
from fastapi import FastAPI, Query, HTTPException, Request
import requests
import feedparser

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
    
def run(app):
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

