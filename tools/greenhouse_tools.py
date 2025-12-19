import requests
import json
from llama_index.core.tools import FunctionTool

def search_greenhouse_jobs(company: str, keyword: str, location: str):
    """
    Search jobs from a company's Greenhouse job board.
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Failed to retrieve jobs for {company}."

    jobs = response.json().get("jobs", [])

    matching_jobs = []
    for job in jobs:
        if location.lower() not in job["location"]["name"].lower():
            continue  
        if keyword.lower() in job["title"].lower():
            matching_jobs.append({
                "company": company,
                "title": job["title"],
                "location": job.get("location", {}).get("name", "N/A"),
                "id": job["id"],
                "absolute_url": job["absolute_url"],
            })

    if not matching_jobs:
        return f"No jobs found for keyword '{keyword}' at {company} in {location}."
    
    return json.dumps(matching_jobs, indent=2)

search_jobs_tool = FunctionTool.from_defaults(
    fn=search_greenhouse_jobs,
    name="search_greenhouse_jobs",
    description="Searches job listings on Greenhouse by company, keyword, and location."
)