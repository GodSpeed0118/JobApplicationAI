import requests
import re
import json
from typing import Dict, Any, List
from llama_index.core.tools import FunctionTool

def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()      
    return text

def get_greenhouse_job_details(jobs: List[Dict[str, Any]]):
    job_descriptions = []
    for job in jobs:
        url = f"https://boards-api.greenhouse.io/v1/boards/{job['company']}/jobs/{job['id']}?content=true"
        response = requests.get(url)

        if response.status_code != 200:
            return f"Failed to retrieve job details for job_id={job["id"]}"
        
        job_content = response.json().get("content", "")
        clean_job_content = strip_html(job_content)[:6000]
        
        job_descriptions.append({
            "company": job["company"],
            "title": job["title"],
            "location": job.get("location", {}).get("name", "N/A"),
            "id": job["id"],
            "absolute_url": job["absolute_url"],
            "description": clean_job_content
        })

    return job_descriptions

greenhouse_job_details_tool = FunctionTool.from_defaults(
    fn=get_greenhouse_job_details,
    name="get_greenhouse_job_details",
    description="Gets the job descriptions of valid jobs displaying the company name on EACH line, title of position, location, id, absolute_url, and the description/content about the job listing all on each line"
)