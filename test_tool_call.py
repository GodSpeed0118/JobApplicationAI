from llama_index.core.tools import FunctionAgent
from llama_index.llms.openai import OpenAI
from tools.greenhouse_tools import search_jobs_tool, search_greenhouse_jobs

agent = FunctionAgent(
    tools=[search_greenhouse_jobs],
    llm=OpenAI(model="gpt-4o-mini"),
    system_prompt="You are a helpful assistant that searches job listings on Greenhouse by company and keyword ",
)

response = agent.run("Find me engineering jobs from Stripe")

print(str(response))