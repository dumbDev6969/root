import json

with open("jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)  # Use json.load() instead of json.loads()
jobz = []
for job in jobs:
    try:
        job = json.loads(job)
        results = job["results"]["results"]["jobs"]
        jobz.extend(results)
    except:
        pass

