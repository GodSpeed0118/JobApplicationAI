import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from tools.greenhouse_tools import search_jobs_tool
from tools.resume_tools import extract_keywords_tool
from tools.greenhouse_job_description import greenhouse_job_details_tool
from dotenv import load_dotenv
load_dotenv()


async def main():
    agent = FunctionAgent(
        tools=[search_jobs_tool, greenhouse_job_details_tool, extract_keywords_tool],
        llm=OpenAI(model="gpt-4o-mini"),
        system_prompt = "You are a helpful assistant that searches job listings on Greenhouse and extracts important keywords. Always use tools in this order: 1) search_jobs_tool 2) get_greenhouse_job_details 3) extract_keywords_from_job",
        verbose = True
    )

    response = await agent.run("Find me important keywords for software engineer job descriptions at Stripe in San Francisco")

    print(str(response))


if __name__ == "__main__":
    asyncio.run(main())