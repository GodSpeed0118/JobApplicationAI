import requests
import re
import json
from typing import Dict, Any, List
from llama_index.core.tools import FunctionTool

def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()      
    return text

def get_greenhouse_job_details(jobs_json: str):
    try:
        jobs = json.loads(jobs_json)
    except json.JSONDecodeError:
        return "Error: Invalid JSON format for jobs"
    
    if not isinstance(jobs, list):
        return "Error: Expected a list of jobs"
    
    if not jobs:
        return "No jobs to fetch details for."
    
    job_descriptions = []
    for job in jobs:
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{job['company']}/jobs/{job['id']}?content=true"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                job_descriptions.append({
                    "company": job.get("company"),
                    "title": job.get("title"),
                    "id": job.get("id"),
                    "error": f"Failed to retrieve details (status {response.status_code})"
                })
                continue
            
            job_content = response.json().get("content", "")
            clean_job_content = strip_html(job_content)[:6000]
            
            job_descriptions.append({
                "company": job.get("company"),
                "title": job.get("title"),
                "location": job.get("location", "N/A"),
                "id": job.get("id"),
                "absolute_url": job.get("absolute_url"),
                "description": clean_job_content
            })
            
        except Exception as e:
            job_descriptions.append({
                "company": job.get("company", "Unknown"),
                "title": job.get("title", "Unknown"),
                "id": job.get("id", "Unknown"),
                "error": f"Error processing job: {str(e)}"
            })

    return json.dumps(job_descriptions, indent=2)

greenhouse_job_details_tool = FunctionTool.from_defaults(
    fn=get_greenhouse_job_details,
    name="get_greenhouse_job_details",
    description="Takes JSON string output from search_greenhouse_jobs and fetches full job descriptions. Returns detailed job information including descriptions as JSON string."
)