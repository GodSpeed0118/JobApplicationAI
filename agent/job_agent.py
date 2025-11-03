# agent/job_agent.py
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgent
from tools.greenhouse_tools import search_jobs_tool
from tools.resume_tools import tailor_resume_tool
# from tools.resume_tools import tailor_resume_tool  # add later if needed

def init_job_agent():
    llm = OpenAI(model="gpt-4o")
    tools = [search_jobs_tool, tailor_resume_tool]  # Add more tools here
    agent = FunctionCallingAgent.from_tools(tools, llm=llm, verbose=True)
    return agent
