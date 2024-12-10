from flask import Flask, jsonify,render_template
import feedparser
import requests

app = Flask(__name__)

# Remotive's RSS feed URL
# RSS_FEED_URL = "https://remotive.com/remote-jobs/feed"
RSS_FEED_URL = "https://jobicy.com/?feed=job_feed"

import requests
import xml.etree.ElementTree as ET

def get_recent_remote_jobs():
    url = "https://jobicy.com/feed/newjobs"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        jobs = []

        for item in root.findall(".//item"):
            job = {
                "title": item.find("title").text,
                "link": item.find("link").text,
                "description": item.find("description").text,
            }
            jobs.append(job)

        return jobs
    else:
        return None
@app.route('/feed/newjobs', methods=['GET'])
def feed_newjobs():
    """
    Fetches remote software development jobs from Remotive's RSS feed.
    
    Returns:
        A JSON response containing a list of job postings.
    """
    try:
        # Parse the RSS feed
        feed = feedparser.parse("https://jobicy.com/feed/newjobs")
        
        # Extract job postings from the feed
        jobs = []
        for entry in feed.entries:
            job = {
                'title': entry.title,
                'link': entry.link,
                'description': entry.description,
                'published': entry.published
            }
            jobs.append(job)
        
        # Return the job postings as JSON
        return render_template("sample.html", jobs=jobs)
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        return jsonify({'error': str(e)}), 500
    



@app.route('/', methods=['GET'])
def get_jobs():
    """
    Fetches remote software development jobs from Remotive's RSS feed.
    
    Returns:
        A JSON response containing a list of job postings.
    """
    try:
        # Parse the RSS feed
        feed = feedparser.parse(RSS_FEED_URL)
        
        # Extract job postings from the feed
        jobs = []
        for entry in feed.entries:
            job = {
                'title': entry.title,
                'link': entry.link,
                'description': entry.description,
                'published': entry.published
            }
            jobs.append(job)
        
        # Return the job postings as JSON
        return render_template("sample.html", jobs=jobs)
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)