import csv
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
    search_term="software engineer",
    google_search_term="software engineer jobs near San Francisco, CA since yesterday",
    location="San Francisco, CA",
    results_wanted=1,
    hours_old=72,
    country_indeed='USA',
    
    #linkedin_fetch_description=True 
  
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())
jobs.to_excel("jobs.(.xlsx)",  index=False)