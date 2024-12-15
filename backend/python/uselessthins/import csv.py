# import csv
# from jobspy import scrape_jobs

# jobs = scrape_jobs(
#     site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
#     search_term="software engineer",
#     google_search_term="software engineer jobs near San Francisco, CA since yesterday",
#     location="San Francisco, CA",
#     results_wanted=20,
#     hours_old=72,
#     country_indeed='USA',
    
#     # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
#     # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
# )
# print(f"Found {len(jobs)} jobs")
# print(jobs)



if __name__ == "__main__":
    import requests

    # Set up the data payload for the POST request
    data = {
        "subject": "Test Subject",
        "body": "This is a test email body.",
        "recipients": ["test@example.com", "recipient2@example.com"]
    }

    # Send a POST request to the /send_email endpoint
    response = requests.post("localhost/sendemial", json=data)

    # Print the response
    print(response.json())