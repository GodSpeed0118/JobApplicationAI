from typing import Dict, Any, List
import json
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o-mini")

def extract_keywords_from_job(job_details_json: str):

    try:
        jobs = json.loads(job_details_json)
    except json.JSONDecodeError:
        return "Error: Invalid job details format"
    
    if not jobs:
        return "No jobs found."
    
    job = jobs[0]  # first job
    job_description = job.get("description", "")

    if not job_description.strip():
        return "No description found."

    keyword_prompt = f"""
    Extract important technical skills, tools, and keywords from this job description.

    Rules:
    - Only extract what is explicitly mentioned
    - Return ONE keyword per line
    - No explanations

    JOB DESCRIPTION:
    {job_description}
    """

    return llm.complete(keyword_prompt).text.strip()

extract_keywords_tool = FunctionTool.from_defaults(
    fn=extract_keywords_from_job,
    name="extract_keywords_from_job",
    description="Extracts technical keywords from job descriptions. Input must be the JSON string output from get_greenhouse_job_details. Returns keywords one per line."
)